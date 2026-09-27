#!/usr/bin/env python3
"""One narrow GitHub main-branch commit for the 359-choice Arabic review update."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "expert-review/2026-09-26-final-page-review"
PACKAGE = REVIEW / "REVIEW_359_SOURCE_RECEIPT.json"
STATE = ROOT / "evidence/publication/review-359-20260927/GITHUB_TRANSACTION.json"
READBACK = STATE.with_name("GITHUB_READBACK.json")
REMOTE = "https://github.com/KokunoYumeto/OpenLogic-ar"
EXPECTED_PARENT = "32298b975874cafd7bb5dba135ef687ed8886ff5"
COMMIT_MESSAGE = "توسيع فهرس مراجعة الترجمة العربية إلى ٣٥٩ قرارًا"
READBACK_STATUS = "PASS_ANONYMOUS_GITHUB_REVIEW_359_EXACT_FILES"
ALLOW_CHANGED = {
    "expert-review/2026-09-26-final-page-review/WORKING_INDEX_AR.md",
    "expert-review/2026-09-26-final-page-review/README_BUILD_AR.md",
    "build/render_arabic_review_existing_20260927.py",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def git(*args: str, env: dict | None = None) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, env=env, text=True,
                            encoding="utf-8", capture_output=True, check=True)
    return result.stdout.strip()


def remote_main() -> str:
    line = git("ls-remote", "origin", "refs/heads/main")
    return line.split()[0]


def save(value: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def selected_files() -> list[str]:
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    if package["status"] != "PASS_LOCAL_ARABIC_REVIEW_359_EDITABLE_SOURCE_ARCHIVE" or package["coverage"]["arabic_choices"] != 359:
        raise RuntimeError("Reviewed editable-source package not accepted")
    archive = ROOT / package["archive_path"]
    if archive.stat().st_size != package["archive_bytes"] or digest(archive) != package["archive_sha256"]:
        raise RuntimeError("Editable-source archive bytes changed")
    for item in package["members"]:
        path = ROOT / item["path"]
        if path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
            raise RuntimeError("Packaged source drift: " + item["path"])
    paths = [item["path"] for item in package["members"]]
    paths.extend([package["archive_path"], PACKAGE.relative_to(ROOT).as_posix()])
    if len(paths) != len(set(paths)):
        raise RuntimeError("Repeated publication path")
    return paths


def prepare() -> None:
    if STATE.exists():
        raise RuntimeError("Existing GitHub transaction needs inspection, not duplication")
    if remote_main() != EXPECTED_PARENT:
        raise RuntimeError("GitHub main moved; inspect the current remote before publishing")
    paths = selected_files()
    with tempfile.TemporaryDirectory(prefix="arabic-review-359-git-index-") as directory:
        env = dict(os.environ)
        env["GIT_INDEX_FILE"] = str(Path(directory) / "index")
        env.update(GIT_AUTHOR_NAME="OpenAI Codex",
                   GIT_AUTHOR_EMAIL="openai-codex@users.noreply.github.com",
                   GIT_COMMITTER_NAME="OpenAI Codex",
                   GIT_COMMITTER_EMAIL="openai-codex@users.noreply.github.com")
        git("read-tree", EXPECTED_PARENT, env=env)
        changed = []
        for name in paths:
            local = ROOT / name
            oid = git("hash-object", "-w", "--", name, env=env)
            try:
                prior = git("rev-parse", f"{EXPECTED_PARENT}:{name}", env=env)
            except subprocess.CalledProcessError:
                prior = None
            if prior and oid != prior and name not in ALLOW_CHANGED:
                raise RuntimeError("Unexpected modification of inherited public file: " + name)
            if oid != prior:
                changed.append({"path": name, "bytes": local.stat().st_size,
                                "sha256": digest(local), "blob": oid})
            git("update-index", "--add", "--cacheinfo", "100644", oid, name, env=env)
        tree = git("write-tree", env=env)
        commit = git("commit-tree", tree, "-p", EXPECTED_PARENT, "-m",
                     COMMIT_MESSAGE, env=env)
    names = git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines()
    if set(names) != {item["path"] for item in changed} or not changed:
        raise RuntimeError("Prepared commit diff does not match selected bytes")
    state = {"status": "PREPARED", "parent": EXPECTED_PARENT, "commit": commit,
             "tree": tree, "changed": changed, "package_sha256": digest(PACKAGE)}
    save(state)
    print(json.dumps({"status": state["status"], "commit": commit, "changed": len(changed)}))


def push() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state["status"] != "PREPARED" or remote_main() != state["parent"]:
        raise RuntimeError("Prepared GitHub parent or transaction state changed")
    if digest(PACKAGE) != state["package_sha256"]:
        raise RuntimeError("Source package receipt changed before push")
    for item in state["changed"]:
        path = ROOT / item["path"]
        if path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
            raise RuntimeError("Selected public bytes changed before push: " + item["path"])
    state["status"] = "PUSH_ATTEMPTED"
    save(state)
    git("push", "origin", f"{state['commit']}:refs/heads/main")
    if remote_main() != state["commit"]:
        raise RuntimeError("Remote main does not point to the exact prepared commit")
    state["status"] = "PUBLISHED_AWAITING_ANONYMOUS_READBACK"
    save(state)
    print(json.dumps({"status": state["status"], "commit": state["commit"]}))


def verify() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state["status"] != "PUBLISHED_AWAITING_ANONYMOUS_READBACK" or remote_main() != state["commit"]:
        raise RuntimeError("Published GitHub commit state differs")
    prefix = f"https://raw.githubusercontent.com/KokunoYumeto/OpenLogic-ar/{state['commit']}/"
    results = []
    for item in state["changed"]:
        url = prefix + item["path"]
        req = Request(url, headers={"User-Agent": "OpenLogic-Arabic-review-readback/1"})
        size = 0
        h = hashlib.sha256()
        with urlopen(req, timeout=75) as response:
            if response.status != 200:
                raise RuntimeError("Anonymous GitHub download failed: " + item["path"])
            while block := response.read(1024 * 1024):
                size += len(block)
                if size > item["bytes"]:
                    raise RuntimeError("Anonymous GitHub object larger than local: " + item["path"])
                h.update(block)
        if size != item["bytes"] or h.hexdigest().upper() != item["sha256"]:
            raise RuntimeError("Anonymous GitHub bytes differ: " + item["path"])
        results.append({"path": item["path"], "bytes": size,
                        "sha256": h.hexdigest().upper(), "url": url})
    entry = f"{REMOTE}/blob/{state['commit']}/expert-review/2026-09-26-final-page-review/WORKING_INDEX_AR.md"
    with urlopen(Request(entry, headers={"User-Agent": "OpenLogic-Arabic-review-readback/1"}), timeout=60) as response:
        html = response.read(2_000_000)
        if response.status != 200 or b"WORKING_INDEX_AR.md" not in html:
            raise RuntimeError("Human-readable public entry is not anonymously browsable")
    receipt = {"status": READBACK_STATUS,
               "commit": state["commit"], "parent": state["parent"], "file_count": len(results),
               "files": results, "human_entry_url": entry, "html_response_bytes": len(html)}
    READBACK.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    state["status"] = "PASS_ANONYMOUS_GITHUB_READBACK"
    save(state)
    print(json.dumps({"status": state["status"], "commit": state["commit"], "files": len(results)}))


if __name__ == "__main__":
    import sys
    {"prepare": prepare, "push": push, "verify": verify}[sys.argv[1]]()
