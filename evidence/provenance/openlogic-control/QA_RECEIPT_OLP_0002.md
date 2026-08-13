# Paired acceptance receipt — OLP-0002

Acceptance date: 2026-08-13. This receipt advances the shared accepted cursor
from `OLP-0002` to `OLP-0003`; it does not claim completion of either edition.

## Authority and source structure

- Official source commit: `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- Unit/path: `OLP-0002`, `content/content.tex`.
- Source SHA-256: `B42CD7F4BFD4185CCDA7F834A706973A728B2126498C873671924A77B4D8F1D6`.
- Role: complete-corpus root containing three editorial paragraphs, two links,
  and 18 ordered `\olimport` edges.

## Arabic (`ar`)

- Target SHA-256: `DDA783A7080EC20C151515B194FA20185E638885CA26424859B6A35F773A5193`.
- Terminology ledger SHA-256: `F977AE8B17B310CBC61456DBD690A268FB6212FB7A1994B45046E3464F031237`.
- Accepted branch commit: `5d25584e4ee0940d79536405b252c0d5c8504eda`.

## Iranian Persian (`fa-IR`)

- Target SHA-256: `8D9F043FC6A265C43981E51DDA87594D60A33C796FB2A613DFAAE4AF7A117636`.
- Terminology ledger SHA-256: `6430090C879C3A5B7346FAC0F97E218C9DDD2A9EED72F64DDA2FE2A7FBEF6E31`.
- Accepted branch commit: `4ff0419acfa81b4354ea4150a92e5ec7d628cea3`.

## Gate result

Both targets pass independent semantic replay of every source claim: raw
compilation is unsuitable for teaching/study; output is customizable; default
logic operators are primitive and all cases are shown; some cases should be
exercises; the project is unfinished and admits drafts/missing exercises;
course PDFs exclude those sections; and sample-course, sample-driver, and
derived-textbook routes remain. Both render the malformed source phrase
`can be generate` according to its intended meaning and record the erratum.

Static parity passes for the exact document class, environment sequence,
`\clearpage`, `\emph`, two ordered URLs, all 18 import arguments/order, three
paragraphs, braces, NFC, script separation, and absence of embedded bidi or
presentation-form characters. Each terminology ledger is append-only with
seven unit-specific decisions. Independent AI QA found no required correction.
`human_review=none`.

## Build state and honest limit

`build_not_run=dependency_closure`. Compiling this corpus-root unit now would
follow all 18 imports into untranslated downstream source and produce hidden
English fallback. No such misleading build was admitted. Its build gate remains
open until the imported target closure exists. There is no OLP-0002 PDF and no
publication checkpoint.

