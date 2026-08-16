import sqlite3
import pandas as pd

def run_queries():
    # Connect to the database
    conn = sqlite3.connect('db/tickets.db')
    
    print("--- 1. High Priority Tickets ---")
    # SQL: SELECT WHERE
    high_priority = pd.read_sql_query(
        "SELECT ticket_id, category, summary FROM tickets WHERE priority = 'High'", conn
    )
    print(high_priority.head())
    
    print("\n--- 2. Ticket Count by Category ---")
    # SQL: GROUP BY and COUNT
    category_count = pd.read_sql_query(
        "SELECT category, COUNT(*) as ticket_count FROM tickets GROUP BY category ORDER BY ticket_count DESC", conn
    )
    print(category_count)
    
    print("\n--- 3. Ticket Count by Priority ---")
    # SQL: GROUP BY and COUNT
    priority_count = pd.read_sql_query(
        "SELECT priority, COUNT(*) as ticket_count FROM tickets GROUP BY priority", conn
    )
    print(priority_count)
    
    print("\n--- 4. 10 Most Recent Tickets ---")
    # SQL: ORDER BY and LIMIT
    recent_tickets = pd.read_sql_query(
        "SELECT ticket_id, category, priority, created_at FROM tickets ORDER BY created_at DESC LIMIT 10", conn
    )
    print(recent_tickets)
    
    print("\n--- 5. Tickets Mentioning 'account' ---")
    # SQL: LIKE (Keyword search)
    keyword_search = pd.read_sql_query(
        "SELECT ticket_id, priority, original_text FROM tickets WHERE original_text LIKE '%account%'", conn
    )
    print(keyword_search.head())
    
    conn.close()

if __name__ == "__main__":
    run_queries()
