import sqlite3

# Path to the SQLite database file
db_path = r'C:\Users\jeffs\OneDrive\Desktop\DataEng Takehome\thrive_test_db.db'

# Connect to the database
conn = sqlite3.connect(db_path)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

#Step 1: Drop consolidated_messages if it already exists
cursor.execute('DROP TABLE IF EXISTS consolidated_messages;')

# Step 2: Create the consolidated_messages table
cursor.execute('''
    CREATE TABLE consolidated_messages (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        email TEXT,
	conversation_id INTEGER,
        message TEXT,
	message_type INTEGER,
        created_at INTEGER
    );
''')

# Step 3: Insert consolidated data from both conversation_start and conversation_parts
cursor.execute('''
insert into consolidated_messages (user_id, email, conversation_id, message, message_type, created_at)

with CTE_consolidated as (
	select
	u.id as user_id,
	cs.conv_dataset_email as email,
	cs.id as conversation_id,
	cs.message,
	1 as message_type,
	cs.created_at
	from conversation_start cs
	left join users u on cs.conv_dataset_email=u.email
	where u.is_customer=1
	union all
	select
	u.id as user_id,
	cp.conv_dataset_email as email,
	cp.id as conversation_id,
	cp.message,
	case
            when cp.part_type = 'open' then 1
            when cp.part_type = 'assignment' then 2
            when cp.part_type = 'close' then 3
            when cp.part_type = 'comment' then 4
            when cp.part_type = 'conversation_rating_change' then 5
            when cp.part_type = 'message_assignment' then 6
            when cp.part_type = 'note' then 7
            else 0
	end as message_type,
	cp.created_at
	from conversation_parts cp
	left join users u on cp.conv_dataset_email=u.email
	where u.is_customer=1
) select * from CTE_consolidated order by user_id, created_at;
''')

# Commit and close
conn.commit()
conn.close()

print("Integration complete!")
