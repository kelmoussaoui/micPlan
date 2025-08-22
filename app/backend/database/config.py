# app/backend/database/config.py
# Configuration de la base de données SQLite

import os

# Configuration de la base de données SQLite
DATABASE_CONFIG = {
    'database_path': os.getenv('DB_PATH', 'data/micplan.db'),
    'max_connections': int(os.getenv('DB_MAX_CONNECTIONS', 25)),
    'timeout': int(os.getenv('DB_TIMEOUT', 30)),
    'check_same_thread': False,  # Permet l'utilisation multi-thread
    'isolation_level': None,  # Mode autocommit pour WAL
}

# Optimisations SQLite
SQLITE_OPTIMIZATIONS = {
    'wal_mode': True,  # Mode Write-Ahead Logging pour la concurrence
    'synchronous': 'NORMAL',  # NORMAL pour performance, FULL pour sécurité max
    'cache_size': -64000,  # 64MB de cache en mémoire
    'temp_store': 'MEMORY',  # Tables temporaires en mémoire
    'mmap_size': 268435456,  # 256MB de mmap
    'page_size': 4096,  # Taille de page optimisée
    'auto_vacuum': 'INCREMENTAL',  # Nettoyage automatique incrémental
    'incremental_vacuum': 1000,  # Nettoyage tous les 1000 pages
}

# Timeouts et retry
DB_TIMEOUTS = {
    'connection_timeout': 10,
    'query_timeout': 30,
    'max_retries': 5,  # Plus de retries pour SQLite
    'retry_delay': 0.05,  # Délai plus court
    'busy_timeout': 30000,  # 30 secondes de timeout pour les locks
}

# Configuration des sauvegardes
BACKUP_CONFIG = {
    'auto_backup': True,
    'backup_interval_hours': 24,
    'max_backups': 30,  # Garder 30 sauvegardes
    'backup_dir': 'data/backups',
    'compress_backups': True
}
