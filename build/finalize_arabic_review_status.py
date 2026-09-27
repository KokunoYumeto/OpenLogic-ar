#!/usr/bin/env python3
"""Replace obsolete prepublication status text without changing review cards."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "expert-review/2026-09-26-final-page-review"
FINAL_LINE = (
    "هذه الدفعة جزء من [الدليل العربي الكامل](../DIRECTORY_AR.md)، "
    "الذي يضم الآن ١٠٩٥ قرارًا من ١٠٩٥ قرارًا مخصصًا للمراجعة البشرية. "
    "الأعداد المرحلية القديمة تخص وقت إعداد الدفعة، لا حالة النشر الحالية."
)
OLD31 = (
    "هذه دفعة عمل محلية لم تُنشر بعد؛ والفهرس الكامل ذو ١٠٩٥ قرارًا لم يكتمل تعريبه."
)
NEW31 = (
    "أُعدت هذه البطاقات الثماني في دفعة سابقة، وهي الآن جزء من "
    "[الدليل العربي الكامل](DIRECTORY_AR.md) ذي ١٠٩٥ قرارًا من ١٠٩٥."
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> None:
    changes = []
    for path in sorted(BASE.glob("arabic-*/README.md")):
        before = path.read_bytes()
        text = before.decode("utf-8")
        if path.parent.name == "arabic-existing":
            old = "والقائمة العربية الكاملة ما زالت قيد التحرير."
            assert text.count(old) == 1
            new = "وقد اكتملت الآن [القائمة العربية الشاملة](../DIRECTORY_AR.md)."
            result = text.replace(old, new)
        else:
            lines = text.splitlines(keepends=True)
            matched = [i for i, line in enumerate(lines)
                       if "لم تُنشر بعد" in line or "لم تُنشر بعد" in line.replace("ولم", "لم")]
            if not matched:
                continue
            assert len(matched) == 1, path
            i = matched[0]
            assert "التغطية" in lines[i] or "القائمة العامة" in lines[i], path
            ending = "\r\n" if lines[i].endswith("\r\n") else "\n"
            lines[i] = FINAL_LINE + ending
            result = "".join(lines)
        assert result != text
        path.write_text(result, encoding="utf-8", newline="")
        changes.append({"path": path.relative_to(ROOT).as_posix(),
                        "original_sha256": sha(before),
                        "final_sha256": sha(path.read_bytes())})
    assert len(changes) >= 40, len(changes)
    batch = BASE / "BATCH_31_38_AR.md"
    previous = batch.read_bytes()
    historical = json.loads((BASE / "BATCH_31_38_READBACK.json").read_text(encoding="utf-8"))
    assert sha(previous) == historical["markdown_sha256"]
    content = previous.decode("utf-8")
    assert content.count(OLD31) == 1
    batch.write_text(content.replace(OLD31, NEW31), encoding="utf-8", newline="\n")
    changes.append({"path": batch.relative_to(ROOT).as_posix(),
                    "original_sha256": sha(previous), "final_sha256": sha(batch.read_bytes()),
                    "exact_replacement_only": [OLD31, NEW31]})
    receipt = {"status": "PASS_STATUS_ONLY_FINALIZATION", "changed_files": changes,
               "count": len(changes), "card_bodies_untouched": True}
    (BASE / "PUBLICATION_STATUS_READBACK.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": receipt["status"], "count": len(changes)}, ensure_ascii=True))


if __name__ == "__main__":
    main()
