-- creating a table with attributes

CREATE TABLE users IF NOT EXISTS (
	id INT NOT NULL AUTO INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255)
);
