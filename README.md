# RBC-Assignment

RBC-Engineering posgres project

Here are the instructions to replicate the db (Note, these instructions are for macOS!)

# ##################################
Section 1: setting up postgres
# ##################################

1. Install postgres

2. connect to postgres via command "psql postgres" and run sql_scripts/create_user_and_db.sql

3. exit via command "\q" and edit the authentication config so that password is required for all local TCP connections (for security reasons)

   this can be done by running:

   nano /opt/homebrew/var/postgresql@14/pg_hba.conf

   and changing trust to md5 for 

    local

    IPv4 local connections:

    IPv6 local connections:

4. reload postgres and log in using command "psql -h localhost -U client_admin -d clientdb"

5. Create client credentials tables by running sql_scripts/create_table.sql  

# ##################################
Section 2: loading data and encrypting using python
# ##################################

1. set up virtual environment (optional but recommended)

    python3 -m venv venv
    
    source venv/bin/activate

2. run "pip install -r req.txt"

3. load tables from csv by running import_csv.py

4. generate encryption key using encrypt_data.py. The key is stored in .env file

5. load the new columns (encrypted_clientname, encrypted_password, and encrypted_email) and delete the old ones using encrypt_data.py

# ##################################
Section 3: python functions
# ##################################

1. retrieve client fields takes a client_id and returns all the information associated with that id

2. alter client field takes an id, a field, and a value and updates the field to that new value

# ##################################
Section 4: flask app and frontend
# ##################################

1. the frontend flask application can be started by running auth_app.py

2. the application can be found on http://127.0.0.1:5000

In the homepage, the user can login using their id and respective password. Once logged in they can change their password and log out.

# ##################################
Section 5: problems encountered and decisions made
# ##################################

1. malformed row in CSV

Solution: fixed row by removing extra comma and made new csv called client_data_cleaned.csv

2. Encryption key handling

Solution: Encryption key is stored in the env variable so that it won't be leaked in the case of a database breach. For larger applications it should be stored on vault or other online key storage distributors such as AWS KMS or Kubernetes key injections.

It is also not a good idea for users to have to pass the secret key as it is very inconvenient for them to need this in order to access their information. As a result, it is dealt with internally.


