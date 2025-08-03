import pytest
from tests.conftest import client, test_user_data


class TestAuth:
    """Test authentication endpoints"""

    def test_register_new_user(self, client, test_user_data):
        """Test user registration"""
        response = client.post("/auth/register", json=test_user_data)
        assert response.status_code == 201
        assert response.json()["email"] == test_user_data["email"]

    def test_register_duplicate_user(self, client, test_user_data):
        """Test registration with duplicate email"""
        # Register first time
        client.post("/auth/register", json=test_user_data)
        
        # Try to register again
        response = client.post("/auth/register", json=test_user_data)
        assert response.status_code == 400

    def test_login_valid_credentials(self, client, test_user_data):
        """Test login with valid credentials"""
        # Register user first
        client.post("/auth/register", json=test_user_data)
        
        # Login
        response = client.post("/auth/login", json=test_user_data)
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client, test_user_data):
        """Test login with invalid credentials"""
        # Register user first
        client.post("/auth/register", json=test_user_data)
        
        # Try login with wrong password
        invalid_data = {
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=invalid_data)
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post("/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "password"
        })
        assert response.status_code == 401

    def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token"""
        response = client.get("/products")
        assert response.status_code == 401

    def test_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        client.headers.update({"Authorization": "Bearer invalid_token"})
        response = client.get("/products")
        assert response.status_code == 401
