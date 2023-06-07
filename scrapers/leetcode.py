# inspired by https://github.com/Bishalsarang/Leetcode-Questions-Scraper/blob/master/main.py
import json
from typing import Any

import requests

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
    # List to store question_title_slug
    links = []
    for child in algorithms_problems_json["stat_status_pairs"]:
        # Only process free problems 'if not child["paid_only"]:'
        question__article__slug = get_editorial_url(child)
        question__title = child["stat"]["question__title"]
        frontend_question_id = child["stat"]["frontend_question_id"]
        difficulty = child["difficulty"]["level"]
        question_url = get_challenge_url(child)
        links.append(
            (
                difficulty,
                frontend_question_id,
                question__title,
                question_url,
                question__article__slug,
            )
        )

    # Sort by problem id in ascending order and then by difficulty
    links = sorted(links, key=lambda x: (x[2], x[1]))

    for i in links:
        print(i)


if __name__ == "__main__":
    main()
