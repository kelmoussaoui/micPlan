# deploy_config.py
# Configuration pour le déploiement portable

import os

# Configuration du déploiement
DEPLOY_CONFIG = {
    'app_name': 'micPlan',
    'version': '1.0.0',
    'description': 'Application de planification des postes de laboratoire',
    'author': 'Équipe micPlan',
    
    # Fichiers à inclure dans l'exécutable
    'include_files': [
        'resources',
        'app',
        'config.py',
        'run.py'
    ],
    
    # Modules Python à inclure explicitement
    'hidden_imports': [
        'streamlit',
        'pandas',
        'numpy',
        'sqlite3',
        'passlib',
        'bcrypt',
        'python-dateutil',
        'pytz',
        'app.backend.database',
        'app.frontend.pages',
        'app.frontend.auth',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.runtime.scriptrunner.script_run_context',
    ],
    
    # Fichiers à exclure pour réduire la taille
    'exclude_patterns': [
        '*.pyc',
        '__pycache__',
        '*.log',
        '*.tmp',
        'tests',
        'docs',
        '.git'
    ],
    
    # Configuration Windows spécifique
    'windows_config': {
        'console': False,  # Pas de console
        'icon': 'resources/images/logo.ico' if os.path.exists('resources/images/logo.ico') else None,
        'uac_admin': False,  # Pas besoin de droits admin
        'version_file': None,
    }
}

# Configuration de l'optimisation
OPTIMIZATION_CONFIG = {
    'strip': True,  # Supprimer les symboles de debug
    'upx': True,    # Compresser avec UPX
    'upx_exclude': [],  # Fichiers à ne pas compresser
    'onefile': False,   # Dossier complet (plus portable)
    'onedir': True,     # Dossier avec tous les fichiers
}
