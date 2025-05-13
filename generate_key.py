from cryptography.fernet import Fernet
from pathlib import Path

def generate_and_store_key(env_path=".env"):
    key = Fernet.generate_key().decode()

    # Create .env file if it doesn't exist
    env_file = Path(env_path)
    if env_file.exists():
        # Check if key already exists
        content = env_file.read_text()
        if "ENCRYPTION_KEY=" in content:
            print("ENCRYPTION_KEY already exists in .env. Aborting to avoid overwrite.")
            return
    else:
        env_file.touch()

    # Append or write the key
    with env_file.open("a") as f:
        f.write(f'\nENCRYPTION_KEY="{key}"\n')

    print(f"Encryption key generated and stored in '{env_path}'.")
    print("Make sure to keep this file secure and add it to your .gitignore!")

if __name__ == "__main__":
    generate_and_store_key()
