import requests
from typing import Any, List, Tuple
from utils import *

CODEFORCES_ENDPOINT_URL = "https://codeforces.com/api/problemset.problems"
CODEFORCES_BASE_URL = "https://codeforces.com/"
CODEFORCES_FILENAME = "codeforces.csv"


def get_challenge_url(child: Any) -> str:
    return f"{CODEFORCES_BASE_URL}/problemset/problem/{child['contestId']}/{child['index']}"


def get_all_task_objs() -> Tuple[int, List[TaskRepresentation]]:
    # Retrieve all problems
    response = requests.get(CODEFORCES_ENDPOINT_URL)
    data = response.json()["result"]["problems"]

    questions: List[TaskRepresentation] = []

    # Process the retrieved problems
    for problem in data:
        # Access the desired information about each problem

        questions.append(
            TaskRepresentation(
                difficulty=problem.get("rating", 0),  # there are unrated problems, rating them as easy!
                title=problem["name"],
                url=get_challenge_url(problem),
                solution_url="",
            )
        )

    difficulty_levels_amount = get_amount_and_normalize_difficulty(questions)

    # Sort by problem name in ascending order and then by difficulty
    questions = sorted(questions, key=lambda x: (x.title, x.difficulty))

    return difficulty_levels_amount, questions


def main() -> None:
    difficulty_levels_amount, tasks = get_all_task_objs()
    tasks_to_csv(CODEFORCES_FILENAME, tasks)


if __name__ == "__main__":
    main()
