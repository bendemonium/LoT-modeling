import model.memory as mem

# 1D

# TOKENS

A = mem.Token(name="A", attribute1="red")
B = mem.Token(name="B", attribute1="red")
C = mem.Token(name="C", attribute1="red")
D = mem.Token(name="D", attribute1="blue")
E = mem.Token(name="E", attribute1="blue")
F = mem.Token(name="F", attribute1="blue")
G = mem.Token(name="G", attribute1="green")
H = mem.Token(name="H", attribute1="green")

# LEXICONS

# lex1 = mem.Lexicon(tokens={A,B,D,E}) 
# lex2 = mem.Lexicon(tokens={A,B,C,D,E,F})   
# lex3 = mem.Lexicon(tokens={A,B,D,E,G,H})

# 2D

# TOKENS

I = mem.Token(name="I", attribute1="red", attribute2="circle")
J = mem.Token(name="J", attribute1="red", attribute2="square")
K = mem.Token(name="K", attribute1="red", attribute2="triangle")
L = mem.Token(name="L", attribute1="blue", attribute2="circle")
M = mem.Token(name="M", attribute1="blue", attribute2="square")
N = mem.Token(name="N", attribute1="blue", attribute2="triangle")
O = mem.Token(name="O", attribute1="green", attribute2="circle")
P = mem.Token(name="P", attribute1="green", attribute2="square")
Q = mem.Token(name="Q", attribute1="green", attribute2="triangle")

# LEXICONS

# lex4 = mem.Lexicon(tokens={I,J,L,M})
# lex5 = mem.Lexicon(tokens={I,J,K,L,M,N})
# lex6 = mem.Lexicon(tokens={I,J,L,M,O,P})




