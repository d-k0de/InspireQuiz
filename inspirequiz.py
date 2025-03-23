import mysql.connector
import random

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",  # Replace with your host (e.g., localhost)
    user="root",       # Replace with your MySQL username
    password="****",  # Replace with your MySQL password
    database="inspirequiz"  # The database to use
)

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
    cursor = db.cursor()
    # Check if the combination of user_id and topic_id already exists
    cursor.execute("SELECT score FROM scores WHERE user_id = %s AND topic_id = %s", (user_id, topic_id))
    existing_score = cursor.fetchone()

    if existing_score:
        # Update the score only if the new score is higher
        if score > existing_score[0]:
            cursor.execute("UPDATE scores SET score = %s WHERE user_id = %s AND topic_id = %s", (score, user_id, topic_id))
            print(f"Updated your high score to {score}!")
    else:
        # Insert a new record if it doesn't exist
        cursor.execute("INSERT INTO scores (user_id, topic_id, score) VALUES (%s, %s, %s)", (user_id, topic_id, score))
    db.commit()
    cursor.close()

# Function to get Resources from db
def get_resources_for_topic(topic_id):
    cursor = db.cursor()
    cursor.execute("SELECT title, link FROM resources WHERE topic_id = %s", (topic_id,))
    resources = cursor.fetchall()
    cursor.close()
    return resources

# Main function to start the app
def main():
    print("Welcome to InspireQuiz! An interactive learning and motivational tool.")
    get_random_start_quote()  # Display a random motivational quote at app start
    while True:
        print("\nMain Menu:")
        print("1. Start Learning")
        print("2. Get Motivated")
        print("3. Exit")

        choice = input("Choose an option (1-3): ")

        if choice == "1":
            start_learning()
        elif choice == "2":
            get_motivated()
        elif choice == "3":
            print("Thank you for using InspireQuiz! Keep learning and stay motivated.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

# Function for displaying motivational quotes
def get_motivated():
    print("\nChoose a motivational speaker:")
    speakers = get_motivational_speakers()  # Fetch speakers from the database
    if not speakers:
        print("No motivational speakers found in the database.")
        return

    for i, speaker in enumerate(speakers, 1):
        print(f"{i}. {speaker}")

    try:
        speaker_choice = int(input("Enter the speaker number: ")) - 1
        if 0 <= speaker_choice < len(speakers):
            selected_speaker = speakers[speaker_choice]
            quote = get_quote_by_speaker(selected_speaker)
            if quote:
                print(f"\n\"{quote}\" – {selected_speaker}")
            else:
                print(f"No quotes available for {selected_speaker}.")
        else:
            print("Invalid choice. Returning to main menu.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Function to view resources
def view_resources(topic_id):
    resources = get_resources_for_topic(topic_id)
    if resources:
        print("\nResources:")
        for i, (title, link) in enumerate(resources, 1):
            print(f"{i}. {title} - {link}")
    else:
        print("Sorry, no available resources for this topic now.")
    input("\nPress any key to return to the main menu.")

# Function for starting the learning session
def start_learning():
    topics = get_topics()  # Fetch topics from the database
    print("\nChoose a topic to learn:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic[1]}")  # topic[1] contains the topic name

    try:
        topic_choice = int(input("Enter the topic number: ")) - 1
        if 0 <= topic_choice < len(topics):
            selected_topic = topics[topic_choice]
            topic_id = selected_topic[0]  # topic_id is the first column
            print(f"\nYou selected: {selected_topic[1]}")
            print("1. View Resources")
            print("2. Take Quiz")
            action_choice = input("Choose an option (1-2): ")

            # Example user_id, replace this with actual user ID (e.g., from session data)
            user_id = 1  # Replace with the logged-in user's ID

            if action_choice == "1":
                view_resources(topic_id)  # View resources for the selected topic
            elif action_choice == "2":
                take_quiz(topic_id, user_id)  # Pass both topic_id and user_id to the quiz function
            else:
                print("Invalid choice. Returning to main menu.")
        else:
            print("Invalid topic number. Returning to main menu.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Function for taking a quiz
def take_quiz(topic_id, user_id):
    # Get the user's highest score for this topic
    highest_score = get_highest_score(user_id, topic_id)
    print(f"\nStarting quiz for the selected topic.")
    print(f"Your highest score obtained for this topic is: {highest_score}")
    print("You can type A, B, C, D OR a, b, c, d to choose answer, and 'END' at any time to stop the quiz.")  # This will only display once

    asked_questions = []  # Initialize the list to track asked questions
    total_score = 0
    total_questions = 20
    question_count = 0

    while question_count < total_questions:
        question_data = get_random_question(topic_id, asked_questions)

        if not question_data:
            print("No more unique questions available. Ending the quiz.")
            break

        # Display the question and options
        print(f"\nQ{question_count + 1}: {question_data['question']}")
        print(f"A) {question_data['options'][0]}")
        print(f"B) {question_data['options'][1]}")
        print(f"C) {question_data['options'][2]}")
        print(f"D) {question_data['options'][3]}")

        # Ask the user for their answer, and allow 'END' to stop the quiz
        user_answer = input("Your answer: ").upper()

        if user_answer == 'END':
            print("Quiz ended.")
            break

        # Check if the user's answer is correct
        if user_answer == question_data['correct_option']:
            print("Correct!")
            total_score += 1
        else:
            print(f"Incorrect! The correct answer is {question_data['correct_option']}.")

        question_count += 1

    print(f"\nQuiz complete! Your total score is: {total_score}/{question_count}")

    # Save the score if it's higher than the previous highest score
    if total_score > highest_score:
        save_score(user_id, topic_id, total_score)
        print(f"New high score: {total_score}!")
    else:
        print(f"Your score did not exceed your high score of {highest_score}.")




# Run the application
if __name__ == "__main__":
    main()
