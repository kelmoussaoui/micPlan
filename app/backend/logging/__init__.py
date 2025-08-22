# app/backend/logging/__init__.py
# Logging module initialization

from .logger import ActivityLogger

# Create a global instance
activity_logger = ActivityLogger()

__all__ = ['activity_logger', 'ActivityLogger']
