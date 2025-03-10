from __future__ import annotations
from typing import Iterator
from rover.resource_pool import ResourcePool
from rover.task_pool import TaskPool
from rover.task import Task, TaskState

class TaskScheduler:
    def __init__(
        self,
        resource_pool: ResourcePool,
        task_pool: TaskPool,
        max_concurrent_tasks: int
    ) -> None:
        self.res_pool: ResourcePool = resource_pool
        self.task_pool: TaskPool = task_pool
        self.max_tasks: int = max_concurrent_tasks

    def step(self) -> list[Task]:
        finished_tasks: list[Task] = []
        for task in self._select_tasks():
            if self._run_task(task):
                finished_tasks.append(task)
        return finished_tasks

    # This function contains a bug
    def _select_tasks(self) -> Iterator[Task]:
        for task in self.task_pool.get_priority_tasks(self.max_tasks):
            resources = task.missing_resources()
            for res_t in resources:
                res = self.res_pool.find_available_resource(res_t)
                if res:
                    task.allocate_resource(res)
                else:
                    res = self.res_pool.find_resource_to_yield(
                        res_t, task.priority
                    )
                    if res and res.allocated_to:
                        res = res.allocated_to.yield_resource(res_t)
                        if res:
                            task.allocate_resource(res)
                        else:
                            break    
                    else:
                        break
            if not task.missing_resources():
                yield task

    def _run_task(self, task: Task) -> Task | None:
        assert task.state in (TaskState.READY, TaskState.RUNNING)
        if task.run() == TaskState.FINISHED:
            task.yield_all_resources()
            self.task_pool.remove_task(task)
            return task
        return None