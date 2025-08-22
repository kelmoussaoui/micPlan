# app/frontend/auth/__init__.py
# Authentication module initialization

from .secure_auth import (
    show_login_page,
    check_authentication,
    logout_user,
    require_authentication,
    require_role,
    get_current_user,
    show_user_info
)

__all__ = [
    'show_login_page',
    'check_authentication',
    'logout_user',
    'require_authentication',
    'require_role',
    'get_current_user',
    'show_user_info'
]
