# Arabic / Persianate / RTL recovery logbook

Append-only operational record. A new process must verify referenced artifacts
and hashes; entries are evidence pointers, not substitutes for the artifacts.

## 2026-08-13 — raw-state reconstruction and priority correction

- Directly read all 604 lines of the user-supplied raw-history attachment in
  four bounded chunks; SHA-256
  `4991B9319D0F128F1FB36F6E59718E1696672313474639F34DED62BD248D8F3F`.
- Goal service returned `goal: null`; no active service record existed at that
  check. A new durable objective must be recreated from
  `CURRENT_GOAL_OPENLOGIC_AR_FA_20260813.md`, never from session summary.
- Active priority corrected to complete Open Logic `ar` + `fa-IR`, paired by
  source unit with independent target evidence and prose. OpenStax gateway is
  next; the optional linear-algebra candidate requires exact admission; Stacks
  is preserved for later; Lean is excluded.
- Interrupted the three still-running Stacks subagents before further Stacks
  mutation. No returned unit 0016/0017/0018+ material was admitted. Existing
  accepted Stacks state remains through `STK-CAT-0015`, source line 538/tag
  `001O`; next cursor line 540/tag `001P`.
- Reverified Open Logic official intake locally: commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`; tree
  `f67757bb9305b173634082ab4cefd5601a707a34`; clean status; origin
  `https://github.com/OpenLogicProject/OpenLogic.git`; `LICENSE.md` SHA-256
  `1094A30E124027CB4CFF48D932F1A8673D1386682A475A0EDC811F2162241FEC`.
- Read upstream `locale/LOCALIZATION.md` directly. It requires a distinct
  locale directory/repository and translation of locale strings plus content.
  Arabic and Persian will therefore use separately owned branches/worktrees.
- Located user-visible Turkic task `019ff804-33ab-7f81-a9a5-386e3a8a49f6`.
  Its current state must be inspected before the one user-authorized priority
  message is sent.
- Floris confirmed the ladder explicitly: after the roughly 8,000-page Open
  Logic + OpenStax sequence, resume and continue Stacks. This is continuation,
  not cancellation of the preserved Stacks state.
- Floris supplied paths to GitHub and Zenodo token files. They were not opened
  or copied because current work is local production and archive publication
  remains a separate later handoff.
- Read the Turkic task's recent completed state directly. It had prioritized a
  Turkish Noether Paper 36 checkpoint and small Hefferon work, so the same
  gateway-first correction is materially applicable.
- Sent the user-authorized message successfully to Turkic task
  `019ff804-33ab-7f81-a9a5-386e3a8a49f6`: complete Turkish Open Logic first;
  then exact useful OpenStax gateway books; preserve existing work; do not use
  Turkish as a proxy for other Turkic standards; advanced Stacks comes later.

## 2026-08-13 — Open Logic paired unit OLP-0001 accepted

- Established separate source-derived worktrees and single-writer branches:
  Arabic `codex/openlogic-ar`; Iranian Persian `codex/openlogic-fa-ir`.
  Shared source authority is commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`; complete closure is 722
  tracked TeX units, of which 642 are complete-reader reachable.
- Accepted `OLP-0001`, source `content/open-logic-about.tex`, SHA-256
  `E4F2E2EC5D9957FA71DF41E9ED100641FE08230F63AF6065EAAFCB3D37346F4A`,
  only after both independent targets passed semantic/static/build/visual and
  post-correction independent-AI replay gates.
- Arabic target SHA-256
  `3DFDAB30491A82C494D48ED98D8D1D81F3778C831C934CD3EB9DC94FFAAF400D`;
  accepted commit `7161fb7efa609e88fafb459bddefd06c62b5419d`; one-page PDF SHA-256
  `E347DF3E113ADA31E24880E92572580E11813DE89E204B6E52F7FA35A4B0AE13`.
- Persian target SHA-256
  `2E400AC320BDBCCFAD6EF2A3520E0ABA53BA92D1ABCFB04F202A30CD67908DCD`;
  accepted commit `2b0c05527ed8bd50bf7e93981747a988593f0e2a`; one-page PDF SHA-256
  `D7CE4D015EC6E9C77F856CC4AD3E3358222785C25D50CC0B8D4070AB9DBC815A`.
- Both PDFs are visually sound with localized metadata/outlines and two exact
  links, but neither is claimed tagged or accessibility-certified. Extraction
  can reorder Arabic diacritics/parentheses; Persian extraction drops ZWNJs
  and can reverse combining sequences. Editable TeX is authoritative;
  `human_review=none`; `publication_checkpoint_ready=false`.
- Full paired receipt:
  `03_projects\language_management\arabic_persianate_rtl\03_working_translations\openlogic\00_control\QA_RECEIPT_OLP_0001.md`.
  Receipt SHA-256 after commit binding:
  `A25355B960284510D9CD742C54861A9E62A4D4D7181891576E47F28A12AAE2F5`.
- Shared cursor advanced to `OLP-0002`, `content/content.tex`, SHA-256
  `B42CD7F4BFD4185CCDA7F834A706973A728B2126498C873671924A77B4D8F1D6`.
  Separate Arabic and Persian targets subsequently passed source/static,
  semantic, and independent-AI QA and were accepted at commits
  `5d25584e4ee0940d79536405b252c0d5c8504eda` and
  `4ff0419acfa81b4354ea4150a92e5ec7d628cea3`. A build was deliberately not
  run because this corpus root would import 18 untranslated dependencies and
  create hidden English fallback; the build gate is deferred to dependency
  closure. Receipt `openlogic\00_control\QA_RECEIPT_OLP_0002.md`, SHA-256
  `001CD6CD76E4076F1CC8A4342FD4786697EB9E13176C5FE24A51B73A76F2F9EC`.
- Current shared cursor is `OLP-0003`,
  `content/sets-functions-relations/sets-functions-relations-complete.tex`,
  source SHA-256
  `03E55D8EE2EC4586A5DC8B64E6FA59950C46DA3CDEE54267946015E7BBD989ED`;
  next cursor after paired acceptance is `OLP-0004`.

## 2026-08-13 — Open Logic paired units OLP-0003 through OLP-0005 accepted

- Accepted `OLP-0003` (naïve-set-theory part driver), source SHA-256
  `03E55D8EE2EC4586A5DC8B64E6FA59950C46DA3CDEE54267946015E7BBD989ED`.
  Arabic target/commit:
  `467A6906D5C46FEBFC3EC1538CD0907EEB7D68FBECE16A4F4BE6452E834F6527` /
  `ab714f4f17b29852d88d3d3ecac0d9094dfaa25f`. Persian target/commit:
  `9B7FE5D8B6438191BF45FEAEC8D7D3367CEA80A412C6653065846758C326A41D` /
  `8dd95bee62e85053f625420ad2e8afb7ea2b371e`. Paired receipt SHA-256:
  `673A2FE7874E543B22DFB6DE48F883F98F9539184357BDA7EB07553131221235`.
- Accepted `OLP-0004` (Sets chapter driver), source SHA-256
  `EEA34D38BB52811468A0025D348457A0F4D3F44AAE4B7CABB28551D6328E2785`.
  Arabic target/commit:
  `B1C50900475E2F94BF13435C7A5069F6BC6820C7F8D2D3B5C49321E521088ECF` /
  `4ceee0dd4d1486d9932261658e3152da0a63136a`. Persian target/commit:
  `DF9B514CCED39A35FA88B65A53659B7207D7E899F8B48CF08066E611752850C9` /
  `a48b835c374a56fa722ef0b33391f029cca2f7c4`. Paired receipt SHA-256:
  `86DB82E0C18BFC968ECE9B44011105ADEC9D02D6FBACFFE93256D76DEFB57678`.
- Units 0003 and 0004 passed source/semantic/structure/independent-AI gates.
  Their builds remain deliberately deferred because their reader imports are
  not closed; no hidden English fallback was generated.
- Accepted `OLP-0005`, Extensionality, source SHA-256
  `8BC9151AF0985E6E20C374AA38CDDD1ADD7A8DFFBABCCC94B89F324F62C40F8C`.
  Arabic target/commit:
  `1175854930480BAFE2EAA2853E068665C083589A4BAF03ACBF55E781FF3E013F` /
  `e9b739f5dd77ff18b3cb47924c6f168bb8a1e2e1`. Persian target/commit:
  `129320E9EEA66762B41C28C6970DBAC6A87D84433AEC529A18BDE8AE903F849C` /
  `bd069c68afbe5e6793ae3868f50763491400aa4b`.
- OLP-0005 passed exact 91-command / 20-environment / 14-token / 52-math
  replay and direct independent semantic review. Upstream localization rules
  are honored with `\olfileid[ar]{sfr}{set}{bas}` and
  `\olfileid[fa-IR]{sfr}{set}{bas}`. The source's “less than 10” versus
  displayed `0 \leq x \leq 10` inconsistency is preserved and adverse-ledgered.
- OLP-0005 clean two-pass PDFs: Arabic one page / 101,398 bytes / SHA-256
  `16A2BABF64BBCF5828AEAF6B25FA385A9CB270F7B5DBA4BDBC6836BA8E205F6C`;
  Persian one page / 99,043 bytes / SHA-256
  `D6A1B72BC058E8B8B3A33CF6337E53B0128B4D63A6D4AA32520B18216BB49FD9`.
  Every page was rendered at 144 dpi and inspected; render witnesses are
  `D26340E9B90744A328716CFF4106BE2AAAC1843C82E55E9FC119630E9BDE2B57`
  and `E360255AF7C66088D7B87D20F66B3F31B78D1CAF85747758E7850A56335657F4`.
- Both PDFs have correct locale `/Lang`, title, author and outline; zero
  U+FFFD and zero Arabic Presentation Forms in Poppler extraction. They are
  not tagged/accessibility certified. Arabic mark/punctuation order can vary;
  Persian extraction drops 67 source ZWNJs. Editable TeX is authoritative;
  `human_review=none`.
- First Persian build exposed an incompatibility between upstream non-reader
  debug margin notes and bidi page-number data; the release/QA wrappers now
  omit that diagnostic package. Arabic About metadata was moved from global
  locale config to its own driver so later units cannot inherit the wrong
  title. OLP-0001 Arabic was rebuilt: PDF SHA-256
  `A62B8FD0B5C4AFC94FE7F17E9B7BE46559AB818DCC9559B5A47D10D3547D5456`;
  visual and extraction witnesses stayed byte-identical.
- The current OLP-0001 paired receipt now has SHA-256
  `BF36FE1789EA85F8473E33F7F6D038232CA9157F8E46BF1BD98F394AB7E4CFEB`;
  earlier OLP-0001 receipt/PDF hashes above remain historical witnesses.
- Paired OLP-0005 receipt:
  `03_projects\language_management\arabic_persianate_rtl\03_working_translations\openlogic\00_control\QA_RECEIPT_OLP_0005.md`,
  SHA-256
  `119F9041A0B4BAD94B73F860B2374F3502326B916F95D33096452C8F829E5977`.
- Next exact shared cursor is `OLP-0006`,
  `content/sets-functions-relations/sets/subsets.tex`, SHA-256
  `5D982F62C40325CF75DA4517ADD45CA073E23FB9463CFB3ADFB9AAFBB8582E46`;
  cursor after paired acceptance is `OLP-0007`.
- Post-admission controls: closure manifest
  `24E186D7B4AE4AA0577E57F821D261384440A7EC2F25C6E7BDAB0CDAF1B06D10`;
  current state
  `304318AA97E10AABD8DAC08CC78CBCE0A2C939678C91ABDE1AA3BF3E6D753878`;
  source-release record
  `74CACA8E5E1D62B3177EEB60DCD3E29B0D75B4873A63A3871E612BA9F0219A0F`;
  branch ownership
  `8928D606E0A905612E162E11C428CFDC7F46C489BD43C7E3EF559B3FB284BB48`;
  unit ledger
  `33B5702F9401315D8EA9B21D8DFA9E503A2734700F5E24AD6B2E7D11884E957D`.

## 2026-08-13 — Open Logic paired unit OLP-0006 accepted

- Accepted `OLP-0006`, Subsets and Power Sets, source
  `content/sets-functions-relations/sets/subsets.tex`, SHA-256
  `5D982F62C40325CF75DA4517ADD45CA073E23FB9463CFB3ADFB9AAFBB8582E46`.
  A prior 63-character transcription in several live controls omitted one
  `B`; direct source hashing and the intact closure-manifest value resolved
  the locator before admission.
- Arabic target/commit:
  `1DC4A005B7F44CDFC46DBF485626BF76551EECBB108C7F822F41A2DF8A883AE5` /
  `b0aac1d674eb68036b0f3691e5888742c64a754d`. Persian target/commit:
  `B8755941AFB97FC801C6FF9F03B54522AE64AC4D321DF207D77C1CE85AC1B4F4` /
  `9913a32aa6383a82542e9e06a88cbb9e352f5caa`.
- Both targets passed exact 137-command / 22-environment / 14-token /
  65-math-segment replay and independent direct semantic review. The Arabic
  first build had one 0.72131pt overfull line; an equivalent shorter MSA
  question removed it without changing content. The Persian first render
  displayed stable Latin counters as `1.set`; the committed wrapper isolates
  each complete counter with `\babelsublr`, and independent delta replay
  confirmed visually invariant `set.1` order with the target hash unchanged.
- Clean final one-page PDFs: Arabic 98,662 bytes / SHA-256
  `D741C747D0EDEC7F11CAB964E60E26CB879B32629E7CAC7C53A0AB44E3043750`;
  Persian 97,145 bytes / SHA-256
  `43F48D1014ADD993170439E43ECF10D83E2C3DEAC3ABFD72F4405FEFC3BC76D6`.
  Every page was rendered at 144 dpi and inspected; witnesses are
  `904E254718C09F95B3F3B767DF230DCD13E7866A180A56C0625CA8336B4C8C20`
  and `9836AAC16953DB4FA263ECCE047DDEF01DB028B7E901FC513D51015A9E6AEDCC`.
- Extraction has zero U+FFFD and zero Presentation Forms in both PDFs. Both
  remain untagged and not accessibility-certified; Persian Poppler extraction
  drops all 36 source ZWNJs and can serialize visually correct counters in
  reverse order. Editable TeX is authoritative; `human_review=none`.
- Paired receipt `openlogic\00_control\QA_RECEIPT_OLP_0006.md`, SHA-256
  `42370905D5C0640D48D3D18EF2A96F172DE2C218D3C54E496E67C577E296CFCB`.
  The corrected OLP-0005 paired receipt now hashes to
  `CBE9022460D7F6147482B4EE53DEFD1C3C9C4DE9B50D628415A6F49547C5BEC3`.
- Post-admission controls: closure manifest
  `82139C511BB636868459192654588E9D3B45AA0170518C71ABAC7410292394E3`;
  current state
  `EDC243F16D4CE3017AFAD4086884127027AB8DB931EDD6FC54714002D1384607`;
  source-release record
  `AB231EE44024A4CBCECC5755813F90B2508A830251982FB759D1D60295241E8C`;
  branch ownership
  `BFE0B8DB69B44712137F6C1A3EC09AE8EB3FED5C226F1A4E4BDB952B06271AF5`;
  unit ledger
  `755938BA95D29DDB272AD368785D79C15189A52291351E14FF7BB942A922CA6F`.
- Shared cursor advanced to `OLP-0007`,
  `content/sets-functions-relations/sets/important-sets.tex`, SHA-256
  `B1B998CAD3FA5AEF48670F755245F86EFE00B239D332A50E764147602405FB32`;
  Arabic and Persian writers started independently from the pinned English
  source. No Lean work and no publication/token access occurred.

## 2026-08-13 — Open Logic paired unit OLP-0007 accepted

- Accepted `OLP-0007`, Some Important Sets, source SHA-256
  `B1B998CAD3FA5AEF48670F755245F86EFE00B239D332A50E764147602405FB32`.
- Arabic target/commit:
  `C9A36E2DBBD89674A4F13784EC149DD93EF2F94881B67AAC62D38FF028C9A3EF` /
  `85f417cbf48fa51b89a2ad8946c03967a5998a93`. Persian target/commit:
  `CDC437750FE229D26DB7E8FD8651350549906375B0AF744B4058AF1B4EAF9F84` /
  `255638bc6cfca482b181cb1027f86f3000dcc5ce`.
- Both targets passed exact 95-command / 14-environment / four-token /
  26-math-segment replay and independent semantic review. Persian was corrected
  before admission to remove an unintended non-emptiness implication.
- Clean final one-page PDFs: Arabic 112,770 bytes / SHA-256
  `C0E896E10123AE76078A8B3147F6EC2D2822D32DBCA6127BE1F1D0138AF0AC62`;
  Persian 110,800 bytes / SHA-256
  `E9261EC31F6CB9C12D1C1C746FA27EA65EC9BCEE66039E729CAB0EB70A373D6D`.
  All pages passed full-resolution visual replay. Extraction has zero U+FFFD
  and zero Presentation Forms, but the PDFs remain untagged and
  non-accessibility-certified; `human_review=none`.
- Paired receipt SHA-256:
  `91DB7C0A19299AB47F6FBC5A5D26EE560FC4C67C8B52BC5F0A050CAC1923084D`.
  Post-admission control hashes: manifest
  `F5B31A2A68A7D87519F3F3DBFF94B273A4795AB680D80223DB577C90D4388E9A`;
  state `20760C50B62297C1F890E8E97676A15F6394B7CBC8423A8AC4301B4D56979CC4`;
  source release
  `26BA235046E98FF742B97D005A74D6E2C94765897158887783B77146AB26D6EB`;
  ownership `1FDA8882167DBAAFFF56D3CD052249876C90234C2B199A2D0C62483FAA75B5B1`;
  unit ledger
  `0D8306B2AA16C02B039E272424F9A03CFFABA09EB5E78AADC8597F41C405449B`.
- Shared cursor advanced to `OLP-0008`,
  `content/sets-functions-relations/sets/unions-and-intersections.tex`,
  SHA-256
  `2AD0EEC70308CEEFF2A4158B2DEE60E59A9B1CF9268FC95C4BB1DA05F65AD60D`.
  No Lean work, publication, upload or credential access occurred.

## 2026-08-13 — Open Logic paired unit OLP-0008 accepted

- Accepted `OLP-0008`, Unions and Intersections, source
  `content/sets-functions-relations/sets/unions-and-intersections.tex`,
  SHA-256
  `2AD0EEC70308CEEFF2A4158B2DEE60E59A9B1CF9268FC95C4BB1DA05F65AD60D`.
- Arabic target/commit:
  `112BCA7B160608FE147114AE1BEE0EB4E18406B0BF9D312A705B8FA2D62D2025` /
  `949b35a5032397fc6efedf9c1e0f51fc439a3994`. Persian target/commit:
  `1015C403DB83903E04890FE7CB9B28ABF3AC2E2A4A32E652BCE62224C0A1EAD5` /
  `82f2b7e043df973c68fb79d78d6746b8ae1f743e`.
- Both targets passed exact 213-command / 46-environment / 27-token /
  72-math-segment replay and independent semantic review. Persian was repaired
  before admission to restore one omitted Open Logic text token. The source's
  unrestricted arbitrary-intersection definition was preserved exactly; no
  nonempty-family hypothesis was added.
- Clean final three-page PDFs: Arabic 134,996 bytes / SHA-256
  `324922ECA3469F4094C869ED877C3C95A22A5CEE813E9FAAE583CF167A6E5D05`;
  Persian 134,566 bytes / SHA-256
  `23E5E6E25A1040449632A1F7644BCC6769FA104785BBB5346E940C4C4B3DD2CC`.
  Every page and all three diagrams passed 180-dpi visual replay. The locale
  layers now render the external section name in Arabic/Persian, and hyperlink
  inspection verifies one remote OLP-0005 action plus three internal figure
  actions per locale.
- Extraction has zero U+FFFD and zero Presentation Forms in both PDFs. Both
  remain untagged and not accessibility-certified; Persian extraction drops
  all 57 source ZWNJs. Editable TeX is authoritative; `human_review=none`.
- Paired receipt SHA-256:
  `C91C7BD366DB30BA10919FD32C4C2F164DC9C2F0733343AAD0DE9EA9B2E55B1A`.
  Post-admission control hashes: manifest
  `5E64079274B7782F5C8591F1EB422699D1265459F62738B650B11400BEEC8465`;
  state `1020647EF864D887C5BAF16125817FB99FAB5A01B15117E04EC4F508CB5E14D1`;
  source release
  `0E6F54F6AD5709BD94D5481F800EDC25C00102C30A0D6D2AF37F997263EC1279`;
  ownership `D04857249F941B30AF6342431080BCF668E14AC3B89EF8E1BD17DFEF65E4D00C`;
  unit ledger
  `A4F66CBE73D10B21A8C81E153BCC44929DE3D19A800494B58B347D0B93600926`.
- Shared cursor advanced to `OLP-0009`,
  `content/sets-functions-relations/sets/pairs-and-products.tex`, SHA-256
  `3DB7F0241D387B49488F70E78062C24192B813873618F761565D97BD7249431C`.
  No Lean work, publication, upload or credential access occurred.

## 2026-08-13 — Open Logic paired unit OLP-0009 accepted

- Accepted `OLP-0009`, Pairs, Tuples, Cartesian Products, source
  `content/sets-functions-relations/sets/pairs-and-products.tex`, SHA-256
  `3DB7F0241D387B49488F70E78062C24192B813873618F761565D97BD7249431C`.
- Arabic target/commit:
  `0209ACCAD5BA65DA9955892285D637EC9B4DA5B98D8C7830695BE6F8161B6809` /
  `d0c5df46857ed209376dc4b08f1c18e066394e0b`. Persian target/commit:
  `9474699C22D159D4F715B48E49B727E9BEAD8AE93F3BEBBD62C1CBD186C92BC5` /
  `019a8c592ce5797e7f73e277d42871487327d1de`.
- Both targets passed exact 177-command / 30-environment / 12-token /
  78-math-segment replay and independent semantic review. The source's
  same-coordinate disjointness notation, implicit product-grid enumeration,
  broad sequence wording and `\emptyset` empty-sequence convention were
  preserved and documented rather than silently repaired.
- Clean final two-page PDFs: Arabic 135,231 bytes / SHA-256
  `EA09C95D64030EE95C6210B21546C602F9F7A93DBB641168689EE80C8A637030`;
  Persian 133,844 bytes / SHA-256
  `94D935230548E75B1E411C12FA24A4154F22DA923A96CC42743F84A3D705F4FB`.
  All four pages passed 180-dpi visual replay; the internal definition link
  resolves in each PDF.
- Poppler extraction has zero U+FFFD and zero Presentation Forms. The PDFs
  remain untagged and not accessibility-certified; Persian extraction drops
  57 source ZWNJs, pypdf emits two U+FFFD characters for Arabic, and copied
  mathematics is imperfect. Editable TeX is authoritative;
  `human_review=none`.
- Paired receipt SHA-256:
  `099E42C88AEE7F171AAE62D1E723C200995C6CFD6E7B9EFA245BB348D1215838`.
  Post-admission control hashes: manifest
  `B8E2CA11AB8F239F4197A2417C423BEC07DD3C4B01D91475BD6B2F61F5BC1F53`;
  state `E6B1F9BE08A832A337AFCE75AE5C7ACF1EEA5CA0BABD3EDCB045B432D992025E`;
  source release
  `683540E45E424FF584B4E034C60FD99BBB2B3B1BB37EE799CE4B9167F44EA0D2`;
  ownership `A79B7527631C1E33526538801B9B4EF3740A433C7AC1C8F70F2F0C900C34D003`;
  unit ledger
  `557E2249B991763CCF992F4A162056F71947F821C3D5BFA03BCD7501401E676E`.
- Shared cursor advanced to `OLP-0010`,
  `content/sets-functions-relations/sets/russells-paradox.tex`, SHA-256
  `9A76315CD0D9CF89D27E90A9B87138B1C95AEA98E0D26DE3FE12D897B8C4D10D`.
  No Lean work, publication, upload or credential access occurred.

## 2026-08-13 — language/work DOI publication ownership adopted

- Direct user authority assigned each language maintainer an independent DOI
  lineage per honestly declared author/work/corpus object, a discoverable
  language publication repository, a reader-first public surface and complete
  translation/typesetting/provenance decision archives. The raw message and
  linked task ID are preserved in `RAW_USER_DIRECTIVES_20260813.md`.
- Read all eight current top-level artifacts in
  `methodology\multilingual-publication-datacite-zenodo-github`. The canonical
  method SHA-256 is
  `BE55F4A54179E65F03E4CFA47FA2CD9D480E6F8F823AB27B3D17BC402B113073`;
  the remaining artifact hashes and lane-specific application are bound in
  `PUBLICATION_ARCHITECTURE_20260813.md`.
- Open Logic will have separate `ar` and `fa-IR` concept-DOI lineages and
  standalone publication repositories. Before 722-unit closure, any released
  checkpoint must front one cumulative linked reader for the exact accepted
  scope and must not claim a complete edition. Editable sources, every durable
  decision/provenance/logbook artifact, QA/build/render evidence and hashes are
  bundled behind the reader in small numbered archives.
- OpenStax uses separate work-level lineages per book and language; Stacks uses
  separate project-edition lineages; Noether uses separate complete author-
  corpus lineages. Arabic and Persian never share release state.
- This supersedes the earlier archive-maintenance-only custody rule for the
  lane's own language/work lineages but not the prohibition on competing with
  the global hub or another language. Credential paths are recorded only by
  path; contents remain unopened and unlogged. No DOI, GitHub repository,
  Zenodo draft, upload or public release was created in this event.
