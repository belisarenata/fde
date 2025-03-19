from fastapi.testclient import TestClient
from app import app
from enums import Stacks

client = TestClient(app)

def test_standard_package():
    response = client.post("/sort", 
        json=
        {
            "width": 100,
            "height": 100,
            "length": 100,
            "mass": 10
        })
    assert response.status_code == 200

    assert response.text == Stacks.STANDARD.value

def test_bulky_package_volume():
    package = {
        "width": 100,
        "height": 100,
        "length": 100.1,  # Just over 1,000,000 cm³
        "mass": 10
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 200
    assert response.text == Stacks.SPECIAL.value

def test_bulky_package_dimension():
    package = {
        "width": 151,  # Over 150cm
        "height": 100,
        "length": 100,
        "mass": 10
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 200
    assert response.text == Stacks.SPECIAL.value

def test_heavy_package():
    package = {
        "width": 100,
        "height": 100,
        "length": 100,
        "mass": 21  # Over 20kg
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 200
    assert response.text == Stacks.SPECIAL.value

def test_rejected_package():
    package = {
        "width": 101,
        "height": 100,
        "length": 100,
        "mass": 21
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 200
    assert response.text == Stacks.REJECTED.value

def test_invalid_package_negative_values():
    package = {
        "width": -1,
        "height": 100,
        "length": 100,
        "mass": 10
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 422  # Validation error

def test_invalid_package_negative_mass_values():
    package = {
        "width": 10,
        "height": 100,
        "length": 100,
        "mass": -10
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 422  # Validation error


def test_invalid_package_missing_values():
    package = {
        "width": 100,
        "height": 100
        # missing length and mass
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 422  # Validation error

def test_invalid_package_zero_values():
    package = {
        "width": 0,
        "height": 100,
        "length": 100,
        "mass": 10
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 422  # Validation error


def test_invalid_package_str_values():
    package = {
        "width": "abc",
        "height": 100,
        "length": 100,
        "mass": 10
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 422  # Validation error
