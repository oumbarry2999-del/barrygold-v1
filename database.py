import sqlite3
import hashlib

DB_NAME = "barrygold.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Table utilisateurs
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prenom TEXT NOT NULL,
        nom TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Table comptes MT5
    c.execute('''CREATE TABLE IF NOT EXISTS mt5_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        login INTEGER,
        password TEXT,
        server TEXT,
        broker TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()
    print("Base de données créée ✓")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(prenom, nom, email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (prenom, nom, email, password) VALUES (?,?,?,?)",
                  (prenom, nom, email, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (email, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

init_db()
