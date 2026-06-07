import psycopg2
import psycopg2.extras
import streamlit as st
import os

# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

def get_connection():
    """Return a live psycopg2 connection using st.secrets or env vars."""
    try:
        conn = psycopg2.connect(
            host=st.secrets.get("DB_HOST", os.getenv("DB_HOST", "localhost")),
            port=st.secrets.get("DB_PORT", os.getenv("DB_PORT", 5432)),
            database=st.secrets.get("DB_NAME", os.getenv("DB_NAME", "school_erp")),
            user=st.secrets.get("DB_USER", os.getenv("DB_USER", "postgres")),
            password=st.secrets.get("DB_PASSWORD", os.getenv("DB_PASSWORD", "atharva")),
        )
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None


def run_query(query: str, params=None, fetch: bool = True):
    """Execute a query and optionally return rows as list-of-dicts."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                rows = cur.fetchall()
                return [dict(r) for r in rows]
            conn.commit()
            return []
    except Exception as e:
        conn.rollback()
        st.error(f"❌ Query error: {e}")
        return []
    finally:
        conn.close()


def execute(query: str, params=None) -> bool:
    """Execute INSERT / UPDATE / DELETE. Returns True on success."""
    conn = get_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        st.error(f"❌ Execute error: {e}")
        return False
    finally:
        conn.close()
