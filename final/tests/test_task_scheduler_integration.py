from __future__ import annotations
from rover.task import Task, TaskState
from rover.task_pool import TaskPool
from rover.resource_pool import ResourcePool
from rover.task_scheduler import TaskScheduler

def validate_step(
    task_pool: TaskPool,
    expected_running_tasks: int,
    finished_tasks: list[Task],
    expected_finished_tasks: list[Task]
) -> None:
    assert(finished_tasks == expected_finished_tasks)
    tasks = task_pool.get_priority_tasks(len(task_pool))
    assert(len(list(tasks)) >= expected_running_tasks)
    for idx, task in enumerate(tasks):
        if idx < expected_running_tasks:
            assert(task.state == TaskState.RUNNING)
        else:
            assert(task.state != TaskState.RUNNING)
            assert(task.progress == 0)

def test_tasks_without_resources() -> None:
    max_tasks: int = 2
    task_pool = TaskPool()
    tasks = [Task(0, [], 1), Task(4, [], 4), Task(7, [], 3), Task(10, [], 2)]
    for t in tasks:
        task_pool.add_task(t)
    scheduler = TaskScheduler(ResourcePool(), task_pool, max_tasks)
    
    # (Number of running tasks, finished tasks) 
    expected_run: list[tuple[int, list[Task]]] = [
        (2, []), (1, [tasks[3]]), (1, [tasks[2]]), (1, [tasks[0]]),
        (1, []), (0, [tasks[1]])
    ]
    # Test that no task is running yet
    for task in task_pool.queue:
        assert(task.state != TaskState.RUNNING)
    # Test that at most max_tasks were run and that tasks are
    # removed from the pool when they finish
    for running_tasks, expected_f in expected_run:
        tasks_f = scheduler.step()
        validate_step(task_pool, running_tasks, tasks_f, expected_f)
    assert(len(task_pool) == 0) 
