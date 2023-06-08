from typing import List, Dict


class TaskRepresentation:
    difficulty: int
    id: int
    title: str
    url: str
    solution_url: str

    def __init__(
            self,
            difficulty: int,
            id_num: int,
            title: str,
            url: str,
            solution_url: str,
    ):
        self.difficulty = difficulty
        self.id = id_num
        self.title = title
        self.url = url
        self.solution_url = solution_url

    def __str__(self):
        return (
            f"difficulty: {self.difficulty}; "
            f"id:{self.id}; "
            f"title: {self.title}; "
            f"url: {self.url}; "
            f"solution: {self.solution_url}"
        )


def get_amount_and_normalize_difficulty(
        list_of_tasks: List[TaskRepresentation],
        is_difficulty_descending=False
) -> int:
    if len(list_of_tasks) <= 0:
        return 0

    # Getting all difficulties of tasks
    list_of_difficulties: List[int] = []
    for task in list_of_tasks:
        list_of_difficulties.append(task.difficulty)

    # Getting unique, sorted values of these difficulties
    # and mapping them to their positions in the list
    # to be able to normalize the difficulties
    # e.g. difficulties [-10, 0, 10, 20] -> [0, 1, 2, 3]
    difficulty_positions: Dict[int:int] = {}

    for index, value in enumerate(
            sorted(set(list_of_difficulties), reverse=is_difficulty_descending)
    ):
        difficulty_positions[value] = index

    # Remapping the normalized difficulties
    for task in list_of_tasks:
        # The difficulty is guaranteed to exist in the dictionary
        task.difficulty = difficulty_positions[task.difficulty]

    return len(difficulty_positions)
