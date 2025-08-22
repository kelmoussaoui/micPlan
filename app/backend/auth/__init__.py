# app/backend/auth/__init__.py
# Backend authentication module initialization

from .user_manager import UserManager

# Create a global instance
user_manager = UserManager()

__all__ = ['user_manager', 'UserManager']
