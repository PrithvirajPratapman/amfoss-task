import time
import random
import threading
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

class QuizEngine:
    """Handles the main quiz logic, including timers and scoring."""

    def __init__(self, questions, time_limit, user_profile):
        self.questions = questions
        self.time_limit = time_limit
        self.user_profile = user_profile
        self.current_question_index = 0
        self.score = 0
        self.timer_expired = threading.Event()
        self.user_answer = None

    def _timer_countdown(self):
        """
        A countdown timer that runs in a separate thread.
        It waits 1 second at a time and stops if the user answers.
        """
        for _ in range(self.time_limit):
            # wait(1) returns True if the event is set, otherwise False after 1 sec
            if self.timer_expired.wait(1):
                return
        # If the loop completes, time is up, so we set the event
        self.timer_expired.set()

    def ask_question(self, question_data):
        """Displays a question and its options, and starts the timer."""
        # Reset state for the new question
        self.timer_expired.clear()
        self.user_answer = None

        console.print(Panel(f"[bold blue]{question_data['question']}[/bold blue]", title=f"Question {self.current_question_index + 1}/{len(self.questions)}"))

        options = question_data['incorrect_answers'] + [question_data['correct_answer']]
        random.shuffle(options)

        choices = {}
        for i, option in enumerate(options, 1):
            choices[str(i)] = option
            console.print(f"  [yellow]{i}[/yellow]. {option}")

        # Start the timer in a background thread
        timer_thread = threading.Thread(target=self._timer_countdown)
        timer_thread.start()

        # Prompt for user input in the main thread
        self.user_answer = Prompt.ask("Your answer (number)", choices=list(choices.keys()), default=None)

        # If user answered, set the event to stop the timer thread immediately
        if not self.timer_expired.is_set():
            self.timer_expired.set()

        # Wait for the timer thread to complete its execution
        timer_thread.join()

        # Check if the user ran out of time (user_answer would still be None)
        if self.user_answer is None:
            console.print("\n[bold red]Time's up![/bold red]")
            return False

        # Check if the provided answer is correct
        return choices.get(self.user_answer) == question_data['correct_answer']

    def run_quiz(self):
        """Main loop to run through all the questions."""
        self.score = 0 # Reset score for the session
        for i, question in enumerate(self.questions):
            self.current_question_index = i
            is_correct = self.ask_question(question)

            if is_correct:
                self.score += 1
                console.print("[bold green]Correct! You earned a point.[/bold green]\n")
            else:
                correct_answer = question['correct_answer']
                console.print(f"[bold red]Sorry, that's incorrect.[/bold red] The correct answer was: [green]{correct_answer}[/green]\n")

        # After the quiz is done, update the user's total score
        self.user_profile.add_score(self.score)
        console.print(f"Quiz finished! You scored [bold yellow]{self.score}/{len(self.questions)}[/bold yellow] in this session.")

