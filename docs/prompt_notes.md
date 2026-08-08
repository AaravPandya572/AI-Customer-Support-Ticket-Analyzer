# Prompt Engineering & Zero-Shot Testing Notes

## Overview
Tested the initial structured JSON prompt using the `gemini-3.6-flash` model on multiple sample tickets from the dataset. 

## JSON Parsing Reliability
- **Did the AI break the JSON format?** No. The AI successfully returned valid, parseable JSON on all attempts. The Python `json.loads()` function did not throw any `JSONDecodeError`s.
- **Did it follow the constraints?** Yes, it strictly adhered to the provided category list (`[Billing, Technical Issue, Delivery Problem, Account Access, General Query]`) and priority list (`[High, Medium, Low]`).
- **Tone:** The suggested responses were consistently professional, empathetic, and stayed within the 2-3 sentence constraint.

## Ticket Results Summary
1. **Internet Speed Complaint (Presthaven Sands):** 
   - **Result:** Technical Issue / Medium
2. **Mobile Data Complaint (Glasgow City Centre):** 
   - **Result:** Technical Issue / Medium
3. **General Alert for Strange App/Phone Issue:** 
   - **Result:** Technical Issue / Medium
4. **Train Delay Inquiry (Wylde green):** 
   - **Result:** General Query / Medium
5. **Suspicious Phishing Email (Apple):** 
   - **Result:** Billing / High

## Key Findings & Prompt Refinement (The Ambiguity Issue)
- **The Problem:** When presented with a vague, contextless ticket (*"I understand but nobody is replying back. Please I need to go to work."*), the AI initially hallucinated and guessed the category as "Delivery Problem". 
- **The Fix:** Added an explicit fallback rule to the prompt: *"If the ticket is vague, ambiguous, or does not contain enough context to confidently identify a specific category, set "category" to "General Query" and "priority" to "Medium'."*
- **Outcome:** The fix worked perfectly. Upon re-testing, the AI correctly categorized the ambiguous ticket as a "General Query" with "Medium" priority, and adjusted its suggested response to urgently ask the customer for more details without making assumptions.
