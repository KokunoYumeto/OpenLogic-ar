# Scope and qualification of the implicit-math intake

The accepted intake has 87 confirmed conversion gaps and eight separate notation-policy questions. It is source-level evidence, not a PDF rendering check or a completed correction. No Arabic prose was changed.

The preceding diagnostic in `implicit-math-intake-96175312` grouped all 95 unchanged arguments together. That was too broad: the third arguments `R` and `N` of eight `TMtrans` calls denote machine instructions. The qualified companion list retains their exact locations but does not call them automatic letter-conversion errors.

The actual primary definitions in `source/open-logic-config.sty` are:

- Lines 859–860: `mTrue` and `mFalse` put their argument inside `ensuremath`.
- Line 1041: `TMtrans` prints all three arguments inside `ensuremath`.
- Lines 1031, 1034 and 1037: `TMright`, `TMleft` and `TMstay` establish the direction constants `R`, `L` and `N`.

Exact source SHA-256: `ab19be71b50b415738603290317b504d9fa6b82850fe640d585c62db1540ced3`.

Provisional editorial treatment of the eight direction constants: retain their current identities until an explicit source-grounded presentation rule is implemented, preserving their consistency with the named direction commands and machine definitions. Do not substitute Arabic letters merely because a token is alphabetic. This is open to correction and does not require expert participation before production continues.

The other 87 arguments are visibly mathematical letters/numerals that remain literal inside these carriers, unlike their already localized explicit-math counterparts. The next finite parser repair should recognize only these primary-source-bound carrier contracts, preserve reference/diagram keys and international exemptions, and verify exact inversion for every changed occurrence. Arbitrary macro expansion is not authorized by this finding.
