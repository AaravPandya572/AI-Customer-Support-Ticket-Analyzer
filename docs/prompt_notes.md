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

# Day 6: Few-Shot Prompting Results

## Overview
Tested the upgraded `few_shot_prompt.py` script. The prompt now includes three hardcoded examples (a standard issue, a delivery issue, and a vague issue) to provide the Gemini 3.6 Flash model with strict pattern matching.

## JSON Parsing Reliability
- **Parsing Success:** 100%. The AI perfectly matched the formatting of the provided examples, returning clean JSON with no markdown blocks or extra conversational text.
- **Constraint Adherence:** The AI strictly followed the provided categories and priority levels.

## Ticket Results Summary & Improvements
1. **General Alert for Strange Issue ("seems like a problem"):** 
   - **Result:** General Query / Medium
   - **Note:** Massive improvement over Zero-Shot. The model correctly identified the lack of specific context and used the "escape hatch" example.
2. **Urgent Vague Complaint ("nobody is replying back. Please I need to go to work"):** 
   - **Result:** General Query / Medium
   - **Note:** Handled perfectly. The AI correctly identified it as a vague query and provided a highly empathetic, urgency-aware response without hallucinating a fake category.
3. **Suspicious Phishing Email (Apple):** 
   - **Result:** Billing / High
   - **Note:** Consistent with Zero-Shot, prioritizing security and potential fraud appropriately.
4. **Mobile Data Complaint (Glasgow City Centre):** 
   - **Result:** Technical Issue / High
   - **Note:** Upgraded to High priority (was Medium in Zero-Shot), which is a much better business decision for a complete loss of service ("Can't even find a server").

## Conclusion
Adding few-shot examples drastically improved the model's consistency and reasoning. It eliminated hallucinations on vague tickets and produced much more accurate priority assignments.
