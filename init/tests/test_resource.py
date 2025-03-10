from rover.resource import Resource, ResourceType, ResourceStatus

def test_resource_init():
    r1 = Resource(10, ResourceType.CAMERA, ResourceStatus.IN_USE)
    assert r1.id == 10
    assert r1.type == ResourceType.CAMERA
    assert r1.status == ResourceStatus.IN_USE
    assert r1.allocated_to == None

def test_resource_is_available():
    r1 = Resource(10, ResourceType.CAMERA, ResourceStatus.IN_USE)
    r2 = Resource(5, ResourceType.ARM, ResourceStatus.AVAILABLE)
    assert not r1.is_available()
    assert r2.is_available()

def test_resource_yield_back_available():
    r1 = Resource(5, ResourceType.ARM, ResourceStatus.AVAILABLE)
    assert r1.is_available()
    r1.yield_back()
    assert r1.is_available()
