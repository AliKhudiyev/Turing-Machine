Q = {R0,R1,CARRY,HALT}
G = {_,0,1}
b = {_}
S = {1,3,1,2,1,2}
q = {PREP}
F = {HALT}

PREP,_ -> _,L,PICK
PREP,1 -> 1,R,PREP
PREP,2 -> 2,R,PREP
PREP,3 -> 3,R,PREP

PICK,_ -> _,R,HALT
PICK,1 -> _,R,P1
PICK,2 -> _,R,P2
PICK,3 -> _,R,P3

P1,_ -> 1,L,PREP
P1,1 -> 1,R,P1
P1,2 -> 2,R,P1
P1,3 -> 3,R,P1

P2,_ -> 2,L,PREP
P2,1 -> 1,R,P1
P2,2 -> 2,R,P1
P2,3 -> 3,R,P1

P3,_ -> 3,L,PREP
P3,1 -> 1,R,P1
P3,2 -> 2,R,P1
P3,3 -> 3,R,P1
