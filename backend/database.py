import mysql.connector
from config import DB_CONFIG

def connect_db():
    """Connect to MySQL Database"""
    return mysql.connector.connect(**DB_CONFIG)

def create_tables():
    """Create portfolios table if not exists"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        ticker VARCHAR(10) NOT NULL,
        quantity FLOAT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

def add_portfolio(user_id, ticker, quantity):
    """Insert a portfolio entry into the database"""
    conn = connect_db()
    cursor = conn.cursor()

    sql = "INSERT INTO portfolios (user_id, ticker, quantity) VALUES (%s, %s, %s)"
    cursor.execute(sql, (user_id, ticker, quantity))

    conn.commit()
    conn.close()

def get_portfolio(user_id):
    """Retrieve user portfolio from the database"""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM portfolios WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    results = cursor.fetchall()

    conn.close()
    return results
