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
