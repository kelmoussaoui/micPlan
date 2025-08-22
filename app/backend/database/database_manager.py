# app/backend/database/database_manager.py
# Gestionnaire de base de données SQLite optimisé

import sqlite3
import os
import json
import gzip
import shutil
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union, Tuple
from contextlib import contextmanager
import logging

# Import de la configuration locale
from .config import DATABASE_CONFIG, SQLITE_OPTIMIZATIONS, DB_TIMEOUTS, BACKUP_CONFIG

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gestionnaire principal de base de données SQLite avec optimisations WAL et gestion des locks"""
    
    def __init__(self):
        self.config = DATABASE_CONFIG
        self.optimizations = SQLITE_OPTIMIZATIONS
        self.timeouts = DB_TIMEOUTS
        self.db_path = self.config['database_path']
        self.connections = {}
        self.is_initialized = False
        
        # Créer le répertoire de la base de données si nécessaire
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
    def initialize(self):
        """Initialiser la base de données avec le schéma et les optimisations"""
        try:
            # Créer le répertoire de la base de données si nécessaire
            db_dir = os.path.dirname(DATABASE_CONFIG['database_path'])
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            # Créer une connexion directe pour l'initialisation
            conn = sqlite3.connect(
                self.db_path,
                timeout=DB_TIMEOUTS['busy_timeout'] / 1000,
                check_same_thread=False
            )
            
            try:
                # Appliquer les optimisations SQLite
                for pragma, value in SQLITE_OPTIMIZATIONS.items():
                    if pragma == 'wal_mode':
                        conn.execute("PRAGMA journal_mode=WAL")
                    elif pragma == 'synchronous':
                        conn.execute(f"PRAGMA synchronous={value}")
                    elif pragma == 'cache_size':
                        conn.execute(f"PRAGMA cache_size={value}")
                    elif pragma == 'temp_store':
                        conn.execute(f"PRAGMA temp_store={value}")
                    elif pragma == 'mmap_size':
                        conn.execute(f"PRAGMA mmap_size={value}")
                    elif pragma == 'page_size':
                        conn.execute(f"PRAGMA page_size={value}")
                    elif pragma == 'auto_vacuum':
                        conn.execute(f"PRAGMA auto_vacuum={value}")
                    elif pragma == 'incremental_vacuum':
                        conn.execute(f"PRAGMA incremental_vacuum={value}")
                
                # Créer le schéma de la base de données
                self._create_schema(conn)
                
                # Nettoyer automatiquement les doublons existants
                self._cleanup_duplicates_direct(conn)
                
                # Créer les données initiales
                self._create_initial_data(conn)
                
                self.is_initialized = True
                logger.info("✅ Base de données SQLite initialisée avec succès")
                
            finally:
                conn.close()
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
            raise
    
    def _create_schema(self, conn):
        """Créer le schéma de la base de données"""
        try:
            # Lire le fichier schema.sql
            schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
            if os.path.exists(schema_file):
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                
                # Exécuter le schéma
                conn.executescript(schema_sql)
                conn.commit()
                logger.info("✅ Schéma de la base de données créé avec succès")
            else:
                logger.warning("⚠️ Fichier schema.sql non trouvé")
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de la création du schéma: {e}")
            raise
    
    def _create_initial_data(self, conn):
        """Créer les données initiales de la base de données"""
        try:
            # Vérifier d'abord si des données existent déjà
            existing_positions = conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
            
            if existing_positions > 0:
                logger.info(f"⚠️ {existing_positions} postes existent déjà, pas de création de données initiales")
                return
            
            # Créer quelques postes d'exemple seulement si la table est vide
            conn.execute("""
                INSERT INTO positions (id, name, secteur, priority, description, min_agents, max_agents)
                VALUES 
                ('P1', 'Poste 1 - Réception', 'Biologie moléculaire', 8, 'Réception et préparation des échantillons', 1, 2),
                ('P2', 'Poste 2 - Extraction', 'Biologie moléculaire', 9, 'Extraction d''ADN/ARN', 1, 1),
                ('P3', 'Poste 3 - PCR', 'Biologie moléculaire', 10, 'Amplification PCR', 1, 1)
            """)
            
            # Créer les configurations de fréquence pour ces postes
            conn.execute("""
                INSERT INTO position_frequency_config 
                (position_id, week_frequency, weekdays, morning, afternoon, evening)
                VALUES 
                ('P1', 'Toutes les semaines', '["lundi", "mardi", "mercredi", "jeudi", "vendredi"]', 1, 1, 0),
                ('P2', 'Toutes les semaines', '["lundi", "mardi", "mercredi", "jeudi", "vendredi"]', 1, 0, 0),
                ('P3', 'Une semaine sur deux', '["mardi", "mercredi"]', 0, 1, 0)
            """)
            
            conn.commit()
            logger.info("✅ Données initiales créées avec succès")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la création des données initiales: {e}")
            # Ne pas lever l'exception car ce n'est pas critique
    
    @contextmanager
    def get_connection(self):
        """Obtenir une connexion SQLite avec gestion automatique des locks"""
        # Si pas initialisé, initialiser automatiquement
        if not self.is_initialized:
            try:
                self.initialize()
            except Exception as e:
                raise RuntimeError(f"Impossible d'initialiser la base de données: {e}")
        
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_path,
                timeout=self.timeouts['connection_timeout'],
                check_same_thread=self.config['check_same_thread'],
                isolation_level=self.config['isolation_level']
            )
            
            # Configurer la connexion
            conn.execute(f"PRAGMA busy_timeout={self.timeouts['busy_timeout']}")
            
            yield conn
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                logger.warning(f"⚠️ Base de données verrouillée, retry automatique...")
                raise
            else:
                logger.error(f"❌ Erreur opérationnelle SQLite: {e}")
                raise
        except Exception as e:
            logger.error(f"❌ Erreur de connexion: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True) -> Optional[List[Dict]]:
        """Exécuter une requête avec retry automatique et gestion des locks"""
        for attempt in range(self.timeouts['max_retries']):
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(query, params or ())
                    
                    if fetch:
                        # Convertir en liste de dictionnaires
                        columns = [description[0] for description in cursor.description]
                        result = []
                        for row in cursor.fetchall():
                            result.append(dict(zip(columns, row)))
                        return result
                    else:
                        conn.commit()
                        return None
                        
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < self.timeouts['max_retries'] - 1:
                    wait_time = self.timeouts['retry_delay'] * (2 ** attempt)
                    logger.warning(f"⚠️ Tentative {attempt + 1} échouée (lock), nouvelle tentative dans {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"❌ Erreur opérationnelle après {attempt + 1} tentatives: {e}")
                    raise
            except Exception as e:
                logger.error(f"❌ Erreur inattendue: {e}")
                raise
    
    def execute_transaction(self, queries: List[Tuple[str, tuple]]) -> bool:
        """Exécuter plusieurs requêtes dans une transaction avec retry"""
        for attempt in range(self.timeouts['max_retries']):
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    for query, params in queries:
                        cursor.execute(query, params or ())
                    conn.commit()
                    return True
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < self.timeouts['max_retries'] - 1:
                    wait_time = self.timeouts['retry_delay'] * (2 ** attempt)
                    logger.warning(f"⚠️ Transaction échouée (lock), nouvelle tentative dans {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"❌ Erreur de transaction: {e}")
                    return False
            except Exception as e:
                logger.error(f"❌ Erreur inattendue dans la transaction: {e}")
                return False
    
    def table_exists(self, table_name: str) -> bool:
        """Vérifier si une table existe"""
        query = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """
        result = self.execute_query(query, (table_name,))
        return len(result) > 0
    
    def get_table_info(self, table_name: str) -> List[Dict]:
        """Obtenir les informations d'une table"""
        query = "PRAGMA table_info(?)"
        return self.execute_query(query, (table_name,))
    
    def backup_database(self, backup_path: str = None) -> str:
        """Sauvegarder la base de données (copie simple du fichier)"""
        try:
            if not backup_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"{BACKUP_CONFIG['backup_dir']}/micplan_backup_{timestamp}.db"
            
            # Créer le répertoire de backup si nécessaire
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # Copier le fichier de base de données
            shutil.copy2(self.db_path, backup_path)
            
            # Compresser si configuré
            if BACKUP_CONFIG['compress_backups']:
                compressed_path = f"{backup_path}.gz"
                with open(backup_path, 'rb') as f_in:
                    with gzip.open(compressed_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(backup_path)  # Supprimer le fichier non compressé
                backup_path = compressed_path
            
            logger.info(f"✅ Sauvegarde créée: {backup_path}")
            
            # Nettoyer les anciennes sauvegardes
            self._cleanup_old_backups()
            
            return backup_path
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
            raise
    
    def restore_database(self, backup_path: str) -> bool:
        """Restaurer la base de données depuis une sauvegarde"""
        try:
            # Décompresser si nécessaire
            if backup_path.endswith('.gz'):
                decompressed_path = backup_path[:-3]
                with gzip.open(backup_path, 'rb') as f_in:
                    with open(decompressed_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                backup_path = decompressed_path
            
            # Créer une sauvegarde de la base actuelle
            current_backup = self.backup_database()
            logger.info(f"✅ Sauvegarde de sécurité créée: {current_backup}")
            
            # Fermer toutes les connexions
            self.close()
            
            # Remplacer la base de données
            shutil.copy2(backup_path, self.db_path)
            
            # Réinitialiser
            self.initialize()
            
            logger.info(f"✅ Base de données restaurée depuis: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la restauration: {e}")
            # Tenter de réinitialiser
            try:
                self.initialize()
            except:
                pass
            raise
    
    def _cleanup_old_backups(self):
        """Nettoyer les anciennes sauvegardes"""
        try:
            backup_dir = BACKUP_CONFIG['backup_dir']
            if not os.path.exists(backup_dir):
                return
            
            # Lister tous les fichiers de backup
            backup_files = []
            for file in os.listdir(backup_dir):
                if file.startswith('micplan_backup_') and (file.endswith('.db') or file.endswith('.db.gz')):
                    file_path = os.path.join(backup_dir, file)
                    backup_files.append((file_path, os.path.getmtime(file_path)))
            
            # Trier par date de modification
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # Supprimer les anciennes sauvegardes
            if len(backup_files) > BACKUP_CONFIG['max_backups']:
                for file_path, _ in backup_files[BACKUP_CONFIG['max_backups']:]:
                    os.remove(file_path)
                    logger.info(f"🗑️ Ancienne sauvegarde supprimée: {file_path}")
                    
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors du nettoyage des sauvegardes: {e}")
    
    def get_database_size(self) -> Dict[str, Any]:
        """Obtenir les informations sur la taille de la base de données"""
        try:
            db_size = os.path.getsize(self.db_path)
            wal_size = 0
            if os.path.exists(f"{self.db_path}-wal"):
                wal_size = os.path.getsize(f"{self.db_path}-wal")
            
            return {
                'database_size_mb': round(db_size / (1024 * 1024), 2),
                'wal_size_mb': round(wal_size / (1024 * 1024), 2),
                'total_size_mb': round((db_size + wal_size) / (1024 * 1024), 2)
            }
        except Exception as e:
            logger.error(f"❌ Erreur lors du calcul de la taille: {e}")
            return {}
    
    def vacuum_database(self) -> bool:
        """Nettoyer et optimiser la base de données"""
        try:
            with self.get_connection() as conn:
                conn.execute("VACUUM")
                conn.execute("ANALYZE")
                logger.info("✅ Base de données optimisée avec VACUUM et ANALYZE")
                return True
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'optimisation: {e}")
            return False
    
    def close(self):
        """Fermer proprement la base de données"""
        try:
            # Fermer toutes les connexions
            for conn in self.connections.values():
                conn.close()
            self.connections.clear()
            
            # Optimiser la base
            self.vacuum_database()
            
            self.is_initialized = False
            logger.info("✅ Base de données fermée proprement")
        except Exception as e:
            logger.error(f"❌ Erreur lors de la fermeture: {e}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def cleanup_duplicates(self):
        """Nettoyer les doublons dans la base de données"""
        try:
            with self.get_connection() as conn:
                # Supprimer les doublons de positions (garder le premier)
                conn.execute("""
                    DELETE FROM positions 
                    WHERE rowid NOT IN (
                        SELECT MIN(rowid) 
                        FROM positions 
                        GROUP BY id
                    )
                """)
                
                # Supprimer les doublons de configurations de fréquence
                conn.execute("""
                    DELETE FROM position_frequency_config 
                    WHERE rowid NOT IN (
                        SELECT MIN(rowid) 
                        FROM position_frequency_config 
                        GROUP BY position_id
                    )
                """)
                
                conn.commit()
                logger.info("✅ Doublons nettoyés avec succès")
                return True
                
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage des doublons: {e}")
            return False

    def _cleanup_duplicates_direct(self, conn):
        """Nettoyer les doublons directement dans la connexion fournie"""
        try:
            # Supprimer les doublons de positions (garder le premier)
            conn.execute("""
                DELETE FROM positions 
                WHERE rowid NOT IN (
                    SELECT MIN(rowid) 
                    FROM positions 
                    GROUP BY id
                )
            """)
            
            # Supprimer les doublons de configurations de fréquence
            conn.execute("""
                DELETE FROM position_frequency_config 
                WHERE rowid NOT IN (
                    SELECT MIN(rowid) 
                    FROM position_frequency_config 
                    GROUP BY position_id
                )
            """)
            
            conn.commit()
            logger.info("✅ Doublons nettoyés automatiquement lors de l'initialisation")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage automatique des doublons: {e}")
            # Ne pas lever l'exception car ce n'est pas critique
