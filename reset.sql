DROP DATABASE IF EXISTS customers_db;
REASSIGN OWNED BY customers_admin TO postgres;
DROP OWNED BY customers_admin;
DROP ROLE IF EXISTS customers_admin;

CREATE USER customers_admin WITH PASSWORD 'admin';
CREATE DATABASE customers_db OWNER customers_admin;
