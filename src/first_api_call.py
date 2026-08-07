import os
from dotenv import load_dotenv
from google import genai

def main():
    # 1. Safely load the environment variables from your .env file
    load_dotenv()
    
    # 2. Initialize the Gemini client. 
    # Because we ran load_dotenv() above, genai.Client() will automatically 
    # find GEMINI_API_KEY in the background without us typing it here.
    client = genai.Client()
    
    # 3. Define the test prompt
    prompt = "Summarize this customer message in one sentence: 'My internet has been down for three days and no one has replied to my emails.'"
    
    print("Sending prompt to Gemini API... (waiting for response)")
    
    # 4. Call the Gemini API with the updated model
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    
    # 5. Print the text response
    print("\n--- AI Response ---")
    print(response.text)

if __name__ == "__main__":
    main()
