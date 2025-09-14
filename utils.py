import requests
import html
from rich.console import Console

console = Console()
API_BASE_URL = "https://opentdb.com/"

def get_category_list():
    """Fetches the list of available quiz categories from the API."""
    url = API_BASE_URL + "api_category.php"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        # Create a dictionary of {id: name}
        return {cat['id']: cat['name'] for cat in data.get('trivia_categories', [])}
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]API Error: Could not fetch categories. {e}[/bold red]")
        return None

def fetch_quiz_questions(amount=10, category=None, difficulty=None, quiz_type=None):
    """
    Fetches a specified number of questions from the Open Trivia Database.
    """
    params = {
        'amount': amount,
        'category': category,
        'difficulty': difficulty,
        'type': quiz_type
    }
    # Clean up params: remove any keys with a None value
    params = {k: v for k, v in params.items() if v is not None}

    url = API_BASE_URL + "api.php"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Check API response code
        if data.get('response_code') != 0:
            console.print(f"[bold red]API returned an error. It might not have enough questions for your specific query.[/bold red]")
            return []

        # Clean HTML entities from questions and answers
        for question_data in data.get('results', []):
            question_data['question'] = html.unescape(question_data['question'])
            question_data['correct_answer'] = html.unescape(question_data['correct_answer'])
            question_data['incorrect_answers'] = [html.unescape(ans) for ans in question_data['incorrect_answers']]

        return data.get('results', [])

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]API Error: Could not fetch questions. {e}[/bold red]")
        return []

