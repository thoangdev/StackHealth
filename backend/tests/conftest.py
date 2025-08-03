import pytest
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import get_db, Base

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }


@pytest.fixture
def authenticated_client(client, test_user_data):
    # Register user
    client.post("/auth/register", json=test_user_data)
    
    # Login to get token
    response = client.post("/auth/login", json=test_user_data)
    token = response.json()["access_token"]
    
    # Set authorization header
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def sample_product_data():
    return {
        "name": "Test Product",
        "description": "A test product for testing"
    }


@pytest.fixture
def sample_scorecard_data():
    return {
        "product_id": 1,
        "category": "security",
        "date": "2025-08-02",
        "breakdown": {
            "sast": True,
            "dast": False,
            "sast_dast_in_ci": True
        }
    }
