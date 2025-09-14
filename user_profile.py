import json
import os
from rich.console import Console

console = Console()
# Correctly locate profiles.json one directory above the current (src) file
PROFILE_FILE = os.path.join(os.path.dirname(__file__), '..', 'profiles.json')

class UserProfile:
    """Manages user profiles, including loading and saving scores."""

    def __init__(self, username):
        if not username:
            raise ValueError("Username cannot be empty.")
        self.username = username
        self.score = 0
        self.profiles = self._load_profiles()
        self._load_user()

    def _load_profiles(self):
        """Loads all profiles from the JSON file."""
        try:
            # Create the file with an empty object if it doesn't exist
            if not os.path.exists(PROFILE_FILE):
                with open(PROFILE_FILE, 'w') as f:
                    json.dump({}, f)
                return {}
            
            with open(PROFILE_FILE, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            console.print(f"[bold red]Warning: Could not read profile file. Starting fresh.[/bold red]")
            return {}

    def _load_user(self):
        """Loads a specific user's score if they exist."""
        if self.username in self.profiles:
            self.score = self.profiles[self.username].get('score', 0)
            console.print(f"Welcome back, [bold cyan]{self.username}[/bold cyan]! Your current score is [bold yellow]{self.score}[/bold yellow].")
        else:
            console.print(f"Welcome, new recruit [bold cyan]{self.username}[/bold cyan]! Let's get you on the board.")
            self.profiles[self.username] = {'score': 0}

    def save_profile(self):
        """Saves the current user's score to the JSON file."""
        self.profiles[self.username]['score'] = self.score
        try:
            with open(PROFILE_FILE, 'w') as f:
                json.dump(self.profiles, f, indent=4)
        except IOError as e:
            console.print(f"[bold red]Error: Could not save profile data. {e}[/bold red]")

    def add_score(self, points):
        """Adds points to the user's current score."""
        self.score += points

