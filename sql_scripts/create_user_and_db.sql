-- This file creates user client_admin, creates the database client_db and grants the user full access to the database

-- Create a user with a password
CREATE USER client_admin WITH PASSWORD 'secure_password';
-- Create the database
CREATE DATABASE clientdb OWNER client_admin;
-- Grant all privileges on the DB to the user
GRANT ALL PRIVILEGES ON DATABASE ClientDB TO client_admin;