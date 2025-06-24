from utils import Element, KComplexity
import primitive_fucntions as pf

a = Element("a", 1, "red")
b = Element("b", 2, "blue")
c = Element("c", 3, "green")
d = Element("d", 4, "yellow")

Elements = {a, b, c, d}

def cog_1(E):
    pf.sample(E)
    among_us = []
    pf.add(a, among_us)
    pf.add(pf.sample(E), among_us)
    pf.remove(b, among_us)

kc = KComplexity()
cog_1(Elements)
print(kc.get_k_complexity())
print(kc.get_prim_counts())