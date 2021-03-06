from blaze.expr import symbol, summary
from datashape import dshape


def test_reduction_dshape():
    x = symbol('x', '5 * 3 * float32')
    assert x.sum().dshape == x.schema
    assert x.sum(axis=0).dshape == dshape('3 * float32')
    assert x.sum(axis=1).dshape == dshape('5 * float32')
    assert x.sum(axis=(0, 1)).dshape == dshape('float32')


def test_keepdims():
    x = symbol('x', '5 * 3 * float32')
    assert x.sum(axis=0, keepdims=True).dshape == dshape('1 * 3 * float32')
    assert x.sum(axis=1, keepdims=True).dshape == dshape('5 * 1 * float32')
    assert x.sum(axis=(0, 1), keepdims=True).dshape == dshape('1 * 1 * float32')

    assert x.std(axis=0, keepdims=True).shape == (1, 3)


def test_summary_keepdims():
    x = symbol('x', '5 * 3 * float32')
    assert summary(a=x.min(), b=x.max()).dshape == \
            dshape('{a: float32, b: float32}')
    assert summary(a=x.min(), b=x.max(), keepdims=True).dshape == \
            dshape('1 * 1 * {a: float32, b: float32}')


def test_summary_axis():
    x = symbol('x', '5 * 3 * float32')
    assert summary(a=x.min(), b=x.max(), axis=0).dshape == \
            dshape('3 * {a: float32, b: float32}')
    assert summary(a=x.min(), b=x.max(), axis=1).dshape == \
            dshape('5 * {a: float32, b: float32}')
    assert summary(a=x.min(), b=x.max(), axis=1, keepdims=True).dshape == \
            dshape('5 * 1 * {a: float32, b: float32}')


def test_summary_str():
    x = symbol('x', '5 * 3 * float32')
    assert 'keepdims' not in str(summary(a=x.min(), b=x.max()))


def test_axis_kwarg_is_normalized_to_tuple():
    x = symbol('x', '5 * 3 * float32')
    exprs = [x.sum(), x.sum(axis=1), x.sum(axis=[1]), x.std(), x.mean(axis=1)]
    for expr in exprs:
        assert isinstance(expr.axis, tuple)


def test_summary_with_multiple_children():
    t = symbol('t', 'var * {x: int, y: int, z: int}')

    assert summary(a=t.x.sum() + t.y.sum())._child.isidentical(t)


def test_dir():
    t = symbol('t', '10 * int')
    assert 'mean' in dir(t)

    t = symbol('t', 'int')
    assert 'mean' not in dir(t)
