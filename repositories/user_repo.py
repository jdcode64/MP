from database.connection import get_connection

def create_user(first_name, last_name, username, email, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # SQLite doesn't strictly support %s placeholders natively if we aren't careful,
        # but with psycopg for postgres we need %s.
        # For simplicity, we can do an abstraction if needed,
        # but let's just format it correctly depending on the connection type.
        # Actually, python sqlite supports ? and psycopg supports %s
        # Let's write a quick helper in a repository base or here.
        is_pg = 'psycopg' in str(type(conn))

        if is_pg:
            cursor.execute(
                "INSERT INTO users (first_name, last_name, username, email, password_hash) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (first_name, last_name, username, email, password_hash)
            )
            return cursor.fetchone()['id']
        else:
            cursor.execute(
                "INSERT INTO users (first_name, last_name, username, email, password_hash) VALUES (?, ?, ?, ?, ?)",
                (first_name, last_name, username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    is_pg = 'psycopg' in str(type(conn))
    try:
        if is_pg:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        else:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        cursor.close()
        conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users ORDER BY id")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        cursor.close()
        conn.close()

def update_user_status(user_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    is_pg = 'psycopg' in str(type(conn))
    try:
        if is_pg:
            cursor.execute("UPDATE users SET status = %s WHERE id = %s", (status, user_id))
        else:
            cursor.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
