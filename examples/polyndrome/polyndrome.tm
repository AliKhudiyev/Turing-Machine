Q = {PREP,GET,SEARCH_A,SEARCH_B,SEARCH_C,A,B,C,HALT}
G = {_,a,b,c,X}
b = {_}
S = {a,c,a,b,a,b,a,c,a}
q = {PREP}
F = {HALT}

PREP,_ -> _,R,GET
PREP,a -> a,L,PREP
PREP,b -> b,L,PREP
PREP,c -> c,L,PREP

GET,_ -> _,R,HALT
GET,a -> _,R,SEARCH_A
GET,b -> _,R,SEARCH_B
GET,c -> _,R,SEARCH_C

SEARCH_A,_ -> _,L,A
SEARCH_A,a -> a,R,SEARCH_A
SEARCH_A,b -> b,R,SEARCH_A
SEARCH_A,c -> c,R,SEARCH_A

SEARCH_B,_ -> _,L,B
SEARCH_B,a -> a,R,SEARCH_B
SEARCH_B,b -> b,R,SEARCH_B
SEARCH_B,c -> c,R,SEARCH_B

SEARCH_C,_ -> _,L,C
SEARCH_C,a -> a,R,SEARCH_C
SEARCH_C,b -> b,R,SEARCH_C
SEARCH_C,c -> c,R,SEARCH_C

A,_ -> X,R,HALT
A,a -> _,L,PREP
A,b -> X,R,HALT
A,c -> X,R,HALT

B,_ -> X,R,HALT
B,a -> X,R,HALT
B,b -> _,L,PREP
B,c -> X,R,HALT

C,_ -> X,R,HALT
C,a -> X,R,HALT
C,b -> X,R,HALT
C,c -> _,L,PREP
