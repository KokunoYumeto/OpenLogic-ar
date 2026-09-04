# Arabic translation decision and terminology log

## Authority and purpose

Direct user instruction, 2026-09-04: keep translating, including terminology
not located in official Arabic mathematics dictionaries; keep meticulous,
complete records of difficult decisions, the selected Arabic, the motivation,
and opportunities for later expert correction. Expert feedback is optional
revision evidence, never a construction, validation or publication hold.

This applies to the Arabic workstream's existing international/Machrek MSA
readers and the complete classical-style edition. The two MSA profiles share
one terminology inventory. It does not authorize changes to other languages.
The exact source documents, not recollection or a generated summary, control.

## Two linked levels

1. A decision identifies an English term and mathematical sense, chosen
   Arabic realization, source evidence and rationale. Different senses or
   grammatical realizations have different decisions. A repeated choice may
   reference a prior decision; do not duplicate an unexplained verdict.
2. An occurrence maps each applicable unit and exact source/target passage to
   its decision. Keep baseline hashes and occurrence context, since line
   numbers alone become stale. Per-unit coverage lists reviewed decisions,
   explicit no-substantive-term cases and any unfinished coverage.

Batch authors write only their own `terminology_decisions` and
`terminology_coverage` arrays in their existing batch receipts. Retrospective
auditors write separate bounded `retro-XXXX-YYYY.json` files here, never edit
another live worker's batch. Root consolidates them into the versioned
DECISIONS.json register, COVERAGE.json and EXPERT_REVIEW_QUEUE.json. Those
consolidated files are not considered complete until their coverage passes.

## Required decision fields

- `decision_id`: stable unique scope/family/sense key.
- `edition`: `msa`, `classical`, or `shared` with an explanation of reuse.
- `english_term`, `sense`, `chosen_arabic` and `grammatical_realization`.
- `occurrences`: unit id; exact English/MSA/classical source identities as
  applicable; relative file paths; SHA256; line range plus a short exact
  identifying excerpt. Never reproduce an entire protected dictionary entry.
- `rationale`: concrete mathematical and Arabic-linguistic reasons for this
  choice, including distinctions it preserves and rejected ambiguities.
- `authority_checks`: source title/id; edition/date where known; physical and
  printed page or dictionary entry; exact search/query if applicable; result
  `attested`, `related-but-not-exact`, `not-found-in-checked-sources`,
  `not-checked`, or `not-applicable`; evidence path/hash when available.
  Name each consulted source. A general dictionary title is not a citation.
- `alternatives`: forms considered and why retained, rejected or deferred.
- `basis`: `authority-attested`, `inherited-unverified`, `contextual-extension`,
  or `ai-proposed`. Attestation of a similar word is not exact sense evidence.
- `confidence`: high/medium/low, with a specific justification.
- `expert_review_useful`: Boolean, with a reason and a precise question where
  true. Keep records even when false; normal terminology still needs traceability.
- `open_to_correction`: true. No wording is immunized from evidence-led revision.
- `recording_mode`: `contemporaneous` or `retrospective-reconstruction`.
- `status`: `provisional-in-use`, `evidence-supported-in-use`, or `superseded`.
  Preserve replaced decisions through `supersedes`/`superseded_by` links.

Do not invent access to dictionaries or retrospectively invent what an earlier
author thought. Retrospective rationale states what currently justifies
retaining or changing the wording. Clearly label unperformed lookups. Do not
claim a term is absent from all official dictionaries based on a partial search.

## Coverage and finite execution

1. Apply this contract to every active drafting/review batch immediately.
2. Backfill completed classical batches and their corresponding MSA terms,
   then all remaining units, without regenerating already verified prose.
3. Inventory shared terminology macros, definition headings, technical names,
   translation alternatives and prose that describes symbols. A lexical scan
   finds candidates; contextual reading decides sense and completeness.
4. Cross-link inherited terms, classical restyling and grammatical variants;
   require exact evidence for official-attestation claims. Where lookup or
   scholarly evidence is incomplete, retain a reasoned provisional translation
   and add a precise expert-review question.
5. Consolidate deduplicated decisions and occurrence records; deterministically
   validate identifiers, hashes, source locators, coverage, authority statuses,
   provisional markings, expert queue and supersession links. Reconcile all
   722 units, including structural and alphabet/specimen units.
6. Include a human-readable terminology report and machine-readable register,
   coverage and expert queue with the corresponding completed edition release.
   Review availability is not a release gate; truthful coverage and sound
   translation remain required. The log is not a substitute for semantic QA.

Current status: logging requirement is active; exhaustive retrospective coverage
is not yet established. Completed build/PDF receipts remain historical and are
not rewritten to pretend this new log existed at their build time.

## Public review surfaces

- Working register and machine-readable ledgers:
  <https://github.com/KokunoYumeto/OpenLogic-ar/tree/main/evidence/classical/terminology>
- Corrections or supporting citations may be proposed through a repository
  issue or pull request: <https://github.com/KokunoYumeto/OpenLogic-ar/issues/new>
- Stable preservation lineage:
  <https://doi.org/10.5281/zenodo.21921850>

The Zenodo concept DOI resolves to the newest published snapshot. Reviewers
should cite a stable `decision_id`; later snapshots preserve supersession links
instead of silently replacing the historical record.
