# app/backend/database/__init__.py
# Module principal de base de données

from .database_manager import DatabaseManager
from . import models
from .migration_manager import MigrationManager

# Instance globale de la base de données
db = DatabaseManager()

def init_database():
    """Initialiser la base de données"""
    try:
        db.initialize()
        return True
    except Exception as e:
        print(f"❌ Erreur d'initialisation de la base de données: {e}")
        return False

def close_database():
    """Fermer la base de données"""
    try:
        db.close()
        return True
    except Exception as e:
        print(f"❌ Erreur de fermeture de la base de données: {e}")
        return False

# Initialisation automatique lors de l'import
try:
    init_database()
except Exception as e:
    print(f"⚠️ Attention: Impossible d'initialiser la base de données automatiquement: {e}")

__all__ = [
    'db',
    'DatabaseManager', 
    'init_database',
    'close_database'
]
