import sqlite3
import openai
import time
from datetime import datetime

# Initialize the OpenAI client
client = openai.OpenAI(api_key='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')

# Complete keyword cloud
KEYWORDS = [
    'artistic expression',
    'business strategy',
    'communication',
    'creative thinking',
    'critical analysis',
    'entrepreneurship',
    'event planning',
    'leadership',
    'negotiation',
    'philosophy',
    'presentation',
    'problem-solving',
    'programming',
    'project management',
    'public speaking',
    'research',
    'social engagement',
    'strategy',
    'teamwork',
    'workshops',
    'arts',
    'accounting',
    'business',
    'consulting',
    'cultural awareness',
    'data science',
    'diplomacy',
    'economics',
    'environment',
    'finance',
    'global issues',
    'history',
    'innovation',
    'international relations',
    'language',
    'law',
    'literature',
    'local culture',
    'networking',
    'marketing',
    'philosophy',
    'policy',
    'politics',
    'science',
    'social justice',
    'sustainability',
    'technology',
    'trading',
    'german',
    'english',
    'french',
    'spanish',
    'turkish',
    'italian',
    'av',
    'international networks',
    'cantons',
    'sports',
    'culture & interests',
    'social & political engagement',
    'business & Investment',
    'industry focus',
    'networking & think tanks',
    'student union'
]

def get_keywords_for_description(description):
    """Get keywords for a single event description using GPT."""
    prompt = f"""Select 15 keywords from this list that best match the event description:
Keywords list: {KEYWORDS}
Event description: {description}

Return only the 15 keywords, separated by commas."""
    
    try:
        # Call GPT API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,  # Increased for more keywords
            temperature=0
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error getting keywords: {e}")
        return None

def process_future_events():
    """Process events that occur after October 1st, 2024."""
    # Connect to SQLite database
    conn = sqlite3.connect('events_database.db')
    cursor = conn.cursor()
    
    try:
        # First, let's create the new column if it doesn't exist
        try:
            cursor.execute('ALTER TABLE events_file ADD COLUMN "expanded keywords" TEXT')
            print("Created new column 'expanded keywords'")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("Column 'expanded keywords' already exists")
            else:
                print(f"Error creating column: {e}")

        # Get events after October 1st, 2024, limited to 3 events
        cutoff_date = '2024-10-01T23:00:00.000Z'
        cursor.execute('''
            SELECT _id, EventDescription, startDate 
            FROM events_file 
            WHERE startDate > ?
        ''', (cutoff_date,))
        
        events = cursor.fetchall()
        
        if events:
            for event in events:
                event_id, description, start_date = event
                print(f"\nProcessing event ID: {event_id}")
                print(f"Start Date: {start_date}")
                print(f"Description: {description}\n")
                
                if description:  # Only process if description exists
                    # Get keywords from GPT
                    keywords = get_keywords_for_description(description)
                    
                    if keywords:
                        print(f"Selected keywords: {keywords}")
                        
                        # Update the database with the new keywords
                        cursor.execute(
                            'UPDATE events_file SET "expanded keywords" = ? WHERE _id = ?',
                            (keywords, event_id)
                        )
                        
                        # Commit the update
                        conn.commit()
                        print("Database updated successfully!")
        else:
            print("No future events found in the database.")
    
    except Exception as e:
        print(f"Error processing events: {e}")
        
    finally:
        # Always close the database connection
        conn.close()

if __name__ == "__main__":
    process_future_events()
