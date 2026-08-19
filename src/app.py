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

all_categories = df['category'].dropna().unique().tolist()
all_priorities = df['priority'].dropna().unique().tolist()

selected_categories = st.sidebar.multiselect("Category", all_categories, default=all_categories)
selected_priorities = st.sidebar.multiselect("Priority", all_priorities, default=all_priorities)
search_term = st.sidebar.text_input("Search Keyword")

# --- APPLY FILTERS ---
filtered_df = df[
    (df['category'].isin(selected_categories)) &
    (df['priority'].isin(selected_priorities))
]

if search_term:
    filtered_df = filtered_df[filtered_df['original_text'].str.contains(search_term, case=False, na=False)]

# --- DYNAMIC METRICS ---
total_tickets = len(filtered_df)
high_priority_count = len(filtered_df[filtered_df['priority'] == 'High'])
most_common_category = filtered_df['category'].mode()[0] if not filtered_df.empty else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("Total Tickets", total_tickets)
col2.metric("High Priority 🔴", high_priority_count)
col3.metric("Top Category", most_common_category)

# --- VISUAL POLISH: CATEGORY BAR CHART ---
st.markdown("---")
st.subheader("Ticket Distribution by Category")
if not filtered_df.empty:
    # Count tickets per category and display as a bar chart
    category_counts = filtered_df['category'].value_counts()
    st.bar_chart(category_counts)
else:
    st.write("No data to display.")

# --- VISUAL POLISH: COLOR-CODED PRIORITY IN TABLE ---
st.markdown("---")
st.subheader("Filtered Tickets")

# Create a copy of the dataframe to format the priority column with emojis for the table
display_df = filtered_df.copy()
def add_priority_emoji(priority):
    if priority == 'High': return '🔴 High'
    elif priority == 'Medium': return '🟡 Medium'
    elif priority == 'Low': return '🟢 Low'
    return priority

display_df['priority_label'] = display_df['priority'].apply(add_priority_emoji)

# Show the cleaner subset of columns
st.dataframe(display_df[['ticket_id', 'category', 'priority_label', 'summary']])

# --- EXPANDABLE TICKET DETAILS ---
st.subheader("Ticket Details")
if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        # Using visual icons in the expander title
        priority_icon = "🔴" if row['priority'] == 'High' else "🟡" if row['priority'] == 'Medium' else "🟢"
        
        with st.expander(f"Ticket #{row['ticket_id']} | {priority_icon} {row['priority']} Priority | {row['category']}"):
            st.write("**Original Message:**")
            st.info(row['original_text']) # Blue box
            
            st.write("**AI Suggested Response:**")
            # Color code the response box based on priority
            if row['priority'] == 'High':
                st.error(row['suggested_response']) # Red box for high priority
            elif row['priority'] == 'Medium':
                st.warning(row['suggested_response']) # Yellow box for medium
            else:
                st.success(row['suggested_response']) # Green box for low
else:
    st.write("No tickets match your current filters.")
