from rover.resource import Resource, ResourceType

class ResourcePool:
    def __init__(self) -> None:
        self.resources: dict[ResourceType, list[Resource]] = {}
        self._detect_resources()

    def find_available_resource(self, res_type: ResourceType) -> Resource | None:
        for res in self.resources.get(res_type, []):
            if res.is_available():
                return res
        return None
    
    def find_resource_to_yield(self, res_type: ResourceType, priority_threshold: int) -> Resource | None:
        for res in self.resources.get(res_type, []):
            if res.allocated_to is None:
                continue
            if res.allocated_to.priority < priority_threshold:
                return res
        return None
    
    def _detect_resources(self) -> None:
        # Some complicated piece of code that scans the rover's resources
        pass