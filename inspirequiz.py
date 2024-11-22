import mysql.connector                                                                                                              
import randoim

# Function to fetch a random quote at app start
def get_random_start_quote():
cursor = db.cursor()
cursor.execute("SELECT speaker, quote FROM quotes ORDER BY RAND() LIMIT 1")
result = cursor.fetchone()
cursor.close()
if result:
print(f"\n\"{result[1]}\" – {result[0]}")

# Function to fetch motivational speakers
def get_motivational_speakers():
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT speaker FROM quotes")
    speakers = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return speakers

# Function to fetch a random quote from a specific speaker
def get_quote_by_speaker(speaker):
    cursor = db.cursor()
    cursor.execute("SELECT quote FROM quotes WHERE speaker = %s ORDER BY RAND() LIMIT 1", (speaker,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None
# Function to fetch topics from the database
def get_topics():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM topics")
    topics = cursor.fetchall()
    cursor.close()
    return topics

