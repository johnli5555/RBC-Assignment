from dotenv import load_dotenv
from db.connection import get_connection
from utils.encryption import get_cipher, encrypt_field
import os

# Load the .env file
load_dotenv()

# Now retrieve the key
key = os.getenv("ENCRYPTION_KEY").encode()
cipher = get_cipher(key)

with get_connection() as conn:
    with conn.cursor() as cur:
        # Step 1: Fetch all existing client data
        cur.execute("""
            SELECT client_id, clientname, password, email, created_on
            FROM client_credentials
        """)
        rows = cur.fetchall()

        # Step 2: Encrypt and update rows
        for row in rows:
            client_id, clientname, password, email, created_on = row

            cur.execute("""
                UPDATE client_credentials
                SET encrypted_clientname = %s,
                    encrypted_password = %s,
                    encrypted_email = %s
                WHERE client_id = %s
            """, (
                encrypt_field(cipher, clientname),
                encrypt_field(cipher, password),
                encrypt_field(cipher, email),
                client_id
            ))

        # Step 3: Drop old sensitive columns
        cur.execute("""
            ALTER TABLE client_credentials
            DROP COLUMN clientname,
            DROP COLUMN password,
            DROP COLUMN email
        """)

    conn.commit()
