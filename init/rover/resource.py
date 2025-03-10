from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rover.task import Task

class ResourceType(Enum):
    CAMERA = 1
    ARM = 2
    ANTENNA = 3
    TEMPERATURE_SENSOR = 4

class ResourceStatus(Enum):
    AVAILABLE = 1
    IN_USE = 2
    BROKEN = 3

class Resource:
    def __init__(
        self,
        res_id: int,
        res_type: ResourceType,
        status: ResourceStatus = ResourceStatus.AVAILABLE
    ) -> None:
        self.id: int = res_id
        self.type: ResourceType = res_type
        self.status: ResourceStatus = status
        self.allocated_to: Task | None = None
    
    def is_available(self) -> bool:
        return self.status == ResourceStatus.AVAILABLE

    def allocate_by(self, task: Task) -> None:
        assert self.is_available()
        self.allocated_to = task
        self.status = ResourceStatus.IN_USE

    def yield_back(self) -> None:
        self.allocated_to = None
        self.status = ResourceStatus.IN_USE
