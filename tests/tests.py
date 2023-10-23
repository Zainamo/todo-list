from src.app import app


def test_create_todo_item():
    data = {
        'title': 'custom_title'
    }
    resp = app.test_client().post(
        'http://127.0.0.1:5000/todo/',
        data=data
    )
    assert resp.status_code == 302


def test_get_todo_list():
    data = {
        'title': 'custom_title'
    }
    app.test_client().post(
        'http://127.0.0.1:5000/todo/',
        data=data
    )
    resp = app.test_client().get(
        'http://127.0.0.1:5000/todo/'
    )
    assert resp.status_code == 200
