import pytest
from model.memory import (
    MemoryStructure, Token, Lexicon, List, Queue, Mode, Sequence, Pointer
)
import networkx as nx

def test_memorystructure_compute_weight_default():
    m = MemoryStructure()
    assert m.compute_weight() == 0.0

def test_token_init_and_weight():
    t = Token(name="A", attribute1="x", attribute2="y")
    assert t.name == "A"
    assert t.attribute1 == "x"
    assert t.attribute2 == "y"
    assert isinstance(t.predecessors, set)
    assert isinstance(t.successors, set)
    assert t.compute_weight() >= 1

def test_token_bool_and_repr():
    t = Token(name="X")
    assert bool(t)
    assert "Token" in repr(t)

def test_lexicon_add_remove_token():
    t1 = Token(name="A")
    t2 = Token(name="B")
    lex = Lexicon(tokens=[t1])
    assert t1 in lex.tokens
    lex.add_token(t2)
    assert t2 in lex.tokens
    lex.remove_token(t1)
    assert t1 not in lex.tokens

def test_lexicon_iter_and_get_token():
    t1 = Token(name="A")
    t2 = Token(name="B")
    lex = Lexicon(tokens=[t1, t2])
    assert set(lex) == {t1, t2}
    assert lex.get_token("A") == t1
    assert lex.get_token("B") == t2
    assert lex.get_token("C") is None

def test_lexicon_graph_property_and_weight():
    t1 = Token(name="A")
    lex = Lexicon(tokens=[t1])
    assert isinstance(lex.G, nx.MultiDiGraph)
    assert isinstance(lex.compute_weight(), float)

def test_list_operations():
    l = List(items=[1,2,3])
    assert l.compute_weight() == 3
    l.suffix(4)
    assert l.items[-1] == 4
    l.prefix(0)
    assert l.items[0] == 0
    l.reverse()
    assert list(l.items) == [4,3,2,1,0]
    l.clear()
    assert len(l.items) == 0
    l2 = List()
    l2.clone(List(items=[5,6]))
    assert list(l2.items) == [5,6]

def test_queue_operations():
    q = Queue(items=[1,2,3])
    assert q.compute_weight() == 3
    q.push_in(0)
    assert q.items[0] == 0
    out = q.push_out()
    assert out == 3
    q.clear()
    assert len(q.items) == 0
    q2 = Queue()
    q2.clone(Queue(items=[7,8]))
    assert list(q2.items) == [7,8]

def test_mode_weight_and_init():
    m = Mode(item="foo")
    assert m.item == "foo"
    assert m.compute_weight() == 1

def test_sequence_click_and_init():
    s = Sequence(items=[1])
    s.click(2)
    assert list(s.items) == [1,2]

def test_pointer_init_and_node():
    p = Pointer(node="N")
    assert p.node == "N"
    l.reverse()
    assert list(l.items) == [3,2,1]
    l2 = List()
    l2.clone(l)
    assert list(l2.items) == [3,2,1]

def test_queue_clone():
    q1 = Queue(items=[1,2])
    q2 = Queue()
    q2.clone(q1)
    assert list(q2.items) == [1,2]

def test_list_prefix_and_suffix():
    l = List(items=[1])
    l.prefix(0)
    l.suffix(2)
    assert list(l.items) == [0,1,2]

def test_list_clear():
    l = List(items=[1,2])
    l.clear()
    assert len(l.items) == 0

def test_queue_clear():
    q = Queue(items=[1,2])
    q.clear()
    assert len(q.items) == 0

def test_mode_weight_and_init():
    m = Mode(item="foo")
    assert m.item == "foo"
    assert m.compute_weight() == 1

def test_sequence_click_and_init():
    s = Sequence(items=[1])
    s.click(2)
    assert list(s.items) == [1,2]

def test_pointer_init_and_node():
    p = Pointer(node="N")
    assert p.node == "N"

