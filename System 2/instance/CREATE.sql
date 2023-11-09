CREATE TABLE dispositivo (
	id VARCHAR(36) NOT NULL, 
	nome VARCHAR(50) NOT NULL, 
	codigo VARCHAR(50) NOT NULL, 
	marca VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id)
)

CREATE TABLE localizacao (
	id varchar(36) primary key
	,id_dispositivo varchar(36)
	,latitude real
	,longitude real
	
	,FOREIGN KEY (id_dispositivo) REFERENCES dispositivo(id)
)