# System Architecture

## Overview
The AI Customer Support Ticket Analyzer follows a three-tier architecture that extracts unstructured data, processes it via a Large Language Model (LLM), and stores it as structured, queryable data.

## 1. AI Workflow & Prompt Engineering
The core processing relies on the `google-genai` SDK. The pipeline uses **Few-Shot Prompting** to guarantee structured output. By passing explicit JSON examples in the prompt, the model is constrained to return a predictable dictionary containing:
* `summary`: A concise explanation of the issue.
* `category`: A strict classification (e.g., Billing, Technical Issue).
* `priority`: A triage level (High, Medium, Low).
* `suggested_response`: A drafted reply for the support agent.

## 2. Database Design (SQLite Schema)
The system uses SQLite for lightweight, reliable storage. 

Column	            Type	        Description
id	INTEGER         (Primary Key)	Unique row ID, auto-generated
ticket_id	        TEXT	        Original ticket ID from the dataset
original_text	    TEXT	        The raw customer message
summary	            TEXT	        AI-generated summary
category	        TEXT	        AI-assigned category
priority	        TEXT	        AI-assigned priority
suggested_response	TEXT	        AI-suggested reply
created_at	        TEXT	        Timestamp of when the record was added