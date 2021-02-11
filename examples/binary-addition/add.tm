Q = {PREP,R-1,L+1,R-1C0,L+1C0,R-1C1,L+1C1,HALT}
G = {_,0,1,+}
b = {_}
S = {0,0,1,0,1,+,0,1,0,0,1}
q = {PREP}
F = {HALT}

PREP,_ -> _,L,R-1
PREP,0 -> 0,R,PREP
PREP,1 -> 1,R,PREP
PREP,+ -> +,R,PREP

R-1,_ -> _,R,HALT
R-1,0 -> 1,L,R-1C1
R-1,1 -> 0,L,R-1C0
R-1,+ -> +,R,HALT

R-1C0,_ -> _,L,HALT
R-1C0,0 -> 0,L,R-1C0
R-1C0,1 -> 1,L,R-1C0
R-1C0,+ -> +,L,L+1

R-1C1,_ -> _,L,HALT
R-1C1,0 -> 1,L,R-1C1
R-1C1,1 -> 0,L,R-1C0
R-1C1,+ -> +,L,HALT

L+1,_ -> _,R,HALT
L+1,0 -> 1,L,L+1C0
L+1,1 -> 0,L,L+1C1
L+1,+ -> +,R,HALT

L+1C0,_ -> _,R,PREP
L+1C0,0 -> 0,L,L+1C0
L+1C0,1 -> 1,L,L+1C0
L+1C0,+ -> +,L,HALT

L+1C1,_ -> _,R,PREP
L+1C1,0 -> 1,L,L+1C0
L+1C1,1 -> 0,L,L+1C1
L+1C1,+ -> +,L,HALT
