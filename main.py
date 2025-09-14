from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

# Corrected imports for files in the same directory
from quiz_engine import QuizEngine
from user_profile import UserProfile
from utils import get_category_list, fetch_quiz_questions

console = Console()

def main():
    """Main function to run the TimeTickQuiz application."""
    console.print(Panel("[bold yellow]Welcome to TimeTickQuiz - A Magic Library Adventure![/bold yellow]"))

    username = Prompt.ask("Enter your username, recruit")
    user_profile = UserProfile(username)

    while True:
        console.print("\n[bold]Let's set up your quiz![/bold]")

        num_questions = IntPrompt.ask("How many questions (1-20)?", default=5)
        time_limit = IntPrompt.ask("How much time per question in seconds (10-30)?", default=15)

        # Fetch and display categories
        categories = get_category_list()
        if not categories:
            console.print("[bold red]Could not fetch categories. Using defaults.[/bold red]")
            # Provide a fallback category if API fails
            categories = {9: "General Knowledge"}

        console.print("\n[bold]Choose a category:[/bold]")
        for cat_id, cat_name in categories.items():
            console.print(f"  [cyan]{cat_id}[/cyan]: {cat_name}")
        category = IntPrompt.ask("Category ID", choices=[str(c) for c in categories.keys()], default=9)

        difficulty = Prompt.ask("Difficulty", choices=['easy', 'medium', 'hard'], default='medium')
        quiz_type = Prompt.ask("Question type", choices=['multiple', 'boolean'], default='multiple')

        console.print("\n[green]Fetching questions from the magic book...[/green]")
        questions = fetch_quiz_questions(
            amount=num_questions,
            category=category,
            difficulty=difficulty,
            quiz_type=quiz_type
        )

        if questions:
            quiz = QuizEngine(questions, time_limit, user_profile)
            quiz.run_quiz()
            user_profile.save_profile()
            console.print(f"Your total score is now [bold yellow]{user_profile.score}[/bold yellow]. Well done!")
        else:
            console.print("[bold red]Could not start the quiz. Please try different settings.[/bold red]")

        play_again = Prompt.ask("\nPlay again?", choices=['yes', 'no'], default='yes')
        if play_again == 'no':
            console.print("[bold]Thanks for playing at the TimeTick Library! Come back soon![/bold]")
            break

if __name__ == "__main__":
    main()

