# Open Logic Arabic and Iranian-Persian production control

This directory controls two separate complete target editions at one immutable
source release. The Arabic and Persian worktrees are independent Git branches
sharing only the owned bare source repository and source identities.

The 722-unit closure and stable order are whole-corpus controls. `OLP-0001` is
the first scheduling unit, not the product boundary. The shared accepted cursor
advances only when both target units have passed their stated checks. One
language may be repaired independently without overwriting or certifying the
other.

The existing Bahasa Indonesia edition is a separate owner. Its manifest and QA
scripts supplied useful source-closure and localization-method evidence, but no
Indonesian prose, terminology, target hash or review claim enters either target.

The current shared cursor is recorded in `CURRENT_STATE.json`. At the present
checkpoint, `OLP-0001` through `OLP-0010` are accepted in both branches and
`OLP-0011` is next. The paired receipts bind source, target, commit and review
evidence; units 0001 and 0005–0010 additionally bind isolated build, PDF,
extraction and complete-page visual evidence. Generated PDFs and full logs are
intentionally kept as local ignored build artifacts under each locale's
`output/` tree; they are not silently implied by Git commits and must be
verified by their hashes.
