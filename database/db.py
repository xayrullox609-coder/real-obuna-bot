"""
database/db.py
Real Obuna Bot — SQLite ma'lumotlar bazasi
"""

import sqlite3
from pathlib import Path


# ============================================================
# DATABASE SOZLAMALARI
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "bot.db"


# ============================================================
# CONNECTION
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # SQLite foreign keylarni yoqish
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ============================================================
# DATABASE INIT
# ============================================================

def init_db():
    """
    Barcha kerakli jadvallarni yaratadi.
    Agar jadval mavjud bo'lsa, qaytadan yaratmaydi.
    """

    with get_connection() as conn:

        # ====================================================
        # USERS
        # ====================================================

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,

                coins INTEGER DEFAULT 0,

                is_vip INTEGER DEFAULT 0,
                vip_until TEXT,

                last_daily TEXT,
                last_vip_daily TEXT,

                referred_by INTEGER,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ====================================================
        # TASKS
        # ====================================================

        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                task_type TEXT NOT NULL,

                target TEXT NOT NULL,

                reward REAL DEFAULT 0,

                required_count INTEGER DEFAULT 1,

                is_active INTEGER DEFAULT 1,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ====================================================
        # TASK COMPLETIONS
        # ====================================================

        conn.execute("""
            CREATE TABLE IF NOT EXISTS task_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,
                task_id INTEGER NOT NULL,

                completed_at TEXT DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(user_id, task_id),

                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE,

                FOREIGN KEY(task_id)
                    REFERENCES tasks(id)
                    ON DELETE CASCADE
            )
        """)

        # ====================================================
        # ORDERS
        # ====================================================

        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                task_type TEXT,
                target TEXT,

                quantity INTEGER DEFAULT 0,

                price REAL DEFAULT 0,

                status TEXT DEFAULT 'pending',

                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ====================================================
        # PAYMENTS
        # ====================================================

        conn.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                amount REAL DEFAULT 0,

                stars INTEGER DEFAULT 0,

                status TEXT DEFAULT 'pending',

                payload TEXT,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ====================================================
        # PREMIUM EMOJIS
        # ====================================================

        conn.execute("""
            CREATE TABLE IF NOT EXISTS premium_emojis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                emoji TEXT NOT NULL,

                price INTEGER DEFAULT 0,

                is_active INTEGER DEFAULT 1,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ====================================================
        # PROMOCODES
        # ====================================================

        conn.execute("""
            CREATE TABLE IF NOT EXISTS promo_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                code TEXT NOT NULL UNIQUE,

                is_active INTEGER DEFAULT 1,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ====================================================
        # PROMO CLAIMS
        # ====================================================

        conn.execute("""
            CREATE TABLE IF NOT EXISTS promo_claims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                promo_id INTEGER NOT NULL,

                claimed_at TEXT DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(user_id, promo_id),

                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE,

                FOREIGN KEY(promo_id)
                    REFERENCES promo_codes(id)
                    ON DELETE CASCADE
            )
        """)

        # ====================================================
        # INDEXLAR
        # ====================================================

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username
            ON users(username)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_active
            ON tasks(is_active)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_promo_active
            ON promo_codes(is_active)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_promo_claims_user
            ON promo_claims(user_id)
        """)

        conn.commit()


# ============================================================
# DATABASE TEKSHIRISH
# ============================================================

def database_exists():
    """
    Database fayli mavjudligini tekshiradi.
    """

    return DB_PATH.exists()


# ============================================================
# DATABASE RESET
# ============================================================

def reset_database():
    """
    DIQQAT:
    Barcha ma'lumotlarni o'chiradi.

    Faqat test vaqtida ishlatish kerak.
    """

    if DB_PATH.exists():
        DB_PATH.unlink()

    init_db()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    init_db()

    print("================================")
    print("Real Obuna Bot Database")
    print("================================")
    print(f"Database: {DB_PATH}")
    print("Database muvaffaqiyatli ishga tushdi.")