PRAGMA FOREIGN_KEYS = ON;

CREATE TABLE IF NOT EXISTS dispositivo (
	id_dispositivo CHAR(36) PRIMARY KEY
	,marca CHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS dispo_info (
	id_dispositivo CHAR(36) PRIMARY KEY
	,quantidade_pos NUMERIC DEFAULT(0)
	,total_km REAL DEFAULT(0)
	,data TEXT
);