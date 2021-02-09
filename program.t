Q = {A,B,HALT}
G = {0,1,2}
b = {0}
S = {1,1,2,1,2}
q = {A}
F = {HALT}

A,1 -> 2,R,B
A,2 -> 2,R,B

B,1 -> 1,R,B
B,2 -> 1,R,HALT
