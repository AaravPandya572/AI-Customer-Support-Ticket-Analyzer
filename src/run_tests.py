import os
from dotenv import load_dotenv
from google import genai
from ai_pipeline import analyze_ticket


load_dotenv()
client = genai.Client()

# Defining the exact edge cases the manual requires
test_cases = {
    "Valid Ticket": "I was double charged for my subscription this month. Please refund me.",
    "Empty Input": "",
    "Very Short Ticket": "help",
    "Very Long Ticket": "My internet is down. Also your app keeps crashing when I try to pay my bill. And yesterday the delivery guy threw my package in the bushes. I am so angry I want a refund for everything and I'm canceling my account.",
    "Special Characters": "🤬 @AmazonHelp WHERE IS MY 📦?!? #angry",
    "Mixed Language": "Mi internet no funciona. Please send a technician."
}

# Running the tests
for case_name, text in test_cases.items():
    print(f"\n--- Testing: {case_name} ---")
    print(f"Input: '{text}'")
    
    
    result = analyze_ticket(client, text)
    
    # If function hits an error on both attempts, it returns the {"error": ...} dictionary
    if "error" in result:
        print(f"Result: HANDLED ERROR -> {result['error']}")
    else:
        print(f"Result: SUCCESS -> {result}")
