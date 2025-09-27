import pytest
import model.memory as mem
import model.primitive_fucntions as pf
from model.complexity import Space, Kolmo, RunScope, RunSnapshot, Complexity, cognitive_function

def test_space_register_update_purge():
    s = Space()
    class Dummy:
        pass
    d = Dummy()
    s.register(d, 5.0)
    assert s.active[id(d)] == 5.0
    assert s.total == 5.0
    s.update(d, 10.0)
    assert s.active[id(d)] == 10.0
    assert s.total == 10.0
    s.purge(d)
    assert id(d) not in s.active
    assert s.total == 0.0

def test_kolmo_record():
    k = Kolmo()
    k.record("foo", 3.0)
    k.record("foo", 2.0)
    assert k.counts["foo"] == 2
    assert k.total == 5.0

def test_runscope_init():
    rs = RunScope()
    assert isinstance(rs.space, Space)
    assert isinstance(rs.kolmo, Kolmo)

def test_runsnapshot_dataclass():
    snap = RunSnapshot(mdl=1, k_complexity_breakdown={"a": 2}, space_complexity=3.5)
    assert snap.mdl == 1
    assert snap.k_complexity_breakdown["a"] == 2
    assert snap.space_complexity == 3.5

def test_complexity_activate_and_properties():
    c = Complexity()
    with c.activate():
        pass
    assert len(c.runs) == 1
    assert c.cf_mdl == c.runs[0].mdl
    assert c.cf_space == c.runs[0].space_complexity
    c.purge()
    assert c.runs == []

def test_cognitive_function_decorator():
    class DummyMem:
        def __init__(self, weight):
            self._track = True
            self.weight = weight
        def compute_weight(self):
            return self.weight

    @cognitive_function()
    def run_fn(x, y):
        return x.compute_weight() + y.compute_weight()

    x = DummyMem(2)
    y = DummyMem(3)
    result, comp = run_fn(x, y)
    assert result == 5
    assert isinstance(comp, Complexity)
    assert len(comp.runs) == 1

def test_complexity_with_mem_objects_and_primitives():
    lex = mem.Lexicon(tokens={mem.Token(name="A"), mem.Token(name="B")})
    q = mem.Queue(items=[1,2])
    l = mem.List(items=[3,4])
    s = mem.Sequence(items=[5,6])

    @cognitive_function()
    def run_ops(lex, q, l, s):
        pf.add(lex, mem.Token(name="C"))
        pf.add(q, 3)
        pf.add(l, 5)
        pf.add(s, 7)
        pf.remove(lex, mem.Token(name="A"))
        pf.flip(0.9)
        pf.pick("x", "y", p=0.5)
        pf.sample(lex)
        pf.loop()
        pf.push_out(q)
        return lex, q, l, s

    result, comp = run_ops(lex, q, l, s)
    assert isinstance(comp, Complexity)
    assert len(comp.runs) == 1
    assert isinstance(result[0], mem.Lexicon)
    assert isinstance(result[1], mem.Queue)
    assert isinstance(result[2], mem.List)
    assert isinstance(result[3], mem.Sequence)
    assert comp.cf_mdl > 0
    assert comp.cf_space >= 0

def test_cognitive_function_registers_mem_objects():
    l = mem.List(items=[1,2])
    q = mem.Queue(items=[3,4])

    @cognitive_function()
    def just_add(l, q):
        pf.add(l, 5)
        pf.add(q, 6)
        return l, q

    result, comp = just_add(l, q)
    assert isinstance(comp, Complexity)
    assert len(comp.runs) == 1
    assert list(result[0].items)[-1] == 5
    assert list(result[1].items)[0] == 6

def test_cognitive_function_decorator_with_mem_objects():
    l = mem.List(items=[1,2])
    q = mem.Queue(items=[3,4])

    @cognitive_function()
    def run_fn(l, q):
        pf.add(l, 5)
        pf.add(q, 6)
        return l.compute_weight() + q.compute_weight()

    result, comp = run_fn(l, q)
    assert result == 3 + 3  # l: [1,2,5], q: [6,3,4]
    assert isinstance(comp, Complexity)
    assert len(comp.runs) == 1

def test_space_register_duplicate_object():
    s = Space()
    l = mem.List(items=[1])
    s.register(l, 2.0)
    s.register(l, 2.0)  # Should not double count
    assert s.active[id(l)] == 2.0
    assert s.total == 2.0

def test_space_update_nonexistent_object():
    s = Space()
    l = mem.List(items=[1])
    s.update(l, 5.0)  # Should add as new
    assert s.active[id(l)] == 5.0
    assert s.total == 5.0

def test_space_purge_nonexistent_object():
    s = Space()
    l = mem.List(items=[1])
    s.purge(l)  # Should not fail
    assert id(l) not in s.active
    assert s.total == 0.0

def test_kolmo_record_zero_weight():
    k = Kolmo()
    k.record("zero", 0.0)
    assert k.counts["zero"] == 1
    assert k.total == 0.0

def test_runscope_multiple_instances():
    rs1 = RunScope()
    rs2 = RunScope()
    assert rs1 is not rs2
    assert isinstance(rs1.space, Space)
    assert isinstance(rs2.kolmo, Kolmo)

def test_complexity_multiple_runs():
    c = Complexity()
    with c.activate():
        pass
    with c.activate():
        pass
    assert len(c.runs) == 2
    assert c.cf_mdl == sum(r.mdl for r in c.runs)
    assert c.cf_space == max(r.space_complexity for r in c.runs)

def test_complexity_purge_empty():
    c = Complexity()
    c.purge()
    assert c.runs == []
    assert c.last is None

def test_cognitive_function_with_no_mem_objects():
    @cognitive_function()
    def fn(x, y):
        return x + y
    result, comp = fn(1, 2)
    assert result == 3
    assert isinstance(comp, Complexity)
    assert len(comp.runs) == 1

def test_cognitive_function_with_kwargs_mem_objects():
    l = mem.List(items=[1])
    @cognitive_function()
    def fn(x=None):
        pf.add(x, 2)
        return x
    result, comp = fn(x=l)
    assert isinstance(result, mem.List)
    assert list(result.items)[-1] == 2
    assert isinstance(comp, Complexity)
    assert len(comp.runs) == 1

def test_cognitive_function_with_empty_list():
    l = mem.List()
    @cognitive_function()
    def fn(l):
        pf.add(l, 1)
        return l
    result, comp = fn(l)
    assert list(result.items) == [1]
    assert isinstance(comp, Complexity)

def test_cognitive_function_with_empty_lexicon():
    lex = mem.Lexicon()
    @cognitive_function()
    def fn(lex):
        pf.add(lex, mem.Token(name="A"))
        return lex
    result, comp = fn(lex)
    assert any(t.name == "A" for t in result.tokens)
    assert isinstance(comp, Complexity)

def test_cognitive_function_with_remove_nonexistent_token():
    lex = mem.Lexicon(tokens={mem.Token(name="A")})
    t = mem.Token(name="B")
    @cognitive_function()
    def fn(lex, t):
        pf.remove(lex, t)
        return lex
    result, comp = fn(lex, t)
    assert mem.Token(name="A") in result.tokens
    assert mem.Token(name="B") not in result.tokens

def test_cognitive_function_with_multiple_types():
    l = mem.List(items=[1])
    q = mem.Queue(items=[2])
    s = mem.Sequence(items=[3])
    lex = mem.Lexicon(tokens={mem.Token(name="A")})
    @cognitive_function()
    def fn(l, q, s, lex):
        pf.add(l, 2)
        pf.add(q, 3)
        pf.add(s, 4)
        pf.add(lex, mem.Token(name="B"))
        return l, q, s, lex
    result, comp = fn(l, q, s, lex)
    assert list(result[0].items)[-1] == 2
    assert list(result[1].items)[0] == 3
    assert list(result[2].items)[-1] == 4
    assert any(t.name == "B" for t in result[3].tokens)
    assert isinstance(comp, Complexity)

def test_cognitive_function_with_pick_and_flip():
    @cognitive_function()
    def fn():
        mode = pf.pick("x", "y", p=1.0)
        outcome = pf.flip(0.0)
        return mode, outcome
    result, comp = fn()
    assert result[0].item == "x"
    assert result[1] is False
    assert isinstance(comp, Complexity)

def test_cognitive_function_with_sample_and_push_out():
    lex = mem.Lexicon(tokens={mem.Token(name="A"), mem.Token(name="B")})
    q = mem.Queue(items=[1,2])
    @cognitive_function()
    def fn(lex, q):
        token = pf.sample(lex)
        out = pf.push_out(q)
        return token, out
    result, comp = fn(lex, q)
    assert isinstance(result[0], mem.Token)
    assert result[1] == 2
    assert isinstance(comp, Complexity)
