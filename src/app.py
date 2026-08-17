import streamlit as st
import pandas as pd
import sqlite3

# 1. Connect to the database and load the data
conn = sqlite3.connect('db/tickets.db')
# We use Pandas to execute the SQL query and convert it directly into a DataFrame
df = pd.read_sql_query("SELECT * FROM tickets", conn)
conn.close()

# 2. Set the Page Title
st.title("AI Customer Support Ticket Analyzer")

# 3. Calculate Summary Metrics
total_tickets = len(df)
# Filter the DataFrame to count only 'High' priority rows
high_priority_count = len(df[df['priority'] == 'High'])
# Find the most common category (mode returns a series, we grab the first item)
most_common_category = df['category'].mode()[0] if not df.empty else "N/A"

# 4. Display the Metrics at the top of the page
col1, col2, col3 = st.columns(3)
col1.metric("Total Tickets", total_tickets)
col2.metric("High Priority", high_priority_count)
col3.metric("Top Category", most_common_category)

# 5. Display the full table
st.subheader("All Tickets")
st.dataframe(df)
