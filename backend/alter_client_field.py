import os
import sys
from dotenv import load_dotenv
import psycopg2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.connection import get_connection  # Assumed database connection handler
from utils.encryption import get_cipher, encrypt_field  # Assumed encryption functions

# Load environment variables
load_dotenv()

def alter_client_field(client_id: int, field_name: str, new_value: str):
    # Ensure that the field name is valid
    valid_fields = ['clientname', 'password', 'email']
    if field_name not in valid_fields:
        return f"Invalid field name. Please choose from {', '.join(valid_fields)}."

    # Retrieve the encryption key from environment variables
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY not found in environment variables.")
    
    # Get the cipher based on the encryption key
    cipher = get_cipher(key.encode())
    
    # Encrypt the new value using the encrypt_field method
    encrypted_value = encrypt_field(cipher, new_value)

    with get_connection() as conn:
        with conn.cursor() as cur:
            # Check if client exists
            cur.execute("""
                SELECT client_id FROM client_credentials WHERE client_id = %s
            """, (client_id,))
            if cur.fetchone() is None:
                return f"Client ID {client_id} not found."
            
            # Update the specified field
            update_query = f"UPDATE client_credentials SET encrypted_{field_name} = %s WHERE client_id = %s"
            cur.execute(update_query, (encrypted_value, client_id))
            conn.commit()

            return f"Client {field_name} has been successfully updated."

# Optional CLI interface
if __name__ == "__main__":
    client_id = int(input("Enter client ID: "))
    field_name = input("Enter the field name you want to alter (clientname, password, email): ")
    new_value = input(f"Enter the new value for {field_name}: ")
    
    result = alter_client_field(client_id, field_name, new_value)
    print(result)
