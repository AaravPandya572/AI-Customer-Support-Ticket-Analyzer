# AI Output Quality Review (Day 9)

## 1. Accuracy Metrics (Sample Size: 20 Tickets)
*   **Summary Accuracy:** 20/20 (100%)
*   **Category Accuracy:** 17/20 (85%)
*   **Priority Accuracy:** 20/20 (100%)
*   **Response Quality:** 20/20 (100%)

## 2. Common Mistake Pattern
The AI model performed exceptionally well on summaries and determining priority based on customer tone. However, the AI struggled slightly when edge-case situations did not perfectly fit the 5 allowed categories. For instance, it categorized a passenger train delay as a "Delivery Problem", and it struggled to consistently label phishing/account security concerns as "Account Access," opting for "Technical Issue" or "General Query" instead.

## 3. Notable Edge Cases (Optional)
*   **Ticket ID 2217961:** The customer was complaining about a train sitting outside a station. The AI categorized this as a "Delivery Problem". While technically a logistics issue, the AI failed to recognize that passenger transit is not a package delivery, highlighting a limitation in how rigid categories are applied to diverse business sectors.
*   **Ticket ID 2736921:** The customer was screaming about a company trying to take control of their Twitter account. The AI categorized this as a "Technical Issue," but it clearly should have been routed to "Account Access" due to the privacy and security implications.

## 4. Day 10 Refinement & Before/After Comparison
To address the edge cases identified in Day 9, explicit rules and a new few-shot example (phishing) were added to the system prompt.

**Results After Re-Running the Batch:**
*   **Ticket 2217961 (Train Delay):** Successfully shifted from "Delivery Problem" to "General Query".
*   **Ticket 235842 (Phishing Email):** Successfully shifted from "General Query" to "Account Access".
*   **Ticket 2736921 (Twitter Account Control):** FAILED to shift. The AI stubbornly kept this as a "Technical Issue". 

**Known Limitation Identified:**
While the prompt adjustments successfully fixed the transit and phishing misclassifications, the model still struggles with nuanced permission/security complaints. For Ticket 2736921, the AI heavily weighted the words "phone company" and categorized the complaint about app permissions/account control as a "Technical Issue" rather than "Account Access." This indicates that while few-shot prompting handles direct matches (like phishing receipts) perfectly, the model still struggles to generalize abstract security complaints into the Account Access bucket.
