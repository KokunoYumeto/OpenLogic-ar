# Attribution and changes

## Source

- Work: *The Open Logic Text*, Open Logic Project.
- Source repository: <https://github.com/OpenLogicProject/OpenLogic>
- Project website: <http://openlogicproject.org/>
- Source authority used for this translation: Git commit `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- Translated unit: `content/open-logic-about.tex`.
- Source SHA-256: `E4F2E2EC5D9957FA71DF41E9ED100641FE08230F63AF6065EAAFCB3D37346F4A`.
- Source localization layer: `open-logic-locale.sty` at the same commit.

## License

The upstream work is supplied under the Creative Commons Attribution 4.0
International License (CC BY 4.0):
<https://creativecommons.org/licenses/by/4.0/>.

This Arabic translation is an adaptation of the upstream work. Attribution
to the Open Logic Project, the source link, and the upstream license must be
retained when it is shared. No endorsement by the Open Logic Project is
implied.

## Changes

- Translated the complete “About the Open Logic Project” unit into formal
  Modern Standard Arabic without English fallback text.
- Translated every reader-facing caption and boilerplate string in the
  upstream localization file; internal localization keys and TeX command
  names remain unchanged.
- Added a minimal Arabic target configuration and an isolated LuaLaTeX driver
  with Unicode Arabic fonts, right-to-left paragraph handling through Babel,
  and left-to-right Latin font families.
- Preserved the source structure, links, scope qualifications, statements of
  incompleteness, and future-work caveats.
- Recorded terminology choices, rejected alternatives, and review status in
  `TERMINOLOGY_AND_ADVERSE_LEDGER.csv`.

Translation date: 2026-08-13. The translation is machine-assisted and has
passed independent AI semantic, structural, build, and visual replay. Review
by an Arabic-speaking human subject-matter editor remains absent.

## Current admitted coverage

The branch now contains paired-accepted Arabic units `OLP-0001` through
`OLP-0010`: the About text, corpus root, naïve-set-theory part driver, Sets
chapter driver, Extensionality, Subsets and Power Sets, Some Important Sets,
Unions and Intersections, Pairs and Products, and Russell's Paradox. Units 0005–0010
have clean isolated reader builds and exact localization IDs. Units 0002–0004 remain
source/structure/semantic accepted but are not
separately built because their imports are not yet closed. This is current
checkpoint history, not a claim that the 722-unit Arabic edition is complete.
