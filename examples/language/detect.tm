Q = {A,B,1,2,HALT}
G = {_,1,2,X,Y,N}
b = {_}
S = {1,1,2,1,2,1,2,2}
q = {A}
F = {HALT}

A,_ -> _,R,B
A,1 -> 1,L,A
A,2 -> 2,L,A
A,X -> X,L,A
A,N -> N,L,HALT

B,_ -> Y,R,HALT
B,1 -> X,R,1
B,2 -> X,R,2
B,X -> X,R,B
B,N -> N,R,HALT

1,_ -> N,L,HALT
1,1 -> 1,R,1
1,2 -> X,L,A
1,X -> X,R,1
1,N -> N,R,HALT

2,_ -> N,L,HALT
2,1 -> X,R,A
2,2 -> 2,R,2
2,X -> X,R,2
2,N -> N,R,HALT
