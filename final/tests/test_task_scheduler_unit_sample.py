from __future__ import annotations

from rover.resource import Resource, ResourceType
from rover.task import Task
from rover.resource_pool import ResourcePool
from rover.task_scheduler import TaskScheduler

class ResourcePoolHasResourcesMock:
    def find_available_resource(
        self, res_type: ResourceType
    ) -> Resource | None:
        return Resource(1, res_type)

    def find_resource_to_yield(
        self, res_type: ResourceType, priority_threshold: int
    ) -> Resource | None:
        t = Task(priority_threshold, [], 5)
        r = Resource(2, res_type)
        r.allocate_by(t)
        return r
    
class TaskPoolMock():
    pass


def test_scheduler(monkeypatch):
    def mock_always_find_available_resource(
        self, res_type: ResourceType
    ) -> Resource | None:
        return Resource(1, res_type)

    poolMock = ResourcePoolHasResourcesMock()
    r = poolMock.find_available_resource(ResourceType.ARM)
    assert r.id == 1 and r.type == ResourceType.ARM
    sched = TaskScheduler(poolMock, TaskPoolMock(), 1)

    monkeypatch.setattr(
        ResourcePool,
        "find_available_resource",
        mock_always_find_available_resource
    )

    pool = ResourcePool()
    r = pool.find_available_resource(ResourceType.ANTENNA)
    assert r.id == 1 and r.type == ResourceType.ANTENNA


