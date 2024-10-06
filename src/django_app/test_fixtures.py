import pytest


@pytest.fixture
def num_seq():
    return [0, 1, 2, 3, 4]


def test_xpto(num_seq):
    assert 1 in num_seq