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
 else:
    print("No motivational quotes available.")


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
# Function to fetch a random question for a selected topic
def get_random_question(topic_id, asked_questions):
    cursor = db.cursor()


    # print(f"Fetching question for topic_id: {topic_id}")
    # print(f"Previously asked questions: {asked_questions}")


    try:
        if asked_questions:  # Check if there are already asked questions
            # Dynamically create placeholders for the NOT IN clause
            placeholders = ', '.join(['%s'] * len(asked_questions))
            query = f"""
            SELECT id, question_text, option_a, option_b, option_c, option_d, correct_option
            FROM questions
            WHERE topic_id = %s AND id NOT IN ({placeholders})
            ORDER BY RAND()
            LIMIT 1
            """
           #  print(f"Executing query with NOT IN filter: {query}")
            # Combine topic_id and asked_questions into one tuple for query parameters
            params = (topic_id, *asked_questions)
            cursor.execute(query, params)
        else:
            query = """
            SELECT id, question_text, option_a, option_b, option_c, option_d, correct_option
            FROM questions
            WHERE topic_id = %s
            ORDER BY RAND()
            LIMIT 1
            """
           #  print("Executing query without NOT IN filter...")
            cursor.execute(query, (topic_id,))


        # Fetch result
        result = cursor.fetchone()
        # print(f"Query result: {result}")


        # If a question is found, return it
        if result:
            question_id, question_text, option_a, option_b, option_c, option_d, correct_option = result
            asked_questions.append(question_id)  # Add question ID to the list
           #  print(f"Returning question ID: {question_id}")
            return {
                'question': question_text,
                'options': [option_a, option_b, option_c, option_d],
                'correct_option': correct_option
            }
        else:
            print("No questions available for this topic or all questions have been asked.")
            return None


    except Exception as e:
        print(f"Error fetching question: {e}")
        raise
    finally:
        cursor.close()

# Function to fetch the highest score of the user for a specific topic
def get_highest_score(user_id, topic_id):
    cursor = db.cursor()
    cursor.execute("SELECT MAX(score) FROM scores WHERE user_id = %s AND topic_id = %s", (user_id, topic_id))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result[0] is not None else 0


# Function to save the user's score
def save_score(user_id, topic_id, score):
    # First, check if the score is in the top 10 for this topic
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM scores WHERE topic_id = %s", (topic_id,))
    count = cursor.fetchone()[0]
    cursor.close()
