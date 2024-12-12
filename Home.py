# Welcome to the backend of MatchMyEvent!

# Before you go on to examine this project, we would like to briefly explain the layout of this project.

# As should evident, this project makes use of a multipage layout to structure both the code and user interface,
# while also facilitating a way to split coding work between group members.

# This here is the entry-page into the multipage layout of the code; we recommend that you proceed to the session_state_handler-file next,
# and then move on to the rest of the actual pages as this will help to better understand this multipage-layout

# Regarding the structure of the code: all pages are structured after the following principle: Imports - Constants - Classes - Functions - Execution

# Besides being the entry page of the program, this page also serves the purpose of accessing the data from an sql-database
# The reason for this is that this page is inevitable the first page to load;
# feeding data into the system here makes sense as there is no need to perform any other action to ensure the readiness of the data
# On the front-end, this is only functions as an welcome- and information page without any further user interaction





from datetime import datetime
import pandas as pd
import sqlite3
import streamlit as st
import session_state_handler as sh

# CONTSTANTS
# DATABASE CONNECTION using sqlite3-library
# specification of file path using raw string; WHEN USING LOCAL COPIES, ENTER FILE PATH HERE
db_path = r"events_database.db"
connection = sqlite3.connect(db_path)

# using cursors to access data in the database
cur1 = connection.cursor()
events_data = cur1.execute('SELECT _id, EventName, EventType, ClubName, EventDescription, startDate, endDate, Location_1, Language, expanded_keywords FROM events_file')
cur2 = connection.cursor()
clubs_data = cur2.execute('SELECT clubName, InterestKeywords FROM club_profile_list')
cur3 = connection.cursor()
keywords_cloud_cursor = cur3.execute('SELECT keywords FROM keyword_cloud')

#this function defined in the session_state_handler-file initates the sessions states as soon as the file is opened
#this avoids session state key errors that might otherwise occur when other parts of the code are accessed before initializing session states
sh.initiate_session_state()

# CLASSES
# The Event-profile class defines events as well as their relevant attributes for further use in other pages, specifically Browse Events and Event Recommendations
class Event_profile:
    def __init__(self, _id, title, event_type, clubName, description, startDate, endDate, location_text, language, event_keywords):
        self._id = _id
        self.title = title
        self.event_type = event_type
        self.clubName = clubName
        self.description = description
        self.startDate = startDate#datetime.strptime(startDate, '%Y-%m-%d')  # Conversion en datetime
        self.endDate = endDate#datetime.strptime(endDate, '%Y-%m-%d')  # Conversion en datetime
        self.location_text = location_text
        self.language = language
        self.event_keywords = event_keywords
        self.event_keywords = []

    def __repr__(self): # coded with ChatGPT to save time; prompt: give me a __repr__-function for the following Class: (Event_profile)
        return (
            f"Event_profile(EventID={self._id!r}, title={self.title!r}, "
            f"event_type={self.event_type!r}, clubName={self.clubName!r}, "
            f"etartDate={self.startDate!r}, endDate={self.endDate!r}, location_text={self.location_text!r}, language={self.language}, "
            f"event_keywords={self.event_keywords})"
        )



# Classe pour les clubs
class Club:
    def __init__(self, clubName, InterestKeywords):
        self.clubName = clubName
        self.InterestKeywords = InterestKeywords
        InterestKeywords = []


    def __repr__(self): # coded with ChatGPT to save time; prompt: give me a __repr__-function for the following Class: (Club)
            return (
                f"Club(ClubName={self.clubName!r}, club_keywords={self.InterestKeywords})"
            )

#FUNCTIONS

#CLEARING SESSION STATES
#deletes all session state values through iteration to reset the session
def reset_session():
        if st.button("Reset all"):
            for key in st.session_state.keys(): #change from keys to values
                del st.session_state[key]
        sh.initiate_session_state()



# EXECUTION - backend

#iterating through cursor list of clubs to create a list of club instances containing the clubs' names and associated keywords
clubs_instances = []
for club in clubs_data:
    interest_keywords_temp = str(club[1])
    club_instance = Club(clubName=club[0], InterestKeywords=interest_keywords_temp.split(', '))
    clubs_instances.append(club_instance)


#iterating through cursor-list to create a list of event profile instances by using the indices of the values in the cursor list
events_instances = []
fixed_date = datetime(2024, 10, 1, 0, 0, 0) #for demonstration purpses; fixed date to be removed if actual future events are to be displayed
for line in events_data:
    event_start_date = datetime.strptime(line[5], "%Y-%m-%dT%H:%M:%S.%fZ") # done with ChatGPT; prompt: give me a code snippet to convert the following date format to work with the datetime library: 2024-01-30T19:00:00.000Z
    if event_start_date > fixed_date: #can be replaced with datetime.now(): to view actual future events
        event_instance = Event_profile(
            _id = line[0],
            title = line[1],
            event_type= line[2],
            clubName = line[3],
            description = line[4],
            startDate = line[5],
            endDate = line[6],
            location_text = line[7],
            language = line[8],
            event_keywords = []
        )
        event_instance.event_keywords.append(str(line[9]).split(', '))
        for keyword in event_instance.event_keywords[0]:
            event_instance.event_keywords.append(keyword)
        event_instance.event_keywords.remove(event_instance.event_keywords[0])
        events_instances.append(event_instance)

for event in events_instances:
    for club in clubs_instances:
        if event.clubName == club.clubName:
            event.event_keywords.extend(club.InterestKeywords)
            #event.event_keywords += club.InterestKeywords

keywords_cloud = []
keywords_cloud = [row[0] for row in keywords_cloud_cursor]

#include set-function to reduce event keywords?

#assigning local list-variables to session states to facilitate global access and store data for the duration of the session
st.session_state['club_instances_list'] = clubs_instances
st.session_state['events_instances_list'] = events_instances
st.session_state['global_keyword_cloud'] = keywords_cloud


# EXECUTION - frontend
    
# Ajouter le style CSS pour centrer le contenu
st.markdown(
    """
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Contenu de la page avec la classe CSS centrée
st.markdown("<h1 class=""centered"">Welcome to MatchMyEvent :) </h1>", unsafe_allow_html=True)
st.markdown('<p class="centered">The webpage to guide you through HSG campus events</p>', unsafe_allow_html=True)
st.markdown('<h4 class="centered">Do you feel overwhelmed by the too big amount of clubs and events proposed at HSG?</h4>', unsafe_allow_html=True)

# URL brute de l'image
image_url = "MatchMyEvent Logo.png"

# Afficher l'image
st.image(image_url, use_column_width=True)
    
st.markdown('<h4 class="centered">Don\'t worry, this page\'s for you</h4>', unsafe_allow_html=True)
st.markdown('<p class="centered">We\'ve created an algorithm that will perfectly match your preferences</p>', unsafe_allow_html=True)



if st.button("see developers' commentary"):
    st.text("""This commentary is meant to complement the video to further\n
explain the code and the processes that gone into realizing this project.\n\n 
“BUSINESS CASE” AND PURPOSE\n\n 
As many students will attest, the number of events taking place on the HSG can \n
be overwhelming to a point where it is difficult to be aware of all the \n
interesting events taking place on and around campus. MatchMyEvent solves \n
this problem by providing personalized event recommendations and allowing \n
students to browse events by clubs.\n\n
BASIC FUNCTIONALITY\n 
To create personalized event recommendations, MatchMyEvent accesses data \n
provided by the SHSG and compares it to a user profile that the user creates \n
through the interface by selecting their interests.\n 
More concretely, this project’s code matches lists of keywords against one \n
another to determine a keyword matching score (kms). The first list is the \n
user_keywords-list, which is based on the user’s inputs gathered in the User \n
Profile creation. The other list is associated with each individual event and \n
contains the event’s keywords. The “overlap” of keywords in the two lists \n
constitutes the kms, which is further increased with a certain “bonus” if the \n
events language matches the user’s language preferences and the event type \n
matches the event type preferences.\n 
The events are then ranked by the kms and the top five are presented to the \n
user. The user can then dislike the event to delete it from the list and get a \n
new recommendation (with a lower kms). Further, the user can also add the \n
event to his personal outlook calendar with the respective button.\n 
In addition to that, the user can browse events by the club that is organizing \n
it. To do so, the user can select any number of clubs, and all the selected \n
clubs’ events are presented to the user.\n\n 
ELEMENTS OF THE CODE\n 
This is a brief summary of all the elements present in the project on a \n
file-level. This section will briefly explain which elements are present, what \n
their role and basic function is and how they interact with the other \n
elements.\n\n 
Here is a visual representation of the elements and their interaction:\n\n""")
#Insert Graphic of interlinked pages
    image_url_2 = 'code_files_architecture_image.JPG'
    st.image(image_url_2, use_column_width=True)
    st.text("""Source: own illustration\n\n 
Database\n 
The starting point of the project is the database. The events_database.db file \n
was created from a csv-file provided by the SHSG, using the DB Browser for \n
SQLite application. This SQL-database contains all of the relevant data, i.e. \n
a table with all of the events registered with the SHSG, a table with all of \n
the student clubs with their corresponding keywords as well as a global \n
keyword cloud, containing all of the keywords that are allowed in the system.\n 
As can be seen above, the database first interacts with the keyword expander \n
file, before it then passes the data to the entry page of the actual project \n
code, i.e. the Home.py file.\n\n 
Keyword Expander\n 
The keywords expander is a separate code file that is not directly integrated \n
into the MatchMyEvent project code but is nonetheless crucial for the \n
functioning of the application. It serves the purpose of expanding the \n
keywords for each event in the events table based on the respective event \n
description and the global keyword cloud, using access to the OpenAI-API. This \n
is explained in more detail later on.\n\n 
Home (entry page)\n 
Home.py is the entry page for the project. When opening the project, this is \n
the file that needs to be opened with the streamlit run Home.py command.\n 
On the frontend, this just serves as an introduction to MatchMyEvent and \n
further contains this documentation.\n 
On the backend, this file calls the data from the database to create a list of \n
Event-instances using the sqlite3 library and a cursor-function. This \n
event_instances_list is saved in a session state and subsequently used to \n
allow the User to browse events and receive personalized event suggestions.\n\n 
Session State Handler\n 
The session_state_handler.py-file is invisible on the front end and serves as \n
infrastructure to manage the permanent storage of variables through the use of \n
the st.session_state widget. While the actual values in the st.session_state \n
dictionary are saved in a cache created by streamlit, the session state \n
handler contains all the relevant functions that help to initialize and later \n
manage the session states. Consequently, all subordinated pages call on the \n
session state handler, at least indirectly, to access the data the session \n
state handler has helped to initialize and manage.\n\n 
User Profile\n 
1_User_Profile.py allows the user to enter his profile as well as certain \n
variables through a number of streamlit widgets. These inputs are stored in \n
the respective sessions states, and, in some cases, lead to further indirect \n
changes to the user_keyword-list variable and its respective session state.\n
to finally create a number of variables that make up the user profile. \n
This user profile is stored in the session states for the duration of the \n
session and can be accessed by the event recommendations file.\n\n 
Event Recommendations\n 
The 2_Event_Recommendations.py-file draws on the sessions state containing \n
the events_instances_list to compare the events instances to the user profile \n
to create a new list of events, ranked by their kms. This list is then \n
presented to the user in the form of the top recommendations.\n\n 
Browse Events\n 
The 3_Browse_Events.py-file draws on both session states as well as the \n
events_instances_list created in the Home.py file to allow the user to view \n
all of the events taking place, filtered by the club that is organizing it.\n\n
Calendar Handler\n
The calendar_handler.py file is another invisible file that cotains the function\n
that allows the sending of outlook invitations through the exchangelib library.\n
The details of this function are elaborated on later. The reason this file is separate\n
is that github does not support the exchangelib library; keeping the code with this\n
library prevents errors associated with the library. Both the Event Recommendation and\n
Browse Events pages call the function contained in this file; some of the code in\n
those files is commented-out to avoid errors.\n\n
DATA\n 
The starting point of this project is the data made available to us by the \n
SHSG through a csv-file. The bigger challenge with the data was the limited \n
amount of information, specifically with regards to attributes suitable for \n
matching individual events with the user preferences.\n 
In addition to the events, there is also data on the clubs that are registered \n
with the SHSG, including a number of keywords.\n 
While the database provided by the SHSG contains plenty of metadata around the \n
events, individual events do not have many attributes that would help to \n
classify or characterize events based on keywords. To solve this issue, we had \n
to improvise and generate keywords based on the available event information.\n 
From a technical implementation perspective, we encountered some issues with \n
these files: when importing csv contents into our code with both pandas’ \n
pd.readcsv as well as a csv library, we had trouble with corrupted files and \n
unreliability with the libraries’ csv-reading functions. Consequently, we \n
decided to transform this data into an SQL-database using DB Browser for \n
SQLite. This allows for a more reliable data access.\n\n 
KEYWORD EXPANSION\n
To solve the issue with the insufficient keywords in the events file, we came \n
up with a solution that uses OpenAI’s API. The API is sent the event \n
description as well as a “global keyword cloud” that contains all keywords \n
that are permitted. Given the event description and the keywords cloud, it is \n
asked to return a list of 15 keywords out of the keyword cloud that best match \n
the event description.\n 
It should be noted that this is not part of the main code, but more of a \n
separate step that is done before the main code is executed. Hence, there is a \n
separate python file that contains code that accesses the SHSG database, \n
retrieves the relevant data (i.e. event descriptions and the global keyword \n
cloud), calls the API to receive the new keywords list and feeds that list \n
back into the database.\n 
This separate setup has two specific reasons: Firstly, the OpenAI API is not \n
free. While the costs per expansion operations are not very expensive (i.e. a \n
few cents for about 70 event instances), repeatedly calling the API during the \n
use of the main project code would be too costly and exhaust the funds quite \n
quickly.\n 
Secondly, the expansion of the keywords takes a lot of time. The expansion of \n
70 keywords takes about five minutes. Again, executing the expansion during \n
the use of the MatchMyEvent-application would be very impractical.\n 
It is also important to note that not all of the events had their keywords \n
expanded. While the database contains all events registered by the clubs with \n
the SHSG since the end of January 2024, only events after the first of October \n
were expanded in line with an artificial starting date explained below. \n
Expanding all of the events would have been more costly and would not have \n
served a purpose.\n\n 
ARTIFICIAL STARTING DATE FOR DEMONSTRATION PURPOSES\n 
As events and the corresponding csv-files are only updated in certain \n
intervals by the SHSG, our current database (as of 12.12.2024) only contains \n
events until mid-December. To have a larger number of events ready for the \n
demonstration, we have set up the system to include all events after \n
01.10.2024 as otherwise, only a handful of events would have been left for the \n
end of this semester. Having a larger number of events, as would be the case \n
throughout the semester, helps to give a better demonstration of the user \n
experience. It is very easy to configure the code to take the current date as \n
a starting point; the code for this is already prepared in the Home.py file \n
and can be copy-pasted into the respective line.\n\n 
OUTLOOK API / EXCHANGLIB LIBRARY\n 
The calendar integration infrastructure is fully implemented using \n
Microsoft's Exchange Web Services (EWS), but several external factors can \n
prevent successful calendar invitations. Institutional network restrictions, \n
such as those commonly found in university WiFi networks, may block the \n
necessary EWS connections required for Outlook communication. Additionally, \n
Microsoft's security policies for personal Outlook accounts often require \n
specific authentication methods, particularly when two-factor authentication \n
is enabled, necessitating the use of special app passwords instead of regular \n
account passwords. The modern shift towards OAuth2 authentication and \n
Microsoft's gradual deprecation of basic authentication methods can also \n
impact the functionality of traditional EWS connections. Furthermore, \n
different types of Outlook accounts (personal, organizational, or educational) \n
may have varying levels of API access permissions, affecting the ability to \n
programmatically create and send calendar invitations. In the implementation \n
process, code documentation using '#' comments was essential to ensure \n
compatibility with GitHub's version control system, as different operating \n
systems and environments might interpret special characters in code comments \n
differently, potentially causing execution errors during repository \n
synchronization.\n\n 
LIMITATIONS\n 
While the code works quite well, there are a few limitations.\n 
As mentioned earlier, the amount of data available from the SHSG is quite \n
limited and varies heavily with regard to the description, making certain the \n
accuracy of the recommendations not quite as accurate as it could be.\n 
Additionally, the mechanism of comparing keyword lists used in our code makes \n
the implementation of machine learning difficult. While this probably would \n
have been possible in principle, we were not able to incorporate it into the \n
code as seamlessly as previously thought and would have required large-scale \n
changes to the architecture of the code. Given these fundamental changes \n
required to facilitate this implementation combined with the time constraint, \n
integrating a machine learning feature would not have been feasible before the \n
deadline.\n 
There are also some minor details, such as the presence of line breaks \n
(backslash-n) in the event descriptions that unfortunately could not be worked \n
out. However, these are more cosmetic and do not affect the functionality of \n
the code.\n 
Finally, not all clubs announce all of their events through the SHSG \n
infrastructure, leading to some blind spots for the MatchMyEvent user. \n
Nonetheless, the app allows students to get recommendations for a large number \n
of events, as the event database beginning in January and ending in May \n
contains more than 200 events.""")
