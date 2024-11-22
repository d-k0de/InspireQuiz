Overview
InspireQuiz is an interactive Python application designed to provide users with a mix of motivation and education. It integrates motivational quotes, topic-specific resources, and quizzes to create a dynamic learning experience.
Features
Motivational Quotes
Displays a random motivational quote on startup.
Allows users to browse quotes by specific speakers.
Learning Topics
Lists topics for users to explore.
Provides resources linked to each topic.
Interactive Quizzes
Presents randomized, multiple-choice questions from selected topics.
Tracks and manages user scores with a leaderboard system.
Resource Accessibility
Offers curated resources for deeper understanding of topics.
Prerequisites
Python 3.8 or higher.
MySQL database setup with the following tables:
quotes: Stores motivational quotes.
topics: Stores topic details.
questions: Stores quiz questions.
scores: Tracks user scores.
resources: Stores topic-specific resources.

Setup
Clone or download the repository.
Update the database connection details in the script:
python
Copy code
db = mysql.connector.connect(
    host="localhost",       # Replace with your host
    user="root",            # Replace with your username
    password="yourpassword",# Replace with your password
    database="inspirequiz"  # Replace with your database name
)


Run the script:
bash
Copy code
python inspirequiz.py



How to Use
Launch the Application: Displays a motivational quote upon startup.
Choose an Option:
Start Learning: Select a topic to view resources or take a quiz.
Get Motivated: Browse quotes from motivational speakers.
Exit: Close the application.
Take a Quiz: Answer randomized questions, and your score will be tracked for the leaderboard.
Future Enhancements
User authentication for personalized profiles.
Advanced analytics for quiz performance.
Web or mobile version for broader accessibility.
Enjoy learning and staying motivated with InspireQuiz! 😊



