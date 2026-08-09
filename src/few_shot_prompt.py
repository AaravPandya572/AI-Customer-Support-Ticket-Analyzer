import os
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai

def get_few_shot_prompt(ticket_text):
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
    
    # Let's test a new ticket index
    ticket_index = 1
    ticket_text = df['text'].iloc[ticket_index]
    print(f"\n--- Original Ticket ---\n{ticket_text}")

    prompt = get_few_shot_prompt(ticket_text)
    print("\nSending few-shot prompt to Gemini API...")
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    
    raw_output = response.text
    clean_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        parsed_data = json.loads(clean_output)
        print("\n--- Parsed JSON Output ---")
        print(f"Summary:  {parsed_data['summary']}")
        print(f"Category: {parsed_data['category']}")
        print(f"Priority: {parsed_data['priority']}")
        print(f"Response: {parsed_data['suggested_response']}")
    except json.JSONDecodeError:
        print("\n[ERROR] The AI did not return valid JSON. Here is the raw output:")
        print(raw_output)

if __name__ == "__main__":
    main()
