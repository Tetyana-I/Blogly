-- from the terminal run:
-- psql < blogly.sql

DROP DATABASE IF EXISTS blogly;

CREATE DATABASE blogly;

\c blogly

CREATE TABLE users
(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(30) NOT NULL
);

INSERT INTO users
  (first_name, last_name)
VALUES
  ('Robert', 'Brown'), ('Yose','Libman');