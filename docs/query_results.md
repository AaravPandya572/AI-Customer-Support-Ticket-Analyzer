# SQL Query Results & Business Explanations

### 1. High Priority Tickets
* **SQL Concept:** `SELECT ... WHERE`
* **Business Question:** "Which tickets are critically urgent and need to be assigned to agents immediately to prevent customer churn?"

### 2. Ticket Count by Category
* **SQL Concept:** `GROUP BY` and `COUNT()`
* **Business Question:** "Where are our product bottlenecks this week? (e.g., Are we getting an unusual spike in Technical Issues?)"

### 3. Ticket Count by Priority
* **SQL Concept:** `GROUP BY` and `COUNT()`
* **Business Question:** "What is the overall stress level of our support queue right now? Do we need to ask staff to work overtime?"

### 4. 10 Most Recent Tickets
* **SQL Concept:** `ORDER BY` and `LIMIT`
* **Business Question:** "What is the absolute latest information coming into our queue right at this exact minute?"

### 5. Keyword Search (e.g., 'account')
* **SQL Concept:** `LIKE '%keyword%'`
* **Business Question:** "A new software bug was just reported regarding account logins—can we instantly pull all recent complaints mentioning 'account'?"
