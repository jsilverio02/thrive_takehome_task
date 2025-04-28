-- Create the consolidated_messages Fact Table

CREATE TABLE consolidated_messages (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        email TEXT,
	conversation_id INTEGER,
        message TEXT,
	message_type TEXT,
        created_at INTEGER
    );