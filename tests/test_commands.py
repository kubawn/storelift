import pytest
from src.commands import create


def test_create_method(mocker):
    mocked_post = mocker.patch("src.commands.requests.post", return_value=mocker.Mock(text="coucou"))
    mocked_print = mocker.patch("src.commands.print")
    
    res = create(1, 10.0)

    mocked_post.assert_called_once_with("http://localhost:5000/register_customer", data={"id": 1, "credits": 10.0})
    mocked_print.assert_called_once_with("coucou")
