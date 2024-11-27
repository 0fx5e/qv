import subprocess
import sys
import requests
import random
import os
import signal
import html

# Function to check and install required libraries
def install_requirements():
    required_libraries = ['requests', 'random', 'os', 'signal', 'html']
    for lib in required_libraries:
        try:
            __import__(lib)  # Try importing the library
        except ImportError:
            print(f"\033[1;91m  [-] {lib} not found! Installing...\033[0m")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# Call the install_requirements function before the main functionality
install_requirements()

# Mapping user-friendly categories to OpenTDB category IDs
CATEGORY_MAP = {
    "1": 9,   # General
    "2": 10,  # Books
    "3": 11,  # Film
    "4": 12,  # Music
    "5": 14,  # Television
    "6": 15,  # VideoGames
    "7": 16,  # BoardGames
    "8": 17,  # Science
    "9": 18,  # Computers
    "10": 19, # Mathematics
    "11": 20, # Mythology
    "12": 21, # Sports
    "13": 22, # Geography
    "14": 23, # History
    "15": 24, # Politics
    "16": 25, # Art
    "17": 26, # Celebrities
    "18": 27, # Animals
    "19": 28, # Vehicles
    "20": 29, # Comics
    "21": 30, # Gadgets
    "22": 31, # Anime
    "23": 32, # Cartoon
    "24": 13, # Theatre
    "25": None  # Random
}

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def linex():
    print('\033[1;93m  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m')

def display_logo():
    logo = '''
    
    
\033[1;96m  █▀█ █░█ █ ▀█ █░█ █▀▀ █▀█ █▀ █▀▀    
  ▀▀█ █▄█ █ █▄ ▀▄▀ ██▄ █▀▄ ▄█ ██▄   
  \033[1;94m  
  Version: 1.0
  Created by: 0fx5e|zyte
  
  Simple quiz game powered by Opentdb API
\033[0m'''
    print(logo)

def display_categories():
    categories = [
        "General", "Books", "Film", "Music", "Television",
        "VideoGames", "BoardGames", "Science", "Computers", "Mathematics",
        "Mythology", "Sports", "Geography", "History", "Politics",
        "Art", "Celebrities", "Animals", "Vehicles", "Comics",
        "Gadgets", "Anime", "Cartoon", "Theatre", "Random"
    ]

    print("\033[1;95m  [::] Quiz Categories [::]\033[0m\n")
    for i in range(0, len(categories), 2):
        row = categories[i:i+2]
        row_display = "  ".join(
            [f"\033[1;94m[{i+j+1:02d}] {cat:<20}\033[0m" for j, cat in enumerate(row)]
        )
        print(f"  {row_display}")
    print("")
    linex()

def fetch_questions(category=None, difficulty=None, num_questions=10):
    url = "https://opentdb.com/api.php"
    params = {
        "amount": num_questions,
        "type": "multiple"
    }

    # Map the user-selected category to OpenTDB category
    if category and category in CATEGORY_MAP and CATEGORY_MAP[category] is not None:
        params["category"] = CATEGORY_MAP[category]
    if difficulty:
        params["difficulty"] = difficulty

    response = requests.get(url, params=params)
    data = response.json()

    if data["response_code"] == 0:
        return data["results"]
    else:
        print("\033[1;91m[-] Failed to fetch questions. Please try again.\033[0m")
        return []

def decode_html_entities(text):
    return html.unescape(text)

def run_quiz(questions, category_name):
    score = 0
    for index, question in enumerate(questions, 1):
        clear_screen()
        display_logo()

        # Display category name above the question number
        print(f"\033[1;92m  [-] Category : {category_name}\033[0m\n")

        # Display question number in the format [-] Question 1/1 in green
        print(f"\033[1;92m  [-] Question {index}/{len(questions)}\033[0m\n")

        # Display the question with the number [1] in green
        decoded_question = decode_html_entities(question['question'])
        print(f"  \033[1;93m[{index}\033[93m] {decoded_question}\n")

        # Shuffle the options and display them in blue
        options = question["incorrect_answers"] + [question["correct_answer"]]
        random.shuffle(options)
        option_labels = ['A', 'B', 'C', 'D']

        for label, option in zip(option_labels, options):
            decoded_option = decode_html_entities(option)
            print(f"\033[1;94m  [{label}] {decoded_option}")  # Blue for choices

        while True:
            # Prompt for the user's answer in yellow
            user_answer = input("\n  \033[1;93m[-] Your answer : \033[0m").strip().upper()
            if user_answer in option_labels:
                selected_option = options[option_labels.index(user_answer)]
                if selected_option == question["correct_answer"]:
                    print("\033[1;92m  [-] Correct!\033[0m")
                    score += 1
                else:
                    correct_option_index = options.index(question["correct_answer"])
                    correct_label = option_labels[correct_option_index]
                    correct_answer = decode_html_entities(question["correct_answer"])
                    print(f"\033[1;91m  [-] Wrong!\033[91m The correct answer was: \033[1;92m{correct_label} : {correct_answer}\033[0m")
                break
            else:
                print("\033[1;91m  [-] Invalid choice! Please select A, B, C, or D.\033[0m")

        input("\n  \033[1;93m[-] Press Enter to continue...")

    clear_screen()
    display_logo()
    print(f"\033[1;92m  [-] Your final score is: {score}/{len(questions)}\033[0m")
    input("\n\033[1;93m  [-] Press Enter to start a new quiz...")

def signal_handler(sig, frame):
    print("\n\033[1;91m  [-] Thank you for playing QuizVerse! Goodbye!\033[0m")
    exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        clear_screen()
        display_logo()
        display_categories()

        while True:
            category = input("\n\033[1;93m  [-] Select category : \033[0m").strip()
            if category in CATEGORY_MAP:
                break
            print("\033[1;91m  [-] Invalid category! Please select a valid option (1-25).\033[0m")

        print("\n\033[1;95m  [::] Difficulty Levels [::] \n\033[0m")
        print("  \033[1;94m[1] Easy\033[0m")
        print("  \033[1;94m[2] Medium\033[0m")
        print("  \033[1;94m[3] Hard\033[0m")
        difficulty = input("\033[1;93m  \n  [-] Select difficulty : \033[0m").strip().upper()
        if difficulty == "2":
            difficulty = "medium"
        elif difficulty == "3":
            difficulty = "hard"
        else:
            difficulty = "easy"

        num_questions = input("\n\033[1;93m  [-] How many questions you want? \033[0m").strip()
        try:
            num_questions = int(num_questions) if num_questions else 10
        except ValueError:
            print("\033[1;91m  [-] Invalid input, defaulting to 10 questions.\033[0m")
            num_questions = 10

        questions = fetch_questions(category, difficulty, num_questions)
        if questions:
            category_name = list(CATEGORY_MAP.keys())[list(CATEGORY_MAP.values()).index(CATEGORY_MAP[category])]
            run_quiz(questions, category_name)

if __name__ == "__main__":
    main()
