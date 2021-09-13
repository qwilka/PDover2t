from operator import mul, sub
from graphkit import compose, operation

# Computes |a|^p.
def abspow(a, p):
    c = abs(a) ** p
    return c


op1 = operation(name="mul1", needs=["a", "b"], provides=["ab"])(mul)

# Compose the mul, sub, and abspow operations into a computation graph.
graph = compose(name="graph")(
    op1,
    operation(name="sub1", needs=["a", "ab"], provides=["a_minus_ab"])(sub),
    operation(name="abspow1", needs=["a_minus_ab"], provides=["abs_a_minus_ab_cubed"], params={"p": 3})(abspow)
)

# Run the graph and request all of the outputs.
out = graph({'a': 2, 'b': 5})

# Prints "{'a': 2, 'a_minus_ab': -8, 'b': 5, 'ab': 10, 'abs_a_minus_ab_cubed': 512}".
print(out)

# Run the graph and request a subset of the outputs.
out = graph({'a': 2, 'b': 5}, outputs=["a_minus_ab"])

# Prints "{'a_minus_ab': -8}".
print(out)
