Q = {PREP,PICK,P1,P2,P3,LOCATE,CARRY,PUT,HALT}
G = {_,1,2,3}
b = {_}
S = {1,3,1,2,1,2}
q = {PREP}
F = {HALT}

PREP,_ -> _,R,PICK
PREP,1 -> 1,L,PREP
PREP,2 -> 2,L,PREP
PREP,3 -> 3,L,PREP

PICK,_ -> _,R,HALT
PICK,1 -> _,L,P1
PICK,2 -> _,L,P2
PICK,3 -> _,L,P3

P1,_ -> 1,R,PREP
P1,1 -> 1,L,P1
P1,2 -> 2,L,P1
P1,3 -> 3,L,P1

P2,_ -> 2,R,PREP
P2,1 -> 1,L,P1
P2,2 -> 2,L,P1
P2,3 -> 3,L,P1

P3,_ -> 3,R,PREP
P3,1 -> 1,L,P1
P3,2 -> 2,L,P1
P3,3 -> 3,L,P1
