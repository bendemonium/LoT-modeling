import pytest
import model.memory as mem
import model.primitive_fucntions as pf

def test_add_list():
    l = mem.List(items=[1])
    pf.add(l, 2)
    assert list(l.items)[-1] == 2

def test_add_sequence():
    s = mem.Sequence(items=[1])
    pf.add(s, 2)
    assert list(s.items)[-1] == 2

def test_add_queue():
    q = mem.Queue(items=[1])
    pf.add(q, 2)
    assert list(q.items)[0] == 2

def test_flip_true_false():
    outcomes = [pf.flip(1.0), pf.flip(0.0)]
    assert outcomes[0] is True
    assert outcomes[1] is False

def test_pick_returns_mode():
    a, b = "x", "y"
    result = pf.pick(a, b, p=1.0)
    assert isinstance(result, mem.Mode)
    assert result.item == a

def test_sample_lexicon():
    t1 = mem.Token(name="A")
    t2 = mem.Token(name="B")
    lex = mem.Lexicon(tokens={t1, t2})
    token = pf.sample(lex)
    assert isinstance(token, mem.Token)
    assert token.name in {"A", "B"}

def test_remove_token():
    t1 = mem.Token(name="A")
    lex = mem.Lexicon(tokens=[t1])
    pf.remove(lex, t1)
    assert t1 not in lex.tokens

def test_inquire_token_attribute():
    t = mem.Token(name="A", attribute1="foo")
    val = pf.inquire_token(t, "attribute1")
    assert val == "foo"

def test_check_similarity():
    t1 = mem.Token(name="A", attribute1="foo")
    t2 = mem.Token(name="B", attribute1="foo")
    result = pf.check_similarity(t1, t2, "attribute1")
    assert result is True

def test_loop_returns_none():
    assert pf.loop() is None

def test_push_out_queue():
    q = mem.Queue(items=[2,1])
    token = pf.push_out(q)
    assert token == 1
    assert len(q.items) == 1

def test_find_basic():
    t1 = mem.Token(name="A", attribute1="foo")
    t2 = mem.Token(name="B", attribute1="bar")
    lex = mem.Lexicon(tokens={t1, t2})
    sub_lex = pf.find(lex, token=t1, criterion="attribute1")
    assert isinstance(sub_lex, mem.Lexicon)
    assert any(t.name == "A" for t in sub_lex.tokens)

def test_write_random_adds_to_memory_and_removes_from_lexicon():
    t1 = mem.Token(name="A")
    t2 = mem.Token(name="B")
    lex = mem.Lexicon(tokens={t1, t2})
    memory = mem.List()
    pf.write_random(lexicon=lex, memory=memory, found=True)
    # After writing, memory should have a token and lexicon should have one less
    print(memory.items)
    print(lex.tokens)
    assert len(memory.items) == 1
    assert len(lex.tokens) == 1

def test_write_all_removes_all_from_lexicon():
    t1 = mem.Token(name="A", attribute1="foo")
    t2 = mem.Token(name="B", attribute1="foo")
    lex = mem.Lexicon(tokens={t1, t2})
    memory = mem.List()
    pf.write_all(lexicon=lex, token=t1, bias="attribute1", memory=memory)
    # All tokens should be removed from lexicon
    assert len(lex.tokens) == 0

def test_inquire_token_link_and_attribute():
    t1 = mem.Token(name="A", attribute1="foo")
    lex = mem.Lexicon(tokens={t1})
    val = pf.inquire_token(t1, "attribute1")
    assert val == "foo"
    # link inquiry (should return 'out' since no edges)
    val_link = pf.inquire_token(t1, "link", lexicon=lex)
    assert val_link in {"in", "out"}