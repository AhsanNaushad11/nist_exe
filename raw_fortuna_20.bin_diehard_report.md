# Diehard Statistical Test Report

**Target File:** `raw_fortuna_20.bin`
**Total Tests Run:** 49

## Summary
- **PASSED:** 41/49
- **WEAK:** 5/49
- **FAILED:** 3/49

## Detailed Results
| Test Name | P-Value | Verdict |
| :--- | :--- | :--- |
| [01] Birthday Spacings 01/10 | `0.406006` | ✅ PASSED |
| [01] Birthday Spacings 02/10 | `0.406006` | ✅ PASSED |
| [01] Birthday Spacings 03/10 | `0.676676` | ✅ PASSED |
| [01] Birthday Spacings 04/10 | `0.947347` | ✅ PASSED |
| [01] Birthday Spacings 05/10 | `0.857123` | ✅ PASSED |
| [01] Birthday Spacings 06/10 | `0.857123` | ✅ PASSED |
| [01] Birthday Spacings 07/10 | `0.983436` | ⚠️ WEAK |
| [01] Birthday Spacings 08/10 | `0.947347` | ✅ PASSED |
| [01] Birthday Spacings 09/10 | `0.406006` | ✅ PASSED |
| [01] Birthday Spacings 10/10 | `0.857123` | ✅ PASSED |
| [02] 5-Permutations | `0.417905` | ✅ PASSED |
| [03] Binary Rank 32x32 | `0.721063` | ✅ PASSED |
| [04] Binary Rank 6x8 | `0.067206` | ✅ PASSED |
| [05] Bitstream 01/03 | `0.336587` | ✅ PASSED |
| [05] Bitstream 02/03 | `0.395651` | ✅ PASSED |
| [05] Bitstream 03/03 | `0.021975` | ⚠️ WEAK |
| [06] OPSO 01/03 | `0.198768` | ✅ PASSED |
| [06] OPSO 02/03 | `0.198768` | ✅ PASSED |
| [06] OPSO 03/03 | `0.198768` | ✅ PASSED |
| [07] OQSO 01/03 | `0.693403` | ✅ PASSED |
| [07] OQSO 02/03 | `0.693403` | ✅ PASSED |
| [07] OQSO 03/03 | `0.693403` | ✅ PASSED |
| [08] DNA 01/03 | `0.203630` | ✅ PASSED |
| [08] DNA 02/03 | `0.203630` | ✅ PASSED |
| [08] DNA 03/03 | `0.203630` | ✅ PASSED |
| [09] Count 1s Stream | `0.427954` | ✅ PASSED |
| [10] Count 1s Byte 1 | `0.728123` | ✅ PASSED |
| [10] Count 1s Byte 2 | `0.936236` | ✅ PASSED |
| [10] Count 1s Byte 3 | `0.909280` | ✅ PASSED |
| [10] Count 1s Byte 4 | `0.038439` | ⚠️ WEAK |
| [11] Parking Lot 01/05 | `0.000217` | ❌ FAILED |
| [11] Parking Lot 02/05 | `0.000369` | ❌ FAILED |
| [11] Parking Lot 03/05 | `0.012025` | ⚠️ WEAK |
| [11] Parking Lot 04/05 | `0.120540` | ✅ PASSED |
| [11] Parking Lot 05/05 | `0.000520` | ❌ FAILED |
| [12] Minimum Distance 01/05 | `0.833262` | ✅ PASSED |
| [12] Minimum Distance 02/05 | `0.849826` | ✅ PASSED |
| [12] Minimum Distance 03/05 | `0.723041` | ✅ PASSED |
| [12] Minimum Distance 04/05 | `0.900459` | ✅ PASSED |
| [12] Minimum Distance 05/05 | `0.835458` | ✅ PASSED |
| [13] 3D Spheres 01/05 | `0.056254` | ✅ PASSED |
| [13] 3D Spheres 02/05 | `0.145954` | ✅ PASSED |
| [13] 3D Spheres 03/05 | `0.012625` | ⚠️ WEAK |
| [13] 3D Spheres 04/05 | `0.681827` | ✅ PASSED |
| [13] 3D Spheres 05/05 | `0.282975` | ✅ PASSED |
| [14] Squeeze | `0.889190` | ✅ PASSED |
| [15] Sums (Non-overlap) | `0.381705` | ✅ PASSED |
| [16] Runs Up | `0.873811` | ✅ PASSED |
| [17] Craps | `0.946259` | ✅ PASSED |

## Interpretation
- **PASSED:** 0.05 <= p <= 0.95. The data appears random according to this test.
- **WEAK:** 0.001 <= p < 0.05 or 0.95 < p <= 0.999. The data is suspicious. In a suite of 49 tests, finding a few weak results is statistically expected due to chance.
- **FAILED:** p < 0.001 or p > 0.999. The data strongly deviates from true randomness.
