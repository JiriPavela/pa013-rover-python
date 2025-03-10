import bisect
import itertools

from typing import Iterator

from rover.task import Task


class TaskPool:
    def __init__(self) -> None:
        self.id_counter = itertools.count()
        self.queue: list[Task] = []

    def __len__(self) -> int:
        return len(self.queue)

    def add_task(self, task: Task) -> None:
        task.id = next(self.id_counter)
        bisect.insort(self.queue, task)
    
    def remove_task(self, task: Task) -> None:
        position = self.queue.index(task)
        self.queue[position].yield_all_resources()
        self.queue.pop(position)
    
    def get_priority_tasks(self, count: int) -> Iterator[Task]:
        return (task for task in reversed(self.queue[-count:]))