"""Prevent tests from ever writing to the operator's real customer database."""
import atexit
import os
import tempfile

_temp = tempfile.TemporaryDirectory(prefix='ltd-book-tests-')
os.environ['MBS_DATA_DIR'] = _temp.name
os.environ.pop('MBS_ADMIN_USER', None)
os.environ.pop('MBS_ADMIN_PASSWORD', None)
atexit.register(_temp.cleanup)
