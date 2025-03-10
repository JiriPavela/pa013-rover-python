import pytest

from rover.resource import Resource, ResourceType, ResourceStatus

class TaskStub:
    pass

@pytest.fixture
def basic_resources() -> tuple[Resource, Resource]:
    r1 = Resource(10, ResourceType.CAMERA, ResourceStatus.IN_USE)
    r2 = Resource(5, ResourceType.ARM, ResourceStatus.AVAILABLE)
    return r1, r2

def test_resource_init():
    r1 = Resource(10, ResourceType.CAMERA, ResourceStatus.IN_USE)
    assert r1.id == 10
    assert r1.type == ResourceType.CAMERA
    assert r1.status == ResourceStatus.IN_USE
    assert r1.allocated_to == None

def test_resource_is_available(basic_resources):
    r1, r2 = basic_resources
    assert not r1.is_available()
    assert r2.is_available()

def test_resource_allocate_by(basic_resources):
    _, r1 = basic_resources
    assert r1.is_available()
    t = TaskStub()
    r1.allocate_by(t)
    assert not r1.is_available()
    assert r1.allocated_to == t

def test_resource_yield_back():
    r1 = Resource(5, ResourceType.ARM, ResourceStatus.AVAILABLE)
    assert r1.is_available()
    r1.allocate_by(TaskStub())
    r1.yield_back()
    assert r1.is_available()
    assert r1.allocated_to == None

def test_resource_yield_back_available():
    r1 = Resource(5, ResourceType.ARM, ResourceStatus.AVAILABLE)
    assert r1.is_available()
    r1.yield_back()
    assert r1.is_available()
