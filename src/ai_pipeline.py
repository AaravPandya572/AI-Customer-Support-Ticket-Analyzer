import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from google import genai

def get_few_shot_prompt(ticket_text):
    return f"""You are a customer support analyst. Read the customer ticket and respond ONLY with a valid JSON object. 
Fields required: "summary", "category" (Billing, Technical Issue, Delivery Problem, Account Access, General Query), "priority" (High, Medium, Low), and "suggested_response".

Rules:
1. If the ticket is vague or lacks context, set category to "General Query" and priority to "Medium".
2. "Delivery Problem" is ONLY for physical packages or food delivery, NOT for public transit or passenger train delays (use "General Query" for transit delays).
3. Respond with ONLY the JSON object.

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

--- Example 4 (Account Security / Edge Case) ---
Ticket: 'hi! Is this an official apple email? If so, I didn’t buy anything that’s on this receipt! 😱😱'
Response:
{{
    "summary": "The customer received a suspicious email receipt for an unauthorized purchase.",
    "category": "Account Access",
    "priority": "High",
    "suggested_response": "Please do not click on any links in that email, as it appears to be a phishing attempt. Official receipts do not use shortened URLs. I recommend checking your actual account history directly through your device settings."
}}

--- Actual Ticket ---
Ticket: '{ticket_text}'
Response:"""


def analyze_ticket(client, ticket_text):
    prompt = get_few_shot_prompt(ticket_text)
    
    # Simple retry mechanism: try up to 2 times
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            raw_output = response.text
            clean_output = raw_output.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_output)
        
        except Exception as e:
            if attempt == 1:
                return {"error": str(e)}
            time.sleep(2) # Short wait before retry

def main():
    load_dotenv()
    client = genai.Client()

    print("Loading full sample dataset...")
    df = pd.read_csv("data/processed/tickets_sample.csv")
    
    results_list = []
    total_processed = 0
    total_successful = 0
    total_failed = 0

    print(f"Starting batch processing for {len(df)} tickets...\n")

    for index, row in df.iterrows():
        ticket_id = row['tweet_id']
        ticket_text = row['text']
        
        print(f"Processing Ticket {ticket_id} (Row {index + 1}/{len(df)})...")
        
        parsed_data = analyze_ticket(client, ticket_text)
        
        # Check if the AI analysis failed
        if "error" in parsed_data:
            print(f"[ERROR] Failed on ticket {ticket_id}: {parsed_data['error']}")
            with open("docs/failed_responses.log", "a") as log_file:
                log_file.write(f"Ticket ID: {ticket_id} | Error: {parsed_data['error']}\n")
            total_failed += 1
        else:
            # Attach the original ticket ID and text so we can track it
            parsed_data['ticket_id'] = str(ticket_id)
            parsed_data['original_text'] = ticket_text
            results_list.append(parsed_data)
            total_successful += 1
            
        total_processed += 1
        
        # Rate limit protection (15 seconds to safely stay under 5-per-minute free tier limit)
        time.sleep(5)

    # Save the full results list as a JSON file
    output_path = "data/processed/ai_results.json"
    with open(output_path, "w") as f:
        json.dump(results_list, f, indent=4)
    
    # Print the final summary
    print("\n=======================================")
    print("   BATCH PROCESSING COMPLETE")
    print("=======================================")
    print(f"Total Tickets Processed: {total_processed}")
    print(f"Total Successful:        {total_successful}")
    print(f"Total Failed:            {total_failed}")
    print(f"Results saved to:        {output_path}")

if __name__ == "__main__":
    main()
