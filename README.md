TimeTickQuiz - A Magic Library Adventure!
The Premise
Welcome, Recruit!

You have found yourself in the enchanted TimeTick Library, a place where books come to life and challenge you with their secrets. But there's a magical rule: you must answer each question before the 15-second timer runs out, or the book will snap shut and the magic will fade!

The library's most powerful book is the Open Trivia API, filled with endless questions about animals, movies, history, and more. Your mission is to build a quiz game that can read from this book, brave its challenges, and become the wisest adventurer in the library. Be quick and be smart to earn your golden star!

Features
Dynamic Quiz Content: Fetches fresh questions directly from the Open Trivia Database API.

User Customization: Choose the number of questions, time limit, category, difficulty, and question type.

Timed Questions: A real-time countdown timer for each question, running on a separate thread to keep the pressure on!

Persistent Player Profiles: Your username and total score are saved in profiles.json, so your progress is never lost.

Beautiful CLI: A rich, colorful command-line interface powered by the rich library, with colors for questions, correct answers, and wrong answers.

Instant Feedback: Know immediately if your answer was correct and see the right answer if you were wrong.

How to Get Started
Follow these steps to set up and run your own TimeTickQuiz adventure.

1. Set Up the Directory
Make sure you have the project files organized in the following structure:

TimeTickQuiz/
├── src/
│   ├── main.py
│   ├── quiz_engine.py
│   ├── user_profile.py
│   └── utils.py
├── profiles.json
├── requirements.txt
└── README.md

2. Open a Terminal
Navigate to the root TimeTickQuiz folder in your terminal or open the folder in an editor like VS Code and use its integrated terminal.

3. Create a Virtual Environment
This keeps your project's dependencies isolated and clean.

python3 -m venv venv

4. Activate the Virtual Environment
You must activate the environment before installing packages.

On macOS/Linux:

source venv/bin/activate

On Windows:

venv\Scripts\activate

You will know it's active when you see (venv) at the start of your terminal prompt.

5. Install Required Packages
Use pip to install the libraries listed in requirements.txt.

pip install -r requirements.txt

6. Run the Game!
Navigate into the source folder and run the main script.

cd src
python main.py

The magic of the TimeTick Library awaits!

Technologies Used
Python 3

Open Trivia Database API for quiz questions.

requests library for making API calls.

rich library for a beautiful and interactive command-line interface.
