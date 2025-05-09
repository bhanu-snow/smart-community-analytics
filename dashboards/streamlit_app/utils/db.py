import psycopg2
import pandas as pd
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def run_query(sql):
    conn = get_connection()
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df
