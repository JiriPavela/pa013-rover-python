from __future__ import annotations

from rover.task_pool import TaskPool
from rover.resource_pool import ResourcePool
from rover.task_scheduler import TaskScheduler


def run() -> None:
    TaskScheduler(ResourcePool(), TaskPool(), 3)
