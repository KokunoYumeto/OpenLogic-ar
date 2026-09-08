"""Independent rendered-glyph checks for fences and transformed tableau nodes.

Use the old probe receipt only to locate PDF regions, never as a correctness
oracle. Verify actual PDF bytes and character positions, not link-box order.
The ordinary source pair (A, operator, B) must place A physically right in RTL.
Opening/closing delimiter glyphs must mirror along with their positions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pdfplumber


FENCES = {"round": ("(", ")"), "square": ("[", "]"),
          "brace": ("{", "}"), "angle": ("⟨", "⟩")}
TABLEAUX = {
    "P11-root": ("→", "←"), "P11-left": ("∈", "∋"),
    "P11-right": ("⊆", "⊇"),
    "P16-global-tableau-root": ("⇒", "⇐"),
    "P16-global-tableau-left": ("≺", "≻"),
    "P16-global-tableau-right": ("⊑", "⊒"),
}


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def chars_in_rect(page, rect: list[float]) -> list[dict]:
    x0, y0, x1, y1 = rect
    top, bottom = float(page.height) - y1, float(page.height) - y0
    return [{"text": c["text"], "x": (c["x0"] + c["x1"]) / 2,
             "top": c["top"], "bottom": c["bottom"]}
            for c in page.chars
            if x0 <= (c["x0"] + c["x1"]) / 2 <= x1
            and top <= (c["top"] + c["bottom"]) / 2 <= bottom]


def fence_ok(actual: str, pair: tuple[str, str], role: str, rtl: bool) -> bool:
    index = 0 if role == "open" else 1
    return actual == pair[1 - index if rtl else index]


def tableau_ok(chars: list[dict], operator: str, rtl: bool) -> bool:
    significant = [c for c in chars if not c["text"].isspace()]
    if sorted(c["text"] for c in significant) != sorted(("A", operator, "B")):
        return False
    positions = {c["text"]: c["x"] for c in significant}
    return (positions["A"] > positions[operator] > positions["B"]) if rtl else (
        positions["A"] < positions[operator] < positions["B"])


def audit(receipt_path: Path) -> dict:
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    checks = []
    pdfs = []
    primary = Path(receipt["build_manifests"]["primary"]["path"]).parent
    for job in ("control", "rtl"):
        path = primary / (job + ".pdf")
        recorded = receipt["artifacts"]["primary"][job]
        if digest(path).lower() != recorded["sha256"].lower() or path.stat().st_size != recorded["bytes"]:
            raise ValueError("PDF identity differs from recorded region source")
        pdfs.append({"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)})
        anchors = recorded["geometry_anchors"]
        rtl = job == "rtl"
        with pdfplumber.open(path) as doc:
            for family, pair in FENCES.items():
                for role in ("open", "close"):
                    key = f"P03-{family}-{role}"
                    anchor = anchors[key]
                    chars = chars_in_rect(doc.pages[anchor["page"] - 1], anchor["rect"])
                    actual = "".join(c["text"] for c in chars)
                    expected = pair[(1 if role == "open" else 0) if rtl else (0 if role == "open" else 1)]
                    checks.append({"job": job, "probe": key, "page": anchor["page"],
                                   "check": "inward-facing-delimiter", "observed": actual,
                                   "expected": expected, "pass": fence_ok(actual, pair, role, rtl)})
            for prefix, operators in TABLEAUX.items():
                region = [anchors[prefix + "-" + suffix] for suffix in ("A", "op", "B")]
                if len({item["page"] for item in region}) != 1:
                    raise ValueError("One tableau node spans pages")
                rect = [min(item["rect"][0] for item in region),
                        min(item["rect"][1] for item in region),
                        max(item["rect"][2] for item in region),
                        max(item["rect"][3] for item in region)]
                chars = chars_in_rect(doc.pages[region[0]["page"] - 1], rect)
                operator = operators[1 if rtl else 0]
                checks.append({"job": job, "probe": prefix, "page": region[0]["page"],
                               "check": "operand-order-and-relation-face", "glyphs": chars,
                               "physical_left_to_right": "".join(c["text"] for c in sorted(chars, key=lambda c: c["x"])),
                               "expected_physical_left_to_right": "B" + operator + "A" if rtl else "A" + operator + "B",
                               "pass": tableau_ok(chars, operator, rtl)})
    failures = [c for c in checks if not c["pass"]]
    return {"schema": "openlogic-rtl-visible-semantics-v1",
            "status": "FAIL_RENDERED_SEMANTICS" if failures else "PASS_BOUNDED_RENDERED_SEMANTICS",
            "region_receipt": {"path": str(receipt_path), "sha256": digest(receipt_path)},
            "pdfs": pdfs, "checks": checks, "failures": failures,
            "scope": "Eight P03 fence faces and six P11/P16 tableau nodes in each of two isolated PDFs; not full-reader acceptance.",
            "authority": "https://www.unicode.org/reports/tr9/#L4",
            "authority_use": "Opening/closing glyph mirroring; semantic operand roles come from the exact fixture source.",
            "limitations": ["Sized delimiters, radicals, and other unanchored constructs still require their separate repair/QA.",
                            "This automated check supplements, not replaces, inspection of all rendered pages."]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.receipt.resolve())
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(result["checks"]),
                      "failures": len(result["failures"]), "output": str(args.output)}, ensure_ascii=False))
    return 1 if result["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
