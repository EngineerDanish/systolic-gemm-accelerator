"""Truth-table check of the MOSA proposed 3:2 and 4:2 compressors (paper Fig. 9, Tables II, III)."""
import itertools
n=lambda a:1-a
# proposed 3:2 per Fig 9 gates
bad=0
for i1,i2,i3,ci in itertools.product((0,1),repeat=4):
    X1n=n(i1|i2);X2n=n(i1&i2);X3n=n(i3|ci);X4n=n(i3&ci)
    cout=n(X2n|X4n)                       # NOR(X2b,X4b)
    carry=n(X2n&X4n)|n(X1n|X3n)          # OR(NAND(X2b,X4b),NOR(X1b,X3b))
    s=n(n(X1n)&X2n)^n(n(X3n)&X4n)         # XOR(NAND(~X1b,X2b),NAND(~X3b,X4b))
    if s+2*(carry+cout)!=i1+i2+i3+ci: bad+=1;print("3:2 FAIL",i1,i2,i3,ci,s,carry,cout)
print("3:2 gate-level fails:",bad,"/16")
# also check vs Table III rows
T3={(0,0,0,0):(0,0,0),(0,0,1,0):(0,0,1),(0,0,1,1):(0,1,0),(1,0,0,0):(0,0,1),(1,0,1,0):(0,1,0),(1,0,1,1):(0,1,1),(1,1,0,0):(0,1,0),(1,1,1,0):(0,1,1),(1,1,1,1):(1,1,0)}
b=0
for (X1,X2,X3,X4),(co,ca,s) in T3.items():
    ec=X2&X4; eca=X2|X4|(X1&X3); es=(X1&n(X2))^(X3&n(X4))
    if (ec,eca,es)!=(co,ca,s): b+=1;print("T3 mismatch",X1,X2,X3,X4)
print("Table III vs equations mismatches:",b,"/9")
# 4:2 per Fig 9 gates
bad=0;bad_lit=0;bad_cin=0
for i1,i2,i3,i4,ci in itertools.product((0,1),repeat=5):
    X1n=n(i1|i2);X2n=n(i1&i2);X3n=n(i3|i4);X4n=n(i3&i4)
    X1,X2,X3,X4=map(n,(X1n,X2n,X3n,X4n))
    cout=X1 & n(X3n&X2n)                  # AND(~X1b, NAND(X3b,X2b))
    Y=n(X4n&X3)^n(X2n&X1)                 # XOR(NAND(X4b,~X3b),NAND(X2b,~X1b))
    s=ci^Y
    carry=ci if Y else X4                 # mux sel=Y: 0 -> ~X4b, 1 -> Cin
    if s+2*(carry+cout)!=i1+i2+i3+i4+ci: bad+=1;print("4:2 FAIL",i1,i2,i3,i4,ci)
    # literal reading without overbars: Carry=Y*X4+Y*Cin, Cout=X1*X3*X2
    c2=(Y&X4)|(Y&ci); co2=X1&X3&X2
    if s+2*(c2+co2)!=i1+i2+i3+i4+ci: bad_lit+=1
    # reading Cout = X1*~X3*~X2 (overbar on each)
    co3=X1&n(X3)&n(X2)
    if s+2*(carry+co3)!=i1+i2+i3+i4+ci: bad_cin+=1
print("4:2 gate-level fails:",bad,"/32")
print("4:2 literal text (no overbars) fails:",bad_lit,"/32")
print("4:2 with Cout=X1.~X3.~X2 (per-term bars) fails:",bad_cin,"/32")
