import pytest

from api.main import hello_world


def test_hello_world(capsys: pytest.CaptureFixture[str]) -> None:
    hello_world()

    assert capsys.readouterr().out == "Hello, World!\n"
