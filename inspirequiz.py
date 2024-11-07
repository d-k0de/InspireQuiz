import random

# Motivational quotes
quotes = {
    "Albert Einstein": ["Life is like riding a bicycle. To keep your balance, you must keep moving.",
                        "Imagination is more important than knowledge."],
    "Maya Angelou": ["You will face many defeats in life, but never let yourself be defeated.",
                     "If you don't like something, change it. If you can't change it, change your attitude."],
    "Nelson Mandela": ["It always seems impossible until it's done.",
                       "Education is the most powerful weapon which you can use to change the world."],
    "Steve Jobs": ["The only way to do great work is to love what you do.",
                   "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work."]
}


# Main function to start the app
def main():
    print("Welcome to InspireQuiz! An interactive learning and motivational tool.")
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

# Function for starting the learning session
def start_learning():
    topics = ["Computer Software/Hardware", "AI", "Linux System", "Intro to Python", "Data Structures and Algorithms"]
    print("\nChoose a topic to learn:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic}")
    
    try:
        topic_choice = int(input("Enter the topic number: ")) - 1
        if 0 <= topic_choice < len(topics):
            selected_topic = topics[topic_choice]
            print(f"\nYou selected: {selected_topic}")
            print("1. View Resources")
            print("2. Take Quiz")
            action_choice = input("Choose an option (1 or 2): ")
            
            if action_choice == "1":
                view_resources(selected_topic)
            elif action_choice == "2":
                take_quiz(selected_topic)
            else:
                print("Invalid choice. Returning to main menu.")
        else:
            print("Invalid topic number. Returning to main menu.")
    except ValueError:
        print("Invalid input. Please enter a number.")
