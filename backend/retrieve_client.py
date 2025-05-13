import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.connection import get_connection
from utils.encryption import get_cipher, decrypt_field

# Load environment variables
load_dotenv()

def retrieve_client_details(client_id: int):
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY not found in environment variables.")
    
    cipher = get_cipher(key.encode())

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT client_id, encrypted_clientname, encrypted_password, encrypted_email, created_on
                FROM client_credentials
                WHERE client_id = %s
            """, (client_id,))
            
            row = cur.fetchone()
            if row is None:
                return f"Client ID {client_id} not found."
            
            return {
                "client_id": row[0],
                "clientname": decrypt_field(cipher, row[1]),  # Ensure this is in bytes
                "password": decrypt_field(cipher, row[2]),
                "email": decrypt_field(cipher, row[3]),
                "created_on": row[4]
            }

# Optional CLI interface
if __name__ == "__main__":
    cid = int(input("Enter client ID: "))
    print(retrieve_client_details(cid))
