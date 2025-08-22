# config.py
# Configuration file for micPlan

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Application settings
APP_NAME = "micPlan"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Comprehensive platform for microbial genomics planning and analysis"

# Authentication settings
AUTH_SESSION_TIMEOUT = 24 * 60 * 60  # 24 hours in seconds
AUTH_MAX_LOGIN_ATTEMPTS = 5
AUTH_LOCKOUT_DURATION = 15 * 60  # 15 minutes in seconds

# Logging settings
LOG_LEVEL = "INFO"
LOG_DIR = BASE_DIR / "logs"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Data directories
DATA_DIR = BASE_DIR / "data"
SAMPLES_DIR = DATA_DIR / "samples"
RESULTS_DIR = DATA_DIR / "results"
EXPORTS_DIR = DATA_DIR / "exports"

# Resource directories
RESOURCES_DIR = BASE_DIR / "resources"
IMAGES_DIR = RESOURCES_DIR / "images"
ICONS_DIR = RESOURCES_DIR / "icons"
TEMPLATES_DIR = RESOURCES_DIR / "templates"

# Create directories if they don't exist
for directory in [LOG_DIR, DATA_DIR, SAMPLES_DIR, RESULTS_DIR, EXPORTS_DIR, 
                  RESOURCES_DIR, IMAGES_DIR, ICONS_DIR, TEMPLATES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Default user credentials (for development only)
DEFAULT_USERS = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "email": "admin@micplan.local"
    },
    "user1": {
        "username": "user1",
        "password": "user123",
        "first_name": "Regular",
        "last_name": "User",
        "role": "user",
        "email": "user1@micplan.local"
    }
}

# Contact information
CONTACT_EMAIL = "kelmoussaoui@chuliege.be"
CONTACT_NAME = "micPlan Support"
INSTITUTION = "CHU Liège"
LOCATION = "Liège, Belgium"
