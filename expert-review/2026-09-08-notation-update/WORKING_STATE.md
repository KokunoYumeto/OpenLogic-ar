# Current Arabic work and limitations

This preservation update adds the latest notation sources, occurrence ledger, tests and findings to the previously published integrated translation review. The earlier review and all reader files remain available unchanged.

## Completed in this update

- Generated mathematical letters and numerals retain the original TeX single-token argument boundaries, including the distinction between `x_12` and `x_{12}`.
- Native mathematical fonts now honor requested normal, script and nested-script sizes. The control and RTL specimen passed measured script-position and font-size checks.
- Diagram identifiers, coordinates and dimensions remain unchanged; explicitly printed formulas inside diagrams and text containers receive notation conversion.
- All 722 presentation units were regenerated and reconstructed exactly back to their canonical sources. There are zero untreated candidates and zero failed inverses. Canonical English and Arabic wording did not change in this pass.

These are bounded source and notation checks, not acceptance of the complete reader. The machine-readable materialization receipt's release-eligibility field applies only to its notation transform, not to the unfinished book.

## Still unfinished

The complete Classical build advanced beyond the earlier subscript error but stopped in a graph example. The diagram-source correction then compiled in an exact small specimen, which exposed misplaced RTL node labels. A first isolated direction candidate compiled but failed the same geometry test; a second stopped at a fail-closed PGF patch-site check before geometry could be tested. Neither candidate is installed as an accepted production fix.

RTL root signs also need their radical faces reflected correctly. These are concrete rendering defects under investigation. No failed, partial or unverified Classical PDF is offered as a completed reader.

The full Classical build, visual checks, deterministic replay, final page-location binding and exhaustive canon-grounded translation audit remain to be completed. The two existing reader PDFs have not yet been regenerated with every newer source correction. Further substantive accepted improvements will be consolidated and mirrored in the same public lineages.

## How to read the evidence

The [technical supplement](source-snapshot/repo/evidence/classical/TYPED_NOTATION_REPAIRS_20260908.md) gives the affected places, decisions, reasons and remaining uncertainties. Its notation ledger records each occurrence and reversible replacement. Historical failed checks are preserved as failures, not relabelled as successful visual acceptance.

The new ZIP is an additive offline supplement. The full translation register and canonical sources remain in the inherited `OPENLOGIC_ARABIC_INTEGRATED_REVIEW_AND_WORK_20260908.zip`, available in the same Zenodo record. For offline reading, extract the new ZIP into a chosen folder; it creates `expert-review/2026-09-08-notation-update/`. Extract the contents of the inherited ZIP specifically into `expert-review/2026-09-08-integrated-review/` under that same chosen folder. This gives the two sibling folders needed by the links. Alternatively, use the GitHub links for immediate online reading.

[Start here](START_HERE.md) · [Full recorded list](FULL_LIST.md).
