import pandas as pd
import re

# Explicit function to strip @company names from the start of a tweet
def remove_leading_mentions(text):
    if not isinstance(text, str):
        return text
    # This regex removes things like "@AmazonHelp " from the start of the message
    return re.sub(r'^(@\w+\s*)+', '', text).strip()

# Explicit function to check string length
def is_long_enough(text):
    return len(str(text)) >= 10

def main():
    print("Loading raw dataset... (this may take a moment)")
    df = pd.read_csv("data/raw/twcs.csv")

    # Step A: Filter for customer tickets only
    df = df[df['inbound'] == True]

    # Step B: Drop empty and duplicate text rows
    df = df.dropna(subset=['text'])
    df = df.drop_duplicates(subset=['text'])

    # Step C: Clean the text (remove leading @mentions)
    df['text'] = df['text'].apply(remove_leading_mentions)

    # Step D: Remove extremely short messages
    df = df[df['text'].apply(is_long_enough)]

    # Step E: Reset the index
    df = df.reset_index(drop=True)

    print(f"Cleaning complete! Total clean rows: {df.shape[0]}")

    # Step F: Save the full cleaned dataset
    df.to_csv("data/processed/tickets_cleaned.csv", index=False)
    print("Saved fully cleaned dataset to data/processed/tickets_cleaned.csv")

    # Step G: Create and save a small working sample
    sample_df = df.sample(n=250, random_state=42)
    sample_df.to_csv("data/processed/tickets_sample.csv", index=False)
    print("Saved 250-row sample to data/processed/tickets_sample.csv")

if __name__ == "__main__":
    main()
