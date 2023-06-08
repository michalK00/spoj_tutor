# inspired by https://github.com/Bishalsarang/Leetcode-Questions-Scraper/blob/master/main.py
import json
from typing import Any, List
import requests

from utils import TaskRepresentation, get_amount_and_normalize_difficulty

# Leetcode API URL to get json of problems on algorithms categories
ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"
ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

# Load JSON from API
algorithms_problems_json = json.loads(requests.get(ALGORITHMS_ENDPOINT_URL).content)


def get_challenge_url(child: Any) -> str:
    return ALGORITHMS_BASE_URL + child["stat"]["question__title_slug"]


def get_editorial_url(child: Any) -> str | None:
    # when a question has an article it has a solution, but the solution URL is constructed like below
    if child["stat"]["question__article__slug"]:
        return get_challenge_url(child) + "/editorial"
    return None


def main():
    questions: List[TaskRepresentation] = []

    for child in algorithms_problems_json["stat_status_pairs"]:
        # Only process free problems
        # if not child["paid_only"]:

        questions.append(
            TaskRepresentation(
                difficulty=child["difficulty"]["level"],
                id_num=child["stat"]["frontend_question_id"],
                title=child["stat"]["question__title"],
                url=get_challenge_url(child),
                solution_url=get_editorial_url(child),
            )
        )

    get_amount_and_normalize_difficulty(questions)

    # Sort by problem id in ascending order and then by difficulty
    questions = sorted(questions, key=lambda x: (x[2], x[1]))

    for i in questions:
        print(i)


if __name__ == "__main__":
    main()
