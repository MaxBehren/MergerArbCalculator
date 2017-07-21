DROP TABLE IF EXISTS universe;

CREATE TABLE universe (
	Target varchar(5) PRIMARY KEY,
	Acquirer TINYTEXT,
	Acq_public BOOLEAN,
	Type ENUM('1','2','3'),
	Cash DECIMAL(6,2),
	Stock DECIMAL(8,4)
);