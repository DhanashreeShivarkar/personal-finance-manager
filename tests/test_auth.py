import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from register import register_user
from login import login_user

def test_user_registration(tmp_path):
    # Example: mock database or use temp file if needed
    result = register_user("testuser", "Testpass@1")
    assert result is True

def test_user_login_success():
    user_id = login_user("testuser", "Testpass@1")
    assert user_id is not None

def test_user_login_failure():
    user_id = login_user("wronguser", "wrongpass")
    assert user_id is None
