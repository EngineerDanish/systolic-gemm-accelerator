# T-01 verification against the official IEEE PDF

Every number in T-01-paper-extraction.md matched the official PDF. This file adds what the low-resolution copy could not show.

## Compressors (Fig. 9, p.3280 to 3281)

Stacking for both: X1 = In1|In2, X2 = In1&In2, X3 = In3|Cin (3:2) or In3|In4 (4:2), X4 = In3&Cin or In3&In4. The figure draws these as NOR/NAND, so the wires carry the complements.

Proposed 3:2 (4 inputs In1, In2, In3, Cin):
- Sum = (X1 & ~X2) ^ (X3 & ~X4)
- Carry = X2 | X4 | (X1 & X3)
- Cout = X2 & X4
- Check: 16/16 gate level, 9/9 against Table III

Proposed 4:2 (5 inputs In1 to In4, Cin):
- Y = (X3 & ~X4) ^ (X1 & ~X2), which is the parity of In1 to In4
- Sum = Cin ^ Y
- Carry = Y ? Cin : X4
- Cout = X1 & (X2 | X3), independent of Cin
- Check: 32/32. The equations as printed without overbars fail 16/32.

Script: model/ref/compressor_truth_tables.py

## 8x8 multiplier tree (Fig. 10, p.3281)

Column k has weight 2^k. The LSB is the rightmost column in the figure. Partial-product heights for col 0 to 14: 1 2 3 4 5 6 7 8 7 6 5 4 3 2 1.

| Stage | Cells per column | Heights after |
|---|---|---|
| 1 | c4 HA; c5 3:2; c6 3:2+FA; c7 3:2+3:2; c8 3:2+FA; c9 4:2; c10 4:2; c11 3:2; c12 FA | 1 2 3 4 4 4 4 5 6 5 3 3 3 3 1 |
| 2 | c2 HA; c3 to c6 3:2 each; c7 4:2; c8 4:2; c9 4:2 | 1 2 2 2 3 3 3 3 4 3 5 3 3 3 1 |
| 3 | c4 HA; c5 to c7 FA; c8 3:2; c9 FA; c10 4:2; c11 to c13 FA | 1 2 2 2 2 2 2 2 2 3 2 3 2 2 2 |
| Final ripple | c0 wire; c1 HA; c2 to c8 FA; c9, c10 3:2; c11 4:2; c12 to c14 3:2; P[15] = Carry or Cout of c14 | 16-bit product |

Totals: 7 of 4:2 and 16 of 3:2 (matches the text), plus 17 FA and 4 HA (our count). Exhaustive check: 0 failures out of 65,536 unsigned operand pairs. Pin order inside a cell does not matter, since each cell is symmetric.

Script: model/ref/mosa_mult8_tree.py

## 16x16 multiplier (Fig. 11)

- Y1 = AL*BL, Y2 = AH*BL, Y3 = AL*BH, Y4 = AH*BH
- P1 = Y2 + Y1[15:8], P2 = Y4 + Y3[15:8] (16-bit adders)
- Out[31:8] = {P2, Y3[7:0]} + P1 (24-bit adder), Out[7:0] = Y1[7:0]
- The figure's "M1" is read as P1 (inference). This reading was checked with 200,000 random pairs.

## Statements the paper does not make

- Signedness: never mentioned. The tree is an unsigned multiplier and gives wrong results for two's complement inputs.
- Peripheral logic: called "PL for rounding" only. No shift amount, rounding mode, saturation or meaning of its Cntrl input.
- The 19-bit output (p.3279, Sec III-B) is stated only for the OS PE peripheral logic.
- The width of D and of the WS weight registers is not stated.

## New facts

- The headline "MOSA" arrays (Tables VII, VIII, XIII) are the simple output-stationary array of Fig. 3: one accumulator per PE, A skewed by row, B skewed by column, using the new multiplier. The Gemmini-integrated WS and OS PEs (Tables IX to XII) are a separate set of results.
- Synthesis setup: Genus, 5 ns clock, 50 ps I/O delay, 400 ps clock transition, SS/TT/FF corners (Table VI).
- Method: cocotb, tiles fed in sequence, outputs checked against golden software results. Throughput from post-synthesis simulation. TinyBERT Q (128x64) times K^T.
- Table XIV adds Top-1 accuracy: 82% AlexNet (CIFAR-10), 75.3% ResNet-50, 71.8% MobileNetV2 (ImageNet).
- Previously unread rows of Tables VII, VIII, X and XII are in the T-01 handoff in Project memory.

## More inconsistencies (our arithmetic on the paper's numbers)

- Table VI multiplier area (1528 um2 at every corner) differs from Table V (1453 um2).
- Table VII array delay (2.1 ns at 8-bit) is lower than the multiplier delay alone in Table V (2.9 ns).
- Sec V-B quotes PDP increases of 19% and 40%; Table VIII gives 23% and 68%.
- The proposed 4:2 compressor (0.442 ns) is slower than the conventional one (0.396 ns) in Table IV.
- Reference numbers in Table XIII differ from those in the text.
