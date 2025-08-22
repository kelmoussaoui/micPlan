# app/backend/database/migration_manager.py
# Gestionnaire de migrations pour la base SQLite

import os
from .database_manager import DatabaseManager

class MigrationManager:
    """Gestionnaire de migrations pour la base SQLite"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    
    def run_migrations(self):
        """Exécuter toutes les migrations en attente"""
        try:
            # Créer la table de migrations si elle n'existe pas
            self.db.execute_query("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version TEXT NOT NULL UNIQUE,
                    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    description TEXT
                )
            """, fetch=False)
            
            # Pour l'instant, on utilise le schéma principal
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors des migrations: {e}")
            return False
    
    def get_applied_migrations(self):
        """Récupérer la liste des migrations appliquées"""
        try:
            return self.db.execute_query("SELECT version FROM schema_migrations ORDER BY applied_at")
        except Exception:
            return []
