import streamlit as st
import pandas as pd
import sqlite3

# 1. Connect and load data
conn = sqlite3.connect('db/tickets.db')
df = pd.read_sql_query("SELECT * FROM tickets", conn)
conn.close()

st.title("AI Customer Support Ticket Analyzer")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Tickets")

# Get unique categories and priorities directly from the dataframe
all_categories = df['category'].dropna().unique().tolist()
all_priorities = df['priority'].dropna().unique().tolist()

# Create multi-select filters (defaulting to showing everything)
selected_categories = st.sidebar.multiselect("Category", all_categories, default=all_categories)
selected_priorities = st.sidebar.multiselect("Priority", all_priorities, default=all_priorities)

# Create a text input for keyword search
search_term = st.sidebar.text_input("Search Keyword")

# --- APPLY FILTERS TO DATAFRAME ---
# Filter by category and priority
filtered_df = df[
    (df['category'].isin(selected_categories)) &
    (df['priority'].isin(selected_priorities))
]

# Filter by keyword if the user typed something in
if search_term:
    filtered_df = filtered_df[filtered_df['original_text'].str.contains(search_term, case=False, na=False)]

# --- DYNAMIC METRICS ---
total_tickets = len(filtered_df)
high_priority_count = len(filtered_df[filtered_df['priority'] == 'High'])
# Handle the case where the filter returns an empty dataframe
most_common_category = filtered_df['category'].mode()[0] if not filtered_df.empty else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("Total Tickets", total_tickets)
col2.metric("High Priority", high_priority_count)
col3.metric("Top Category", most_common_category)

# --- DISPLAY TABLE ---
st.subheader("Filtered Tickets")
# Showing a cleaner subset of columns in the main table
st.dataframe(filtered_df[['ticket_id', 'category', 'priority', 'summary']])

# --- EXPANDABLE TICKET DETAILS ---
st.subheader("Ticket Details")
if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        # Create a dropdown for each ticket
        with st.expander(f"Ticket #{row['ticket_id']} - {row['priority']} Priority ({row['category']})"):
            st.write("**Original Message:**")
            st.info(row['original_text'])
            st.write("**AI Suggested Response:**")
            st.success(row['suggested_response'])
else:
    st.write("No tickets match your current filters.")
