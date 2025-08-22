-- app/backend/database/schema.sql
-- Schéma complet de la base de données SQLite pour MicPlan

-- =====================================================
-- TABLE: users - Utilisateurs et authentification
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    role TEXT NOT NULL DEFAULT 'utilisateur' CHECK (role IN ('admin', 'superviseur', 'utilisateur')),
    secteur TEXT NOT NULL CHECK (secteur IN ('Biologie moléculaire', 'Sérologie infectieuse', 'Bactériologie')),
    is_active BOOLEAN DEFAULT 1,
    last_login DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE: positions - Postes et configurations
-- =====================================================
CREATE TABLE IF NOT EXISTS positions (
    id TEXT PRIMARY KEY, -- P1, P2, P3, etc.
    name TEXT NOT NULL,
    secteur TEXT NOT NULL CHECK (secteur IN ('Biologie moléculaire', 'Sérologie infectieuse', 'Bactériologie')),
    priority INTEGER NOT NULL CHECK (priority >= 1 AND priority <= 10),
    description TEXT,
    min_agents INTEGER DEFAULT 1 CHECK (min_agents >= 1),
    max_agents INTEGER DEFAULT 1 CHECK (max_agents >= 1),
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE: position_frequency_config - Configuration des fréquences des postes
-- =====================================================
CREATE TABLE IF NOT EXISTS position_frequency_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id TEXT REFERENCES positions(id) ON DELETE CASCADE,
    week_frequency TEXT NOT NULL CHECK (week_frequency IN ('Toutes les semaines', 'Une semaine sur deux', 'Une semaine sur trois', 'Une semaine sur quatre')),
    weekdays TEXT NOT NULL, -- JSON array: '["lundi", "mardi", "mercredi"]'
    morning BOOLEAN DEFAULT 1,
    afternoon BOOLEAN DEFAULT 1,
    evening BOOLEAN DEFAULT 0,
    weeks TEXT, -- JSON array: '[1,3,5,7]' pour une semaine sur deux
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE: availability - Disponibilités des utilisateurs
-- =====================================================
CREATE TABLE IF NOT EXISTS availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    morning BOOLEAN DEFAULT 0,
    afternoon BOOLEAN DEFAULT 0,
    evening BOOLEAN DEFAULT 0,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, date)
);

-- =====================================================
-- TABLE: availability_preferences - Préférences de disponibilité
-- =====================================================
CREATE TABLE IF NOT EXISTS availability_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    weekday INTEGER NOT NULL CHECK (weekday >= 1 AND weekday <= 7), -- 1=lundi, 7=dimanche
    morning BOOLEAN DEFAULT 1,
    afternoon BOOLEAN DEFAULT 1,
    evening BOOLEAN DEFAULT 0,
    priority INTEGER DEFAULT 5 CHECK (priority >= 1 AND priority <= 10),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, weekday)
);

-- =====================================================
-- TABLE: planning - Planning effectif des postes
-- =====================================================
CREATE TABLE IF NOT EXISTS planning (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    position_id TEXT REFERENCES positions(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    shift TEXT NOT NULL CHECK (shift IN ('morning', 'afternoon', 'evening')),
    status TEXT DEFAULT 'planned' CHECK (status IN ('planned', 'confirmed', 'completed', 'cancelled')),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, position_id, shift)
);

-- =====================================================
-- TABLE: absences - Absences et congés
-- =====================================================
CREATE TABLE IF NOT EXISTS absences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('congé', 'maladie', 'formation', 'autre')),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'cancelled')),
    approved_by INTEGER REFERENCES users(id),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date >= start_date)
);

-- =====================================================
-- TABLE: leave_requests - Demandes de congés
-- =====================================================
CREATE TABLE IF NOT EXISTS leave_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('congé payé', 'RTT', 'congé sans solde', 'autre')),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'cancelled')),
    requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME,
    processed_by INTEGER REFERENCES users(id),
    notes TEXT,
    CHECK (end_date >= start_date)
);

-- =====================================================
-- TABLE: schedules - Horaires et plannings types
-- =====================================================
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_by INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE: schedule_templates - Modèles d'horaires
-- =====================================================
CREATE TABLE IF NOT EXISTS schedule_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_id INTEGER REFERENCES schedules(id) ON DELETE CASCADE,
    weekday INTEGER NOT NULL CHECK (weekday >= 1 AND weekday <= 7),
    start_time TIME,
    end_time TIME,
    break_start TIME,
    break_end TIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE: audit_logs - Historique des actions et modifications
-- =====================================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    action TEXT NOT NULL,
    table_name TEXT NOT NULL,
    record_id TEXT,
    old_values TEXT, -- JSON string
    new_values TEXT, -- JSON string
    ip_address TEXT,
    user_agent TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE: schema_migrations - Gestion des migrations
-- =====================================================
CREATE TABLE IF NOT EXISTS schema_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    checksum TEXT,
    execution_time_ms INTEGER
);

-- =====================================================
-- INDEXES pour les performances
-- =====================================================

-- Index sur les dates pour le planning et la disponibilité
CREATE INDEX IF NOT EXISTS idx_planning_date ON planning(date);
CREATE INDEX IF NOT EXISTS idx_availability_date ON availability(date);
CREATE INDEX IF NOT EXISTS idx_absences_dates ON absences(start_date, end_date);

-- Index sur les utilisateurs
CREATE INDEX IF NOT EXISTS idx_planning_user ON planning(user_id);
CREATE INDEX IF NOT EXISTS idx_availability_user ON availability(user_id);
CREATE INDEX IF NOT EXISTS idx_absences_user ON absences(user_id);

-- Index sur les postes
CREATE INDEX IF NOT EXISTS idx_planning_position ON planning(position_id);
CREATE INDEX IF NOT EXISTS idx_positions_secteur ON positions(secteur);

-- Index sur les audits
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);

-- =====================================================
-- TRIGGERS pour la mise à jour automatique des timestamps
-- =====================================================

-- Trigger pour mettre à jour updated_at
CREATE TRIGGER IF NOT EXISTS update_users_updated_at 
    AFTER UPDATE ON users
    BEGIN
        UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_positions_updated_at 
    AFTER UPDATE ON positions
    BEGIN
        UPDATE positions SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_position_frequency_config_updated_at 
    AFTER UPDATE ON position_frequency_config
    BEGIN
        UPDATE position_frequency_config SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_availability_updated_at 
    AFTER UPDATE ON availability
    BEGIN
        UPDATE availability SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_availability_preferences_updated_at 
    AFTER UPDATE ON availability_preferences
    BEGIN
        UPDATE availability_preferences SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_planning_updated_at 
    AFTER UPDATE ON planning
    BEGIN
        UPDATE planning SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_absences_updated_at 
    AFTER UPDATE ON absences
    BEGIN
        UPDATE absences SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_leave_requests_updated_at 
    AFTER UPDATE ON leave_requests
    BEGIN
        UPDATE leave_requests SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_schedules_updated_at 
    AFTER UPDATE ON schedules
    BEGIN
        UPDATE schedules SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- =====================================================
-- VUES utiles pour simplifier les requêtes
-- =====================================================

-- Vue pour les postes avec leur configuration de fréquence
CREATE VIEW IF NOT EXISTS positions_with_frequency AS
SELECT 
    p.*,
    pfc.week_frequency,
    pfc.weekdays,
    pfc.morning,
    pfc.afternoon,
    pfc.evening,
    pfc.weeks
FROM positions p
LEFT JOIN position_frequency_config pfc ON p.id = pfc.position_id
WHERE p.is_active = 1;

-- Vue pour le planning complet
CREATE VIEW IF NOT EXISTS planning_complete AS
SELECT 
    pl.*,
    p.name as position_name,
    p.secteur as position_secteur,
    u.username,
    u.first_name,
    u.last_name,
    u.secteur as user_secteur
FROM planning pl
JOIN positions p ON pl.position_id = p.id
JOIN users u ON pl.user_id = u.id;

-- =====================================================
-- DONNÉES INITIALES
-- =====================================================

-- Insérer un utilisateur admin par défaut
INSERT OR IGNORE INTO users (username, password_hash, role, secteur, first_name, last_name) 
VALUES ('admin', 'pbkdf2:sha256:600000$default_hash', 'admin', 'Biologie moléculaire', 'Administrateur', 'Système');

-- Insérer quelques postes par défaut
INSERT OR IGNORE INTO positions (id, name, secteur, priority, description) VALUES
('P1', 'Poste PCR - Quotidien', 'Biologie moléculaire', 9, 'Poste de PCR quotidien, matin et après-midi'),
('P2', 'Poste Sérologie - Hebdomadaire', 'Sérologie infectieuse', 7, 'Poste de sérologie une semaine sur deux'),
('P3', 'Poste Bactériologie - Mensuel', 'Bactériologie', 5, 'Poste de bactériologie mensuel');

-- Configuration des fréquences pour les postes par défaut
INSERT OR IGNORE INTO position_frequency_config (position_id, week_frequency, weekdays, morning, afternoon, evening) VALUES
('P1', 'Toutes les semaines', '["lundi", "mardi", "mercredi", "jeudi", "vendredi"]', 1, 1, 0),
('P2', 'Une semaine sur deux', '["mardi", "mercredi"]', 0, 1, 0),
('P3', 'Une semaine sur quatre', '["lundi"]', 1, 1, 1);
