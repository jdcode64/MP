from database.connection import get_connection

def get_scoring_config():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT key_name, key_value FROM configurations")
        rows = cursor.fetchall()
        return {row['key_name']: row['key_value'] for row in rows}
    finally:
        cursor.close()
        conn.close()

def update_scoring_config(configs):
    conn = get_connection()
    cursor = conn.cursor()
    is_pg = 'psycopg' in str(type(conn))
    try:
        for key, value in configs.items():
            if is_pg:
                cursor.execute(
                    "UPDATE configurations SET key_value = %s WHERE key_name = %s",
                    (value, key)
                )
            else:
                cursor.execute(
                    "UPDATE configurations SET key_value = ? WHERE key_name = ?",
                    (value, key)
                )
        conn.commit()
    finally:
        cursor.close()
        conn.close()
