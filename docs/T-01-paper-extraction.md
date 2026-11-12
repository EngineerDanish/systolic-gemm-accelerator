# T-01: MOSA paper extraction

Paper: A. Sharma, L. H. Krishna, B. Srinivasu (IIT Mandi), "High-Performance Gemmini-Based Matrix Multiplication Accelerator for Deep Learning Workloads", IEEE TVLSI, vol. 33, no. 12, pp. 3276 to 3289, Dec 2025. DOI 10.1109/TVLSI.2025.3605207.

Source used: an unofficial full-text copy (body text readable, tables and figures low resolution). Values marked (low-res) need a check against the official IEEE PDF.

Baseline: upstream ucb-bar/gemmini at commit b82d49c.

## Parameters

| Parameter | MOSA (paper) | Gemmini default (source) | Paper ref |
|---|---|---|---|
| Input / weight width | 8-bit (16-bit also evaluated) | SInt(8) | Tables VII, VIII; Sec V-B |
| Signedness | Unsigned (inferred from Fig. 10, 11: zero-extended, no sign handling) | Signed | Fig. 10, 11 |
| PE output width after peripheral logic | 19 bits | SInt(20) | Sec III-B |
| Accumulator width | 16, 32, 64 evaluated; headline rows use 16 | SInt(32) | Tables VIII, XI, XII |
| Mesh | MOSA SA 8x8 to 64x64; Gemmini-integrated WS 2x2 to 8x8, OS 8x8 | 16x16 | Tables VII, X, XII |
| Tile | Not given | 1x1 | n/a |
| Dataflow | Separate WS PE and OS PE designs | BOTH | Sec III-A, III-B; Alg. 1, 2 |
| Scratchpad, acc memory, DMA | Not given | 256 KB / 4 banks; 64 KB / 2 banks; 128-bit bus | n/a |
| Platform | ASIC, UMC 90 nm, Cadence Genus, 5 ns constraint (200 MHz). No FPGA results | n/a | Sec V |

## What MOSA changes

Note: the paper's "existing Gemmini PE" has two MAC units per PE. Upstream Gemmini already moved to one shared MAC per PE in Dec 2022 (commit d3a58f4), so the paper compares against an older baseline.

1. Multiplier (Sec IV, Fig. 9 to 11, Tables II, III). The 8x8 multiplier uses AND-array partial products, a 3-stage reduction with 7 of the 4:2 compressors and 16 of the proposed 3:2 compressors, then a ripple-carry adder. The 16x16 multiplier is built from four 8x8 blocks. The proposed "3:2" compressor takes 4 equal-weight inputs (In1, In2, In3, Cin) through a stacking stage (X1 = In1|In2, X2 = In1&In2, X3 = In3|Cin, X4 = In3&Cin) and produces Sum, Carry and Cout. The multiplier is exact, so the change affects area, power and delay only.
2. WS PE (Sec III-A, Fig. 6, Alg. 1). One multiplier and one adder. The two weight registers have AND-gated load enables in place of input muxes. V gates only weight loading. A pipelined variant adds a register after the multiplier.
3. OS PE (Sec III-B, Fig. 8, Alg. 2). The valid signal is removed, so only P controls the PE. Two accumulator registers sit behind one shared multiplier and adder, and a single peripheral logic block (shift, round, saturate) follows the output mux.
4. Controller, scratchpad, DMA and ISA: no changes described.

## Claimed results (ASIC, 90 nm, all from the paper)

| Item | MOSA | Gemmini (paper's numbers) | Ref |
|---|---|---|---|
| WS PE | 1321 um2, 268 uW, 2.2 ns | 1891 um2, 481 uW, 2.8 ns | Table IX |
| WS SA 8x8 | 0.116 mm2, 38.07 mW, 2.2 ns | 0.159 mm2, 65.12 mW, 2.9 ns | Table X |
| OS PE, 32-bit acc | 6261 um2, 1900 uW, 2.9 ns | 8850 um2, 2500 uW, 3.0 ns | Table XI |
| OS SA 8x8, 32-bit acc | 0.404 mm2, 158 mW (low-res) | 0.625 mm2, 362 mW | Table XII |
| 8x8 multiplier | 1453 um2, 88.39 uW, 2.9 ns | n/a | Table V |
| MOSA 8-bit SA, 16-bit acc, 8x8 | 0.086 mm2, 0.018 W, 2.1 ns (low-res) | n/a | Tables VII, VIII |

Full results, including the compressor, transformer and CNN tables, are in the T-01 handoff in Project memory.

## Inconsistencies found in the paper (our arithmetic on its numbers)

- Table XIII: GOPS/W and GOPS/mm2 are exactly half of GOPS divided by power and by area.
- MOSA-32 reports 540.5 GOPS, which is above its own single-array peak of 204.8 GOPS.
- Table XIV AlexNet GOPS equal the four-array peaks, while the text reports 12.8 / 25.6 GOPS.
- The paper counts 1 op per MAC; most accelerator papers count 2.
