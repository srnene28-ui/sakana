import sqlite3
import os

DB_NAME = "data/xp.db"


def connect():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS xp_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        xp REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def add_xp(user_id, name, xp):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO xp_history (user_id, name, xp) VALUES (?, ?, ?)",
        (user_id, name, float(xp))
    )

    conn.commit()
    conn.close()


def get_latest_xp(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT xp
        FROM xp_history
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))

    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def get_best_xp(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(xp)
        FROM xp_history
        WHERE user_id=?
    """, (user_id,))

    row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else None


def get_ranking(limit=10):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT h.user_id, h.name, h.xp
        FROM xp_history h
        INNER JOIN (
            SELECT user_id, MAX(id) AS latest_id
            FROM xp_history
            GROUP BY user_id
        ) latest
        ON h.id = latest.latest_id
        ORDER BY h.xp DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()
    return rows


def get_user_stats(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT xp, created_at
        FROM xp_history
        WHERE user_id=?
        ORDER BY id ASC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()

    if not rows:
        return None

    xps = [row[0] for row in rows]

    latest_xp = xps[-1]
    best_xp = max(xps)
    count = len(xps)
    diff = xps[-1] - xps[-2] if len(xps) >= 2 else 0.0

    return {
        "latest_xp": latest_xp,
        "best_xp": best_xp,
        "count": count,
        "diff": diff,
        "first_date": rows[0][1],
        "last_date": rows[-1][1],
    }


def get_user_history(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT xp, created_at
        FROM xp_history
        WHERE user_id=?
        ORDER BY id ASC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows
def get_all_history():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, name, xp, created_at
        FROM xp_history
        ORDER BY id ASC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

def delete_latest_xp(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, xp
        FROM xp_history
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))

    row = cur.fetchone()

    if not row:
        conn.close()
        return None

    record_id, deleted_xp = row

    cur.execute(
        "DELETE FROM xp_history WHERE id=?",
        (record_id,)
    )

    conn.commit()
    conn.close()

    return deleted_xp

def get_history(user_id, limit=10, offset=0):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT xp, created_at
        FROM (
            SELECT xp, created_at, id
            FROM xp_history
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        )
        ORDER BY id ASC
    """, (user_id, limit, offset))

    rows = cur.fetchall()
    conn.close()

    return rows

def set_goal(user_id, goal):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            user_id INTEGER PRIMARY KEY,
            goal REAL
        )
    """)

    cur.execute("""
        INSERT INTO goals(user_id, goal)
        VALUES(?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET goal=excluded.goal
    """, (user_id, goal))

    conn.commit()
    conn.close()


def get_goal(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            user_id INTEGER PRIMARY KEY,
            goal REAL
        )
    """)

    cur.execute(
        "SELECT goal FROM goals WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()
    conn.close()

    return row[0] if row else None
def get_current_ranking_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT h.user_id, h.name, h.xp
        FROM xp_history h
        INNER JOIN (
            SELECT user_id, MAX(id) AS latest_id
            FROM xp_history
            GROUP BY user_id
        ) latest
        ON h.id = latest.latest_id
        ORDER BY h.xp DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows
