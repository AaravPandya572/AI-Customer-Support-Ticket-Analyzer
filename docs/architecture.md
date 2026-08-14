Column	            Type	        Description
id	INTEGER         (Primary Key)	Unique row ID, auto-generated
ticket_id	        TEXT	        Original ticket ID from the dataset
original_text	    TEXT	        The raw customer message
summary	            TEXT	        AI-generated summary
category	        TEXT	        AI-assigned category
priority	        TEXT	        AI-assigned priority
suggested_response	TEXT	        AI-suggested reply
created_at	        TEXT	        Timestamp of when the record was added