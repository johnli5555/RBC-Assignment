ALTER TABLE client_credentials
ADD COLUMN encrypted_clientname BYTEA,
ADD COLUMN encrypted_password BYTEA,
ADD COLUMN encrypted_email BYTEA;