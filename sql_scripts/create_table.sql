-- Create client credentials table
CREATE TABLE client_credentials (
    client_id SERIAL PRIMARY KEY,
    clientname TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    encrypted_clientname BYTEA,
    encrypted_password BYTEA,
    encrypted_email BYTEA
);