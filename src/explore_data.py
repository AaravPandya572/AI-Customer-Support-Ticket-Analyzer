import pandas as pd

def main():
    # Load the CSV file into a Pandas DataFrame
    file_path = "data/raw/twcs.csv" 
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)

    # Print the total number of rows and columns
    print("\n--- Dataset Shape ---")
    print(f"Rows, Columns: {df.shape}")

    # Print a preview of the first 5 rows
    print("\n--- First 5 Rows ---")
    print(df.head())

    # Check for empty or missing data in each column
    print("\n--- Missing Values Per Column ---")
    print(df.isnull().sum())

    # Count how many rows are customer messages (True) vs company replies (False)
    print("\n--- Inbound vs Outbound Counts ---")
    print(df['inbound'].value_counts())

if __name__ == "__main__":
    main()
