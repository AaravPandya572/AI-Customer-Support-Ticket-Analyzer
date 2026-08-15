import sqlite3
import json
import os
from datetime import datetime

def create_table():
    # Connects to the database (and creates the file if it doesn't exist)
    conn = sqlite3.connect('db/tickets.db')
    cursor = conn.cursor()
    
    # Create the table matching your Day 11 schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT,
            original_text TEXT,
            summary TEXT,
            category TEXT,
            priority TEXT,
            suggested_response TEXT,
            created_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_ticket(data):
    conn = sqlite3.connect('db/tickets.db')
    cursor = conn.cursor()
    
    # Using parameterized queries (?) to prevent SQL injection
    cursor.execute('''
        INSERT INTO tickets (
            ticket_id, original_text, summary, category, priority, suggested_response, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('ticket_id'),
        data.get('original_text'),
        data.get('summary'),
        data.get('category'),
        data.get('priority'),
        data.get('suggested_response'),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Automatically stamps the current time
    ))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # 1. Ensure the db folder exists
    os.makedirs('db', exist_ok=True)
    
    # 2. Create the table
    print("Setting up database and creating tickets table...")
    create_table()
    
    # 3. Load the JSON data
    print("Loading AI results from JSON...")
    with open('data/processed/ai_results.json', 'r') as f:
        results = json.load(f)
        
    # 4. Loop through and insert each record
    print(f"Inserting {len(results)} records into the database...")
    for ticket in results:
        insert_ticket(ticket)
        
    print("Database population complete! Open db/tickets.db using the SQLite Viewer extension to verify.")
