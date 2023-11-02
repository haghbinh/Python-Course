import random

# Define a dictionary to store flashcards and their corresponding answers.
flashcards = {
    "What is the capital of France?": "Paris",
    "How many sides does a triangle have?": "3",
    "What is the chemical symbol for water?": "H2O",
}

# Function to start the flashcard quiz.
def start_flashcard_quiz():
    print("Welcome to the Flashcard Quiz App!")
    print("Type 'exit' to quit the quiz.")

    while True:
        question, answer = random.choice(list(flashcards.items()))
        user_input = input(f"{question} ")
        
        if user_input.lower() == "exit":
            break
        
        if user_input.lower() == answer.lower():
            print("Correct! Well done.")
        else:
            print(f"Sorry, the correct answer is: {answer}")

if __name__ == "__main__":
    start_flashcard_quiz()
