import re
from contextlib import contextmanager


@contextmanager
def transaction(db):
    """
    Decorator for transactional database commits
    """
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


class TodoUtils:

    def _get_item(self, todo_id):
        """
        returns to do item or 404
        """
        return self.model.query.get_or_404(todo_id)

    @staticmethod
    def validate_title(title):
        """
        validation that eliminates digits as a task
        """
        if re.match('\d', title):
            raise AssertionError('not a valid task')
