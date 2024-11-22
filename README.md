# InspireQuiz

InspireQuiz is an interactive Python application designed to provide users with a mix of motivation and education. It integrates motivational quotes, topic-specific resources, and quizzes to create a dynamic learning experience.

## Features

### Motivational Quotes
- Displays a random motivational quote on startup.
- Allows users to browse quotes by specific speakers.

### Learning Topics
- Lists topics for users to explore.
- Provides resources linked to each topic.

### Interactive Quizzes
- Presents randomized, multiple-choice questions from selected topics.
- Tracks and manages user scores with a leaderboard system.

### Resource Accessibility
- Offers curated resources for deeper understanding of topics.

## Prerequisites

- **Python**: Version 3.8 or higher.
- **MySQL Database**: Ensure the following tables are set up:
  - `quotes`: Stores motivational quotes.
  - `topics`: Stores topic details.
  - `questions`: Stores quiz questions.
  - `scores`: Tracks user scores.
  - `resources`: Stores topic-specific resources.

## Setup

1. Clone or download the repository.
2. Update the database connection details in the script:
   ```python
   db = mysql.connector.connect(
       host="localhost",       # Replace with your host
       user="root",            # Replace with your username
       password="yourpassword",# Replace with your password
       database="inspirequiz"  # Replace with your database name
   )
3. Run the script:
```python
python inspirequiz.py
```

## How to Use
1. Launch the Application: 
Displays a motivational quote upon startup.
2. Choose an Option:
 - Start Learning: Select a topic to view resources or take a quiz.
 - Get Motivated: Browse quotes from motivational speakers.
 - Exit: Close the application.
3. Take a Quiz:
 - Answer randomized questions.
 - Your score will be tracked and displayed on the leaderboard.

Enjoy learning and staying motivated with InspireQuiz! 😊
