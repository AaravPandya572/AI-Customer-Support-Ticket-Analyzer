# AI Customer Support Ticket Analyzer

A full-stack, AI-powered pipeline designed to automate the triage of customer support tickets. This application processes raw text requests, utilizes Google's Gemini AI to categorize and prioritize them, stores the structured data in a relational database, and visualizes the results via an interactive Streamlit web dashboard.

## Project Structure
* **`/src`**: Contains the core Python application logic (AI pipeline, database insertion, and Streamlit app).
* **`/docs`**: Contains detailed system architecture and setup instructions.
* **`/db`**: Contains the SQLite database storing the processed ticket data.
* **`/reports`**: Contains the comprehensive Technical Report.

## Documentation
* [User Guide](docs/user_guide.md) - Step-by-step instructions to run the project.
* [System Architecture](docs/architecture.md) - Detailed breakdown of the pipeline and database schema.
