import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_standard_package():
    package = {
        "width": 100,
        "height": 100,
        "length": 100,
        "mass": 10
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 200
    assert response.json()["stack"] == "STANDARD"

def test_bulky_package_volume():
    package = {
        "width": 100,
        "height": 100,
        "length": 100.1,  # Just over 1,000,000 cm³
        "mass": 10
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 200
    assert response.json()["stack"] == "SPECIAL"

def test_bulky_package_dimension():
    package = {
        "width": 151,  # Over 150cm
        "height": 100,
        "length": 100,
        "mass": 10
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 200
    assert response.json()["stack"] == "SPECIAL"

def test_heavy_package():
    package = {
        "width": 100,
        "height": 100,
        "length": 100,
        "mass": 21  # Over 20kg
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 200
    assert response.json()["stack"] == "SPECIAL"

def test_rejected_package():
    package = {
        "width": 101,
        "height": 100,
        "length": 100,
        "mass": 21
    }
    response = client.post("/sort", json=package)
    assert response.status_code == 200
    assert response.json()["stack"] == "REJECTED"

def test_invalid_package_negative_values():
    package = {
        "width": -1,
        "height": 100,
        "length": 100,
        "mass": 10
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
