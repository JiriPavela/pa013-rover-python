from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rover.resource import ResourceType, Resource

class TaskState(Enum):
    WAITING = 1
    READY = 2
    RUNNING = 3
    FINISHED = 4

class Task:
    def __init__(
        self,
        priority: int,
        required_resources: list[ResourceType],
        required_time: int
    ) -> None:
        self.id: int = -1
        self.priority: int = priority
        self.req_resources: list[ResourceType] = required_resources
        self.req_time: int = required_time
        self.allocated: list[Resource] = []
        self.progress: int = 0
        self.state: TaskState = TaskState.WAITING
        self._update_state()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self.priority < other.priority or (
            self.priority == other.priority and self.id > other.id
        )

    def missing_resources(self) -> list[ResourceType]:
        missing = list(self.req_resources) 
        for res in self.allocated:
            missing.remove(res.type)
        return missing

    def allocate_resource(self, res: Resource) -> None:
        if res.is_available() and res.type in self.req_resources:
            res.allocate_by(self)
            self.allocated.append(res)
            self._update_state()

    def yield_resource(self, res_type: ResourceType) -> Resource | None:
        for idx, r in enumerate(self.allocated):
            if r.type == res_type:
                resource = self.allocated.pop(idx)
                resource.yield_back()
                self._update_state()
                return resource
        return None
    
    def yield_all_resources(self) -> None:
        while self.allocated:
            resource = self.allocated.pop()
            resource.yield_back()
        self._update_state()

    def run(self) -> TaskState:
        if self.state in (TaskState.RUNNING, TaskState.READY):
            self.state = TaskState.RUNNING
            self.progress += 1
            self._update_state()
        return self.state

    def _update_state(self) -> None:
        if self.progress >= self.req_time:
            self.state = TaskState.FINISHED
        missing = self.missing_resources()
        if missing:
            self.state = TaskState.WAITING
        elif self.state == TaskState.WAITING and not missing:
            self.state = TaskState.READY
