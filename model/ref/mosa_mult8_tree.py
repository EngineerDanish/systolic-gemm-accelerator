"""Bit-level reference of the MOSA 8x8 unsigned multiplier tree (paper Fig. 10, p.3281).
Reconstructed from the official PDF in T-01 verification. Exhaustively checked: 0/65536 failures.
Reference for RTL (T-03); the golden model itself uses plain integer multiply."""
# Fig.10 tree as read (col0 = LSB = rightmost column in figure)
n=lambda a:1-a
def c32(i1,i2,i3,ci):
    X1,X2,X3,X4=i1|i2,i1&i2,i3|ci,i3&ci
    return (X1&n(X2))^(X3&n(X4)), X2|X4|(X1&X3), X2&X4      # sum, carry, cout
def c42(i1,i2,i3,i4,ci):
    X1,X2,X3,X4=i1|i2,i1&i2,i3|i4,i3&i4
    Y=(X3&n(X4))^(X1&n(X2)); return ci^Y, (ci if Y else X4), X1&(X2|X3)
def fa(a,b,c): return a^b^c, (a&b)|(a&c)|(b&c)
def ha(a,b): return a^b, a&b
# per stage: {col: [cell types]}; remaining bits pass through
S1={4:['ha'],5:['32'],6:['32','fa'],7:['32','32'],8:['32','fa'],9:['42'],10:['42'],11:['32'],12:['fa']}
S2={2:['ha'],3:['32'],4:['32'],5:['32'],6:['32'],7:['42'],8:['42'],9:['42']}
S3={4:['ha'],5:['fa'],6:['fa'],7:['fa'],8:['32'],9:['fa'],10:['42'],11:['fa'],12:['fa'],13:['fa']}
RCA={1:'ha',**{k:'fa' for k in range(2,9)},9:'32',10:'32',11:'42',12:'32',13:'32',14:'32'}
W={'ha':2,'fa':3,'32':4,'42':5}
cnt={'ha':0,'fa':0,'32':0,'42':0}
def stage(cols,ops,count):
    out=[[] for _ in range(17)]
    for k,bits in enumerate(cols):
        bits=list(bits)
        for t in ops.get(k,[]):
            if count: cnt[t]+=1
            ins=[bits.pop(0) for _ in range(W[t])]
            r={'ha':ha,'fa':fa,'32':c32,'42':c42}[t](*ins)
            out[k].append(r[0]); out[k+1]+=list(r[1:])
        out[k]+=bits
    return out
def mul(a,b,count=False):
    cols=[[] for _ in range(17)]
    for i in range(8):
        for j in range(8): cols[i+j].append((a>>i)&1 & (b>>j)&1)
    h=[len(c) for c in cols]
    cols=stage(cols,S1,count); h1=[len(c) for c in cols]
    cols=stage(cols,S2,count); h2=[len(c) for c in cols]
    cols=stage(cols,S3,count); h3=[len(c) for c in cols]
    p=0; carry=[]
    for k in range(15):
        bits=cols[k]+carry; carry=[]
        if k in RCA:
            t=RCA[k]; assert len(bits)==W[t],(k,len(bits),t)
            if count: cnt[t]+=1
            r={'ha':ha,'fa':fa,'32':c32,'42':c42}[t](*bits); p|=r[0]<<k; carry=list(r[1:])
        else:
            assert len(bits)<=1,(k,bits); p|=(bits[0] if bits else 0)<<k
    if count: print("heights PP,S1,S2,S3 (col0..14):",h[:15],h1[:16],h2[:16],h3[:16],sep="\n"); print("carries into col15:",carry)
    return p,carry
p,c=mul(255,255,True); print(cnt)
fails=0;both=0
for a in range(256):
    for b in range(256):
        p,c=mul(a,b)
        p|= (c[0]|c[1])<<15 if len(c)==2 else 0
        if sum(c)==2: both+=1
        if p!=a*b: fails+=1
print("fails",fails,"/65536; cases with Carry&Cout both 1 at col15:",both)
