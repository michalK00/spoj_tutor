# inspired by https://github.com/Bishalsarang/Leetcode-Questions-Scraper/blob/master/main.py
import json
from typing import Any, Tuple
import requests

from utils import *

# Leetcode API URL to get json of problems on algorithms categories
ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"
ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"
LEETCODE_FILENAME = "leetcode.csv"

# Load JSON from API
algorithms_problems_json = json.loads(requests.get(ALGORITHMS_ENDPOINT_URL).content)


def get_challenge_url(child: Any) -> str:
    return ALGORITHMS_BASE_URL + child["stat"]["question__title_slug"]


def get_editorial_url(child: Any) -> str | None:
    # when a question has an article it has a solution, but the solution URL is constructed like below
    if child["stat"]["question__article__slug"]:
        return get_challenge_url(child) + "/editorial"
    return None


def get_all_task_objs() -> Tuple[int, List[TaskRepresentation]]:
    questions: List[TaskRepresentation] = []

    for child in algorithms_problems_json["stat_status_pairs"]:
        # Only process free problems
        # if not child["paid_only"]:

        questions.append(
            TaskRepresentation(
                difficulty=child["difficulty"]["level"],
                title=child["stat"]["question__title"],
                url=get_challenge_url(child),
                solution_url=get_editorial_url(child),
            )
        )

    difficulty_levels_amount = get_amount_and_normalize_difficulty(questions)

    # Sort by problem name in ascending order and then by difficulty
    questions = sorted(questions, key=lambda x: (x.title, x.difficulty))

    return difficulty_levels_amount, questions


def main() -> None:
    difficulty_levels_amount, tasks = get_all_task_objs()
    tasks_to_csv(LEETCODE_FILENAME, tasks)


if __name__ == "__main__":
    main()
