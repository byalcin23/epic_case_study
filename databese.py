import os
import time
import psycopg2

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "appdb")
DB_USER = os.getenv("POSTGRES_USER", "appuser")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "apppassword")

def get_connection():
    while True:
        try:
            return psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
        except psycopg2.OperationalError:
            print("DB Connection failed, retrying in 2 seconds...")
            time.sleep(2)

def init_db():
    query = """
    CREATE TABLE IF NOT EXISTS pets (
        id BIGINT PRIMARY KEY,
        name TEXT,
        status TEXT,
        pet_category TEXT,
        name_character_count INTEGER
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    print("DB init completed, table is ready.")

def save_pet_to_db(pet_id, name, status, category, char_count):
    query = """
    INSERT INTO pets (id, name, status, pet_category, name_character_count)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (pet_id, name, status, category, char_count))
            if cur.rowcount > 0:
                print(f"[DB] New record inserted: {pet_id} - {name}")
            conn.commit()
