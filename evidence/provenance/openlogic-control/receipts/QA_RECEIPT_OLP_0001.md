# Paired acceptance receipt — OLP-0001

Acceptance date: 2026-08-13. This receipt advances the shared accepted cursor
from `OLP-0001` to `OLP-0002`; it does not claim completion of either edition.

## Authority and scope

- Official source repository: `https://github.com/OpenLogicProject/OpenLogic.git`.
- Pinned commit: `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- Unit/path: `OLP-0001`, `content/open-logic-about.tex`.
- Source SHA-256: `E4F2E2EC5D9957FA71DF41E9ED100641FE08230F63AF6065EAAFCB3D37346F4A`.
- Closure: 722 tracked TeX units; this receipt accepts one paired scheduling unit.
- The upstream `LICENSE.md` is unmodified in both target worktrees at admission.

## Arabic (`ar`)

- Target: `ar/locale/ar/content/open-logic-about.tex`.
- Accepted branch commit: `7161fb7efa609e88fafb459bddefd06c62b5419d` (`codex/openlogic-ar`).
- Target SHA-256: `3DFDAB30491A82C494D48ED98D8D1D81F3778C831C934CD3EB9DC94FFAAF400D`.
- Attribution SHA-256: `23DBFD067F3EC83DD4442E90C743EBFC9E47A302D2AA5A6ACBE4076300E1260B`.
- Locale/config/driver SHA-256: `7F1B34A57BD396F63218DF69E6E879D5E931CB9D883B4A9C65B607D152D9FBAB` / `744C2E9590E24E91D22FF31E825CC3D9575FDEC307B95069FF6E86DCB6B90BC2` / `0480F9696EC067E93732DA80FACBDDB20A205B2AE410B3B84A9AE4C7ED90EB82`.
- Build/QA receipt SHA-256: `7EB97830CC9A94C6CCEEFB1264D8448E186C6B555AACC030D3145AF65B07A89F`.
- PDF: `ar/locale/ar/output/pdf/open-logic-olp0001-ar.pdf`, one page, 51,534 bytes, SHA-256 `A62B8FD0B5C4AFC94FE7F17E9B7BE46559AB818DCC9559B5A47D10D3547D5456`.
- Two-pass log SHA-256: `D6EE04F0E744FB04838B6898C590BB6F28E4E1D3E1FFE0666310B7E5813BA511`.
- Saved extraction SHA-256: `A242EA1F98A47C17993D987575BF438D14026258C17FF1C5FA0A0A693AE39374`.

## Iranian Persian (`fa-IR`)

- Target: `fa-IR/locale/fa-IR/content/open-logic-about.tex`.
- Accepted branch commit: `2b0c05527ed8bd50bf7e93981747a988593f0e2a` (`codex/openlogic-fa-ir`).
- Target SHA-256: `2E400AC320BDBCCFAD6EF2A3520E0ABA53BA92D1ABCFB04F202A30CD67908DCD`.
- Attribution SHA-256: `FBBDBDE530C71484D6ED49B2EF05A496BE60D8937BEBEEE55680876580F832D6`.
- Locale/config/driver SHA-256: `0AAF1CA41D3CAA6E6CC53AA3DEA75251E65428290FF9613209ABF9D92F7A49A3` / `DF8A82CE6D3DCE9E9BA1621D03E52B2FBDEFABE4F34FC290F9A531E92678A85B` / `29EB420105DD253FD66CF6E1A7C94A7D3DC52E24C14D43AF287962643C5ECD9F`.
- Build/QA receipt SHA-256: `EB5878DCD87BDC6E64F1167726C2E33BE5F8459CD71E875CF8D8481E7D4D0B6B`.
- PDF: `fa-IR/locale/fa-IR/output/pdf/open-logic-olp0001-fa-IR.pdf`, one page, 48,535 bytes, SHA-256 `D7CE4D015EC6E9C77F856CC4AD3E3358222785C25D50CC0B8D4070AB9DBC815A`.
- Two-pass log SHA-256: `BBEBCE26119B55DB2691495015BF964BC4FDA90A15015B451E2FE7DCE5F9BFCA`.
- Saved extraction SHA-256: `C007AC4524A4834614815267973EEC321BD436C73C51DC4ED341BA06468F68FB`.

## Gate result and caveat

Both targets pass exact source identity, nine-proposition semantic replay,
command/URL/locale parity, script-residual checks, two-pass builds, localized
metadata/outlines, exact link annotations, complete-page visual inspection,
and independent post-correction AI replay. `human_review=none` for both.

The PDFs are visually sound but are not tagged-PDF or accessibility certified.
Extraction can reorder Arabic diacritics/parentheses; Persian extraction loses
all 23 source ZWNJs and can reverse combining sequences. Editable TeX is the
authoritative target. `publication_checkpoint_ready=false` because this is
only unit 1 of 722 and no complete reader edition exists yet.
