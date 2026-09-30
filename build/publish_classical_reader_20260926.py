"""Finite Zenodo transaction for the accepted Classical Arabic reader.

Run only after the GitHub release has passed anonymous byte readback. Inherit
every file in the current concept lineage, upload five checked assets, make
the Classical PDF the preview, publish once, and verify public bytes. The
credential stays in the established private transport; receipts are sanitized.
"""

from __future__ import annotations

import hashlib
import argparse
import json
from pathlib import Path
import sys

import requests

from build import prepare_classical_pdf_release_20260926 as release


REPO = Path(__file__).resolve().parents[1]
STATE_DIR = REPO / "evidence/publication/classical-eastern-rtl-20260926"
TRANSPORT_ROOT = Path(
    "C:/interlanguage-production/openlogic-arabic-review-publication-20260907"
)
sys.path.insert(0, str(TRANSPORT_ROOT))
from publish_checked_supplement import authenticated, call, save  # noqa: E402


API = "https://zenodo.org/api"
RDM = "application/vnd.inveniordm.v1+json"
PREVIOUS = 22951266
CONCEPT = 21921850
PREVIEW = release.NAMES[0]
VERSION = "OLP-0722-AR-CLASSICAL-EASTERN-RTL-20260926"
SUCCESSOR = False
ORDER_PREFIX: tuple[str, ...] = ()
REPLACEMENT_NAMES: tuple[str, ...] | None = None


def configure_successor(path: Path) -> None:
    global STATE_DIR, PREVIOUS, VERSION, SUCCESSOR
    release.configure_successor(path)
    STATE_DIR = release.PUBLICATION
    PREVIOUS = int(release.SUCCESSOR_CONFIG["previous_zenodo_record"])
    VERSION = release.SUCCESSOR_CONFIG["zenodo_version"]
    SUCCESSOR = True


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def assets() -> list[dict]:
    rows = release.local_check()
    require([row["name"] for row in rows] == list(release.NAMES),
            "Classical stage order differs")
    return rows


def public_record(number: int) -> dict:
    response = requests.get(
        f"{API}/records/{number}", headers={"Accept": RDM}, timeout=(20, 60)
    )
    response.raise_for_status()
    return response.json()


def draft_record(session: requests.Session, number: int) -> dict:
    return call(session, "GET", f"{API}/records/{number}/draft",
                headers={"Accept": RDM}).json()


def checked_github_receipt(rows: list[dict]) -> None:
    path = STATE_DIR / "GITHUB_READBACK.json"
    require(path.is_file(), "Anonymous GitHub readback must precede Zenodo")
    receipt = json.loads(path.read_text(encoding="utf-8-sig"))
    require(receipt.get("status") == "PASS_ANONYMOUS_GITHUB_READBACK"
            and receipt.get("release") == release.GITHUB,
            "GitHub readback identity differs")
    by_name = {row["name"]: row for row in receipt.get("files", [])}
    require(set(by_name) == {row["name"] for row in rows},
            "GitHub file inventory differs")
    for row in rows:
        public = by_name[row["name"]]
        require((public["bytes"], public["sha256"]) ==
                (row["bytes"], row["sha256"]),
                "GitHub public bytes differ: " + row["name"])


def metadata_for(draft: dict) -> dict:
    metadata = dict(draft["metadata"])
    metadata.pop("doi", None)
    metadata.pop("prereserve_doi", None)
    if SUCCESSOR:
        description = metadata.get("description", "")
        description = (
            '<div lang="ar" dir="rtl"><h2>القارئ التراثي المصحح</h2>'
            '<p>تتيح هذه النسخة القارئ العربي التراثي الكامل ذي الوحدات الـ٧٢٢، '
            'مع ملف LaTeX تراكمي مباشر وحزمة المصدر الكامل القابل لإعادة البناء. '
            'تطبع أسماء الدوال اللاتينية بترتيبها الصحيح داخل الصيغ من اليمين إلى '
            'اليسار، وتصحح خرائط استخراج ستة رموز من خط MSBM10، من غير تغيير '
            'المعنى الرياضي أو الطبعتين العربيتين المعاصرتين.</p>'
            '<p>أُعيد بناء القارئ ومكونيه مستقلًا، وطابقت ملفات PDF بايتًا ببايت. '
            'فُحصت خرائط Unicode واتجاه أسماء الدوال والروابط وحدود الصفحات، '
            'واستُعرضت صفحات ممثلة بصريًا. بقيت المصادر والطبعتان المعاصرتان '
            'وكتب EPUB وسجل المراجعة والتاريخ المنشور متاحة.</p>'
            '<p>تصحيح اتجاه أسماء الدوال وخرائط Unicode: <strong>OpenAI Codex — GPT-6 Astra، '
            'بمستوى جهد Ultra</strong>. إعادة البناء والتحقق والتجميع والنشر لهذه النسخة: '
            '<strong>OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra</strong>. '
            'ويشمل تصحيح GPT-6 Sol اتجاه أسماء النظريات والأنساق وقاعدة القطع ورمز القيمة. '
            'تبقى نسب النماذج السابقة في الملفات والأوصاف الموروثة؛ '
            'ولا يُدَّعى تحرير بشري أو مراجعة عربية بشرية شاملة.</p>'
            f'<p><a href="{release.GITHUB}">القارئ المصحح ومصادره على GitHub</a>.</p></div>'
            + description)
        metadata.update(version=VERSION, publication_date="2026-09-28",
                        access_right="open", description=description,
                        language="ara")
        related = list(metadata.get("related_identifiers", []))
        link = {"identifier": release.GITHUB, "relation": "isIdenticalTo", "scheme": "url"}
        if not any(row.get("identifier") == release.GITHUB for row in related):
            related.append(link)
        metadata["related_identifiers"] = related
        return metadata
    metadata.update(
        title="نص المنطق المفتوح: الطبعة العربية التراثية الكاملة ذات الأرقام الشرقية والصيغ من اليمين إلى اليسار",
        version=VERSION,
        publication_date="2026-09-26",
        access_right="open",
        license="cc-by-4.0",
        creators=[{"name": "Open Logic Project"}],
        language="ara",
        keywords=["العربية التراثية", "المنطق", "الرياضيات", "LaTeX", "اتجاه الصيغ"],
        description=(
            '<div lang="ar" dir="rtl"><h2>الطبعة العربية التراثية الكاملة</h2>'
            '<p>يجمع هذا القارئ الثالث الوحدات المصدرية الـ٧٢٢ في نص واحد بأسلوب عربي '
            'تراثي، مع الأرقام العربية الشرقية، والحروف والرموز الرياضية العربية، '
            'واتجاه الصيغ من اليمين إلى اليسار. يبقى تعريف الأعداد الطبيعية مشتملًا '
            'على الصفر، وتحفظ الطبعة بيانات الأصل وإحالاته وبراهينه وتمارينه.</p>'
            '<p>أول الملفات هو PDF القارئ الكامل للقراءة المباشرة، يليه ملف LaTeX '
            'التراكمي القابل للتنزيل وحده، ثم حزمة جميع المصادر والخطوط والأنماط '
            'والتعليمات اللازمة لإعادة البناء. ويليها الدليل العربي وقائمة SHA-256. '
            'كل الملفات المنشورة سابقًا في هذه السلسلة باقية متاحة.</p>'
            '<p>اجتاز القارئ بناءً معادًا مطابقًا بايتًا ببايت وفحوص التغطية والخطوط '
            'والروابط وحدود الصفحات، وفُحصت صفحات ممثلة بصريًا، ومنها المصادر '
            'والروابط الطويلة. ملف PDF ثابت التخطيط وغير موسوم وفق PDF/UA.</p>'
            f'<p><a href="{release.GITHUB}">طبعة GitHub المطابقة وملفات تنزيلها</a>.</p>'
            '<p>الترجمة والصياغة والتصحيحات الموروثة: <strong>OpenAI Codex — '
            'GPT-5.6 Sol، بمستوى جهد Ultra</strong>. تصحيح التنضيد الأخير وتجميع '
            'القارئ والتحقق منه: <strong>OpenAI Codex — GPT-6 Sol، بمستوى جهد '
            'Ultra</strong>. لم تقع مراجعة بشرية عربية شاملة، وتبقى اختيارات '
            'المصطلحات والأسلوب مفتوحة للتصحيح المتخصص؛ ولا يتوقف نشر الطبعة '
            'على رد بشري.</p></div>'
        ),
        related_identifiers=[
            {"identifier": f"10.5281/zenodo.{CONCEPT}",
             "relation": "isVersionOf", "scheme": "doi"},
            {"identifier": release.GITHUB,
             "relation": "isIdenticalTo", "scheme": "url"},
        ],
    )
    return metadata


def prepare() -> None:
    rows = assets()
    checked_github_receipt(rows)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path = STATE_DIR / "ZENODO_TRANSACTION.json"
    require(not state_path.exists(),
            "Existing transaction must be inspected, not recreated")
    previous = public_record(PREVIOUS)
    require(previous["is_published"] and previous["versions"]["is_latest"],
            "Wrong predecessor state")
    require(int(previous["parent"]["id"]) == CONCEPT,
            "Wrong Zenodo concept")
    require(previous["access"]["record"] == previous["access"]["files"] == "public",
            "Predecessor access is not fully public")
    predecessor_inventory = {
        name: {"bytes": entry["size"], "checksum": entry["checksum"]}
        for name, entry in previous["files"]["entries"].items()
    }
    replacement_names = (set(REPLACEMENT_NAMES) if REPLACEMENT_NAMES is not None
                         else {row["name"] for row in rows}) if SUCCESSOR else set()
    require(replacement_names.issubset(row["name"] for row in rows),
            "Every replacement must have a checked successor asset")
    if SUCCESSOR:
        require(len(predecessor_inventory) == 98 and
                replacement_names.issubset(predecessor_inventory),
                "Successor must replace only named existing files in the 98-file predecessor")
    inherited = {name: row for name, row in predecessor_inventory.items()
                 if name not in replacement_names}
    require((SUCCESSOR or len(inherited) == 81) and
            len(inherited) + len(rows) <= 100, "Inherited/new file cap differs")
    require(not set(inherited).intersection(row["name"] for row in rows),
            "Unexpected new asset collision")
    state = {"status": "CREATING_VERSION", "previous_record": PREVIOUS,
             "concept": CONCEPT, "assets": rows, "inherited": inherited,
             "predecessor_inventory": predecessor_inventory,
             "replaced_in_new_draft_only": sorted(replacement_names)}
    save(state_path, state)
    with authenticated() as session:
        prior = call(session, "GET", f"{API}/deposit/depositions/{PREVIOUS}").json()
        pending = prior["links"].get("latest_draft", "")
        require(not pending or pending.rstrip("/").endswith("/" + str(PREVIOUS)),
                "An existing Zenodo draft requires inspection")
        state["status"] = "NEW_VERSION_POST_ATTEMPTED"
        save(state_path, state)
        created = call(session, "POST",
                       f"{API}/deposit/depositions/{PREVIOUS}/actions/newversion").json()
        draft_url = created["links"].get("latest_draft") or created["links"]["self"]
        draft_id = int(draft_url.rstrip("/").split("/")[-1])
        require(draft_id != PREVIOUS, "New version did not yield a new draft")
        state.update(status="DRAFT_CREATED", draft_id=draft_id)
        save(state_path, state)
        draft = call(session, "GET", f"{API}/deposit/depositions/{draft_id}").json()
        require(int(draft["conceptrecid"]) == CONCEPT and not draft["submitted"],
                "Wrong draft lineage/state")
        actual = {
            item["filename"]: {
                "bytes": item["filesize"],
                "checksum": "md5:" + item["checksum"].removeprefix("md5:"),
            }
            for item in draft["files"]
        }
        require(actual == predecessor_inventory, "Inherited draft inventory differs")
        for item in draft["files"]:
            if item["filename"] in replacement_names:
                url = f"{API}/deposit/depositions/{draft_id}/files/{item['id']}"
                call(session, "DELETE", url)
        for row in rows:
            with (release.STAGE / row["name"]).open("rb") as stream:
                call(session, "PUT", draft["links"]["bucket"] + "/" + row["name"],
                     data=stream,
                     headers={"Content-Type": "application/octet-stream"})
        call(session, "PUT", f"{API}/deposit/depositions/{draft_id}",
             json={"metadata": metadata_for(draft)})
        modern = draft_record(session, draft_id)
        expected = set(inherited) | {row["name"] for row in rows}
        require(set(modern["files"]["entries"]) == expected,
                "Uploaded draft inventory differs")
        payload = {key: modern[key] for key in ("metadata", "access", "custom_fields")
                   if key in modern}
        order_prefix = list(ORDER_PREFIX) if ORDER_PREFIX else [row["name"] for row in rows]
        require(set(order_prefix).issubset(expected) and len(order_prefix) == len(set(order_prefix)),
                "Public reading/source order prefix differs")
        payload["files"] = {
            "enabled": True, "default_preview": PREVIEW,
            "order": order_prefix + sorted(expected - set(order_prefix)),
        }
        call(session, "PUT", f"{API}/records/{draft_id}/draft",
             headers={"Accept": RDM}, json=payload)
        checked = draft_record(session, draft_id)
        require(checked["files"]["default_preview"] == PREVIEW,
                "Wrong Zenodo PDF preview")
        require(checked["access"]["record"] == checked["access"]["files"] == "public",
                "Draft is not public")
        state.update(status="READY_TO_PUBLISH", draft_files=len(expected),
                     default_preview=PREVIEW)
        save(state_path, state)
    print(json.dumps({"status": state["status"], "draft_id": state["draft_id"]}))


def publish() -> None:
    rows = assets()
    checked_github_receipt(rows)
    state_path = STATE_DIR / "ZENODO_TRANSACTION.json"
    state = json.loads(state_path.read_text(encoding="utf-8-sig"))
    require(state["status"] == "READY_TO_PUBLISH" and state["assets"] == rows,
            "Zenodo transaction is not ready")
    with authenticated() as session:
        checked = draft_record(session, int(state["draft_id"]))
        require(checked["files"]["default_preview"] == PREVIEW and
                checked["metadata"]["version"] == VERSION,
                "Draft preview/version changed")
        require(public_record(PREVIOUS)["versions"]["is_latest"],
                "A later concept version appeared")
        state["status"] = "PUBLISH_POST_ATTEMPTED"
        save(state_path, state)
        call(session, "POST",
             f"{API}/deposit/depositions/{state['draft_id']}/actions/publish")
        state["status"] = "PUBLISHED_AWAITING_READBACK"
        save(state_path, state)
    print(json.dumps({"status": state["status"], "record_id": state["draft_id"]}))


def verify() -> None:
    rows = assets()
    state_path = STATE_DIR / "ZENODO_TRANSACTION.json"
    state = json.loads(state_path.read_text(encoding="utf-8-sig"))
    require(state["status"] == "PUBLISHED_AWAITING_READBACK",
            "Publication is not awaiting readback")
    public = public_record(int(state["draft_id"]))
    require(public["is_published"] and public["versions"]["is_latest"],
            "New record is not latest/public")
    require(public["access"]["record"] == public["access"]["files"] == "public",
            "Public access differs")
    require(public["files"]["default_preview"] == PREVIEW,
            "Public PDF preview differs")
    entries = public["files"]["entries"]
    expected = set(state["inherited"]) | {row["name"] for row in rows}
    require(set(entries) == expected, "Public file inventory differs")
    for name, identity in state["inherited"].items():
        require((entries[name]["size"], entries[name]["checksum"]) ==
                (identity["bytes"], identity["checksum"]),
                "Inherited file identity changed: " + name)
    results = []
    inherited_results = []
    by_name = {row["name"]: row for row in rows}
    with requests.Session() as anonymous:
        anonymous.trust_env = False
        names = [row["name"] for row in rows]
        if not SUCCESSOR:
            names += sorted(state["inherited"])
        for name in names:
            new = name in by_name
            expected_bytes = (by_name[name]["bytes"] if new
                              else state["inherited"][name]["bytes"])
            with anonymous.get(entries[name]["links"]["content"],
                               stream=True, timeout=(20, 90)) as response:
                require(response.status_code == 200,
                        "Anonymous Zenodo download failed: " + name)
                count = 0
                digest = hashlib.sha256()
                md5 = hashlib.md5()
                for block in response.iter_content(1024 * 1024):
                    count += len(block)
                    require(count <= expected_bytes,
                            "Public file exceeds expected size: " + name)
                    digest.update(block)
                    md5.update(block)
            require(count == expected_bytes, "Public file size differs: " + name)
            require(entries[name]["checksum"] == "md5:" + md5.hexdigest(),
                    "Zenodo checksum differs: " + name)
            if new:
                require(digest.hexdigest() == by_name[name]["sha256"],
                        "New public SHA-256 differs: " + name)
            else:
                require("md5:" + md5.hexdigest() ==
                        state["inherited"][name]["checksum"],
                        "Inherited public bytes differ: " + name)
            item = {"name": name, "bytes": count,
                    "sha256": digest.hexdigest(),
                    "url": entries[name]["links"]["content"],
                    "anonymous": True}
            (results if new else inherited_results).append(item)
    receipt = {
        "schema": "openlogic-classical-zenodo-readback-v1",
        "status": "PASS_ANONYMOUS_EXACT_ZENODO_READBACK",
        "record_id": state["draft_id"], "concept": CONCEPT,
        "doi": "10.5281/zenodo." + str(state["draft_id"]),
        "default_preview": PREVIEW,
        "inherited_files_unchanged": len(state["inherited"]),
        "inherited_files": inherited_results,
        "inherited_inventory_checked_without_redundant_download": SUCCESSOR,
        "inherited_inventory": state["inherited"] if SUCCESSOR else None,
        "new_files": results,
    }
    save(STATE_DIR / "ZENODO_READBACK.json", receipt)
    state["status"] = receipt["status"]
    save(state_path, state)
    print(json.dumps({"status": state["status"], "doi": receipt["doi"],
                      "new_files": len(results),
                      "inherited_files": len(inherited_results)}))


if __name__ == "__main__":
    actions = {"prepare": prepare, "publish": publish, "verify": verify}
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=tuple(actions))
    parser.add_argument("--successor-config", type=Path)
    args = parser.parse_args()
    if args.successor_config:
        configure_successor(args.successor_config)
    try:
        actions[args.action]()
    except requests.RequestException as error:
        raise SystemExit(
            "Zenodo transport failed (" + type(error).__name__
            + "); inspect the saved transaction before any bounded retry"
        ) from None
