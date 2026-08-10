import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from google import genai

def get_few_shot_prompt(ticket_text):
    # This is the exact same rock-solid prompt from yesterday
    return f"""You are a customer support analyst. Read the customer ticket and respond ONLY with a valid JSON object. 
Fields required: "summary", "category" (Billing, Technical Issue, Delivery Problem, Account Access, General Query), "priority" (High, Medium, Low), and "suggested_response".

Rules:
1. If the ticket is vague or lacks context, set category to "General Query" and priority to "Medium".
2. Respond with ONLY the JSON object.

--- Example 1 (Standard Issue) ---
Ticket: 'My screen went black and won't turn on.'
Response:
{{
    "summary": "The customer is reporting a black screen that will not power on.",
    "category": "Technical Issue",
    "priority": "High",
    "suggested_response": "I am so sorry your screen is unresponsive. Let's try a hard reset first. Please hold the power button for 10 seconds."
}}

--- Example 2 (Delivery Issue) ---
Ticket: 'Where is my order? It was supposed to be here yesterday.'
Response:
{{
    "summary": "The customer is asking about an overdue delivery.",
    "category": "Delivery Problem",
    "priority": "High",
    "suggested_response": "I apologize for the delay in your delivery. Let me pull up your tracking information right away to see where it is."
}}

--- Example 3 (The Vague Ticket) ---
Ticket: 'This is ridiculous.'
Response:
{{
    "summary": "The customer is expressing extreme dissatisfaction without specifying the issue.",
    "category": "General Query",
    "priority": "Medium",
    "suggested_response": "I am very sorry you are having a frustrating experience. Could you please provide a bit more detail about what happened so I can help resolve this?"
}}

--- Actual Ticket ---
Ticket: '{ticket_text}'
Response:"""

def main():
    load_dotenv()
    client = genai.Client()

    print("Loading sample tickets...")
    df = pd.read_csv("data/processed/tickets_sample.csv")
    
    # To respect API rate limits and test safely, we will only process the first 10 rows for now.
    # We use explicit iteration to control the flow step-by-step.
    df_subset = df.head(10)
    
    # We will store the AI's structured responses in this list
    results_list = []

    print(f"Starting batch processing for {len(df_subset)} tickets...\n")

    for index, row in df_subset.iterrows():
        ticket_id = row['tweet_id']
        ticket_text = row['text']
        
        print(f"Processing Ticket {ticket_id} (Row {index + 1}/10)...")
        prompt = get_few_shot_prompt(ticket_text)
        
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            
            raw_output = response.text
            clean_output = raw_output.replace("```json", "").replace("```", "").strip()
            
            # Parse the JSON and attach the original ticket ID so we can track it
            parsed_data = json.loads(clean_output)
            parsed_data['tweet_id'] = ticket_id
            
            results_list.append(parsed_data)
            
        except Exception as e:
            # If the API fails or JSON breaks, we catch the error, print it, and KEEP GOING.
            print(f"[ERROR] Failed on ticket {ticket_id}: {e}")
        
        # Pause for 15 seconds between requests to safely stay under the 5-per-minute limit
        time.sleep(15)


    # Convert the list of dictionary results back into a clean Pandas DataFrame
    results_df = pd.DataFrame(results_list)
    
    # Save the final categorized data
    output_path = "data/processed/analyzed_tickets.csv"
    results_df.to_csv(output_path, index=False)
    
    print(f"\nBatch processing complete! Saved results to {output_path}")

if __name__ == "__main__":
    main()
