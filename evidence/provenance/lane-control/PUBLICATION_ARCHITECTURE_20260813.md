# Language/work publication architecture

Authority date: 2026-08-13. Direct user authority is preserved verbatim in
`RAW_USER_DIRECTIVES_20260813.md`. This receipt applies the canonical method
read from:

`<LOCAL_USER_ROOT>\Documents\interlanguage\methodology\multilingual-publication-datacite-zenodo-github`

## Bound methodology artifacts

| File | SHA-256 |
| --- | --- |
| `00_METHOD_IN_PLAIN_ENGLISH.txt` | `BE55F4A54179E65F03E4CFA47FA2CD9D480E6F8F823AB27B3D17BC402B113073` |
| `01_MAINTAINER_INSTRUCTION.txt` | `1895C0860318977AD37405F55C8ADAB0E36B7E3DBAC39E98B0C09DFDE33893CE` |
| `02_GLOBAL_HUB_LANGUAGE_TABLE_TEMPLATE.tsv` | `0E3DCD7C2E0E3A82687F7B80B9ACC0972562386BECEA4358958827AD654B7FB1` |
| `03_DATACITE_RELATION_SIDECAR_TEMPLATE.json` | `D496EFFC1B6D41CA4C80FA1F6706521FBEB83CFA3384E2B492A564B7E6A097E5` |
| `04_LANGUAGE_RELEASE_TREE_TEMPLATE.txt` | `127F81CA445A0C5C238148BD66A2145F2DC65665A178FE52B2E6992D71B55473` |
| `05_METADATA_CROSSWALK.tsv` | `C693E5D89339E117D69DC0AD4D8A6DB22790BE7CE52AFBF6854D3846AEC7963E` |
| `06_OBJECT_GRANULARITY_RULE.txt` | `52D10E8B4228FEEB7EAF251A4A0177047920F0A4BB588A74FC8D6C4120002343` |

The official-document archive manifest reports 64 downloaded official
documents and SHA-256
`C16656B44BC3BECCDB690793B9E08639371CAB1060A9F02F2BE0747A369009B3`.

## Lane application

- Arabic and Iranian Persian never share a DOI lineage, repository, release
  archive, terminology ledger, evidence claim or version history.
- Open Logic gets one evolving `ar` language concept DOI and one evolving
  `fa-IR` language concept DOI. Exact releases receive immutable version DOIs.
- Before all 722 units close, a release title and reader filename must state
  the exact accepted checkpoint and may not say “complete edition.” Its file
  `00` is one cumulative linked reader containing every accepted unit in that
  locale, not a single-unit PDF. After closure, file `00` becomes the complete
  linked edition.
- Each admitted OpenStax book is its own work object and gets independent
  `ar` and `fa-IR` lineages. A gateway-catalog Collection DOI is optional only
  if an actual maintained aggregation is produced; book lineages are never
  silently widened into the catalog.
- The Stacks Project gets separate complete `ar` and `fa-IR` project-edition
  lineages. The preserved Noether programme gets separate full-corpus `ar` and
  `fa-IR` lineages rather than per-paper DOI proliferation.
- Future SGA/EGA publication follows the user's corpus rule: one language-level
  full-work/corpus DOI lineage, with separately downloadable completed volume
  readers inside that language release; no DOI per internal seminar volume
  merely because the cumulative reader has parts.
- The public surface is deliberately small: `00` reader PDF, `01` editable
  sources ZIP, `02` evidence/provenance ZIP, `03` SHA-256 manifest. The
  provenance ZIP includes raw authority receipts, terminology/adverse ledgers,
  source manifests, build/render/source checks, review limits, correction and
  failure logs, decision trees, current/recovery state and exact hashes. It
  excludes credentials and reproducible cache clutter.
- Each language has a standalone discoverable GitHub publication repository
  with its translation on default `main`, reader and DOI above the fold,
  synchronized `README`, `CITATION.cff`, `.zenodo.json`, release manifest,
  DataCite relation sidecar, source, evidence and deterministic build entry.
  The current branches remain workbenches until that release surface is ready.
- DataCite direction is exact: language `IsTranslationOf` original; original
  `HasTranslation` language; language `IsPartOf` stable global hub; hub
  `HasPart` language; exact release `IsVersionOf` language concept. Until
  Zenodo exposes translation relations, preserve them in description, reader,
  README and the relation sidecar, while using supported `IsPartOf/HasPart`.
- A genuine stable global Open Logic concept DOI would be the directory
  anchor. None has been identified at this checkpoint, so the language records
  preserve a pending relation instead of inventing `IsPartOf`. DOI
  `10.5281/zenodo.20393488` was independently resolved to an unrelated
  mathematics-manuscripts dataset and is explicitly prohibited as an Open
  Logic relation target. Each language record remains directly discoverable
  and gives one-click reader preview/download.
- The latest direct instruction supersedes the earlier archive-maintenance-only
  custody rule for this lane's own language/work DOI lineages. No competing
  global/omnibus record is created or rewritten. Source errors still route to
  the appropriate central source maintainer.

## Release gate and credentials

Publish only an honestly scoped, cumulative, source-checked, independently
replayed, built, rendered and hashed release with unresolved items disclosed.
Human review is optional later evidence, never a release dependency. A DOI is
not minted for every unit or commit.

Authorized credential files may be used only when a verified release is ready:

- `[REDACTED_LOCAL_CREDENTIAL_PATH]`
- `[REDACTED_LOCAL_CREDENTIAL_PATH]`

Their contents may never be printed, logged, committed, copied into an archive,
or sent to another task. As of this receipt they have not been opened by this
lane, and no external repository, DOI, draft or release has yet been created.
