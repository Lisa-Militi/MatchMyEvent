# This part of the code was written with the help of Claude AI (3.5 Sonnet). This was done mainly due to the reason that, the code could not be tested infinitely due to the limited credit use of the API
# 6CHF were invested into the Credits to use the ChatGPT API
# The keyword expansion code was run once to expand the keywords of 71 events, then this expanded database was used in the rest of the code
# importing the necessary libraries
import sqlite3
import openai
import time
from datetime import datetime

# Initialize the OpenAI client
client = openai.OpenAI(api_key='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')

# Complete keyword cloud: A mixture of existing keywords and manually generated ones matching events at HSG and HSG Student Clubs
# These are all keywords that are allowed within the system of our whole code.
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

#Taking Event description as an input
def get_keywords_for_description(description):
#Defining the prompt for the keyword expansion
# Goal of the prompt: To attribute more keywords to an event so that the matching is more accurate in the end
    prompt = f"""Select 15 keywords from this list that best match the event description:
Keywords list: {KEYWORDS}
Event description: {description}

Return only the 15 keywords, separated by commas."""
    
    try:
        # Call GPT-4 API
        response = client.chat.completions.create(
            model="gpt-4", #Specifying ChatGPT model
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,  # Was added to not use up to much API credits
            temperature=0 #0 temperature to get consistent response
        )
        # Getting the text content from GPT's response
        return response.choices[0].message.content
    
#Error handler        
    except Exception as e:
        print(f"Error getting keywords: {e}")
        return None
#Processing Events after 1st of October 2024
# Since it is the end of the semester there were only a few future events
def process_future_events():
    # Connect to SQLite database (stored directly in repository)
    conn = sqlite3.connect('events_database.db')
    cursor = conn.cursor()
    
    try:
        # Create new column "expanded keywords" in the Database via python code
        # Column will store TEXT data type
        try:
            cursor.execute('ALTER TABLE events_file ADD COLUMN "expanded keywords" TEXT')
            print("Created new column 'expanded keywords'")
        #Error handler for SQLite database
        except sqlite3.OperationalError as e:
        #Error message if column already exists
            if "duplicate column name" in str(e):
                print("Column 'expanded keywords' already exists")
            # Different kind of SQLite error
            else:
                print(f"Error creating column: {e}")

        # Get events after October 1st, 2024
        # Since it is the end of the semesters only few future events were available
        cutoff_date = '2024-10-01T23:00:00.000Z'
        # Get necessary information from database. startDate is bigger than the cutoff date
        cursor.execute('''
            SELECT _id, EventDescription, startDate 
            FROM events_file 
            WHERE startDate > ?
        ''', (cutoff_date,))
        
        events = cursor.fetchall()

        #Checking for events in the database
        if events:
        # Loop through each event
            for event in events:
                #Splitting the event data into the three necessary variables and printing the information the code is processing
                event_id, description, start_date = event
                print(f"\nProcessing event ID: {event_id}")
                print(f"Start Date: {start_date}")
                print(f"Description: {description}\n")
                
                if description:  # Only process if description exists
                    # Get keywords from GPT 4
                    keywords = get_keywords_for_description(description)
                #Expand kexwords if existing keywords can be found 
                    if keywords:
                        print(f"Selected keywords: {keywords}")
                        
                        # Update the database with the generated keywords
                        cursor.execute(
                            'UPDATE events_file SET "expanded keywords" = ? WHERE _id = ?',
                            (keywords, event_id)
                        )
                        
                        # Commit the update
                        conn.commit()
                        print("Database updated successfully!")
        else:
        # If no events were found, print this message
            print("No future events found in the database.")

    #Error handling
    except Exception as e:
        print(f"Error processing events: {e}")
        
    finally:
        # Closing the database connection
        conn.close()

if __name__ == "__main__":
    process_future_events()
