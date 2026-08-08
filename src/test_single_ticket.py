import os
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Explicit function to generate our strict prompt
def get_structured_prompt(ticket_text):
    return f"""You are a customer support analyst. Read the customer ticket below and respond ONLY with a valid JSON object with these exact fields:
- "summary": a one-sentence summary of the customer's issue
- "category": one of [Billing, Technical Issue, Delivery Problem, Account Access, General Query]
- "priority": one of [High, Medium, Low]
- "suggested_response": a professional, empathetic response to the customer, 2-3 sentences

Rules:
1. If the ticket is vague, ambiguous, or does not contain enough context to confidently identify a specific category, set "category" to "General Query" and "priority" to "Medium".
2. Respond with ONLY the JSON object. Do not include any explanation, markdown formatting, or extra text.

Ticket: '{ticket_text}'"""


def main():
    load_dotenv()
    client = genai.Client()

    # 1. Load your clean sample data
    print("Loading sample tickets...")
    df = pd.read_csv("data/processed/tickets_sample.csv")
    
    # Grab the very first ticket (index 0)
    ticket_index = 6 
    ticket_text = df['text'].iloc[ticket_index]
    print(f"\n--- Original Ticket ---\n{ticket_text}")

    # 2. Build the prompt
    prompt = get_structured_prompt(ticket_text)
    print("\nSending structured prompt to Gemini API...")
    
    # 3. Call the API
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    
    raw_output = response.text
    
    # We strip those out just in case, to protect our parser.
    clean_output = raw_output.replace("```json", "").replace("```", "").strip()

    # 4. Parse the JSON text into a Python dictionary
    try:
        parsed_data = json.loads(clean_output)
        print("\n--- Parsed JSON Output ---")
        print(f"Summary:  {parsed_data['summary']}")
        print(f"Category: {parsed_data['category']}")
        print(f"Priority: {parsed_data['priority']}")
        print(f"Response: {parsed_data['suggested_response']}")
    except json.JSONDecodeError:
        print("\n[ERROR] The AI did not return valid JSON. Here is the raw output that broke the parser:")
        print(raw_output)

if __name__ == "__main__":
    main()
