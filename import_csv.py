import pandas as pd
from db.connection import get_connection

# Load CSV into a DataFrame
df = pd.read_csv('raw_data/client_data_cleaned.csv', on_bad_lines='warn')

conn = get_connection()
cur = conn.cursor()

# Insert df into database
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO client_credentials (client_id, clientname, password, email, created_on)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        row['client_id'], row['clientname'], row['password'],
        row['email'], row['created_on']
    ))

conn.commit()
cur.close()
conn.close()
print("CSV data imported successfully.")