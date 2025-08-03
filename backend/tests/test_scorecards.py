import pytest
from tests.conftest import authenticated_client, sample_scorecard_data, sample_product_data


class TestScorecards:
    """Test scorecard management endpoints"""

    def test_create_scorecard(self, authenticated_client, sample_product_data, sample_scorecard_data):
        """Test creating a new scorecard"""
        # Create a product first
        product_response = authenticated_client.post("/products", json=sample_product_data)
        product_id = product_response.json()["id"]
        
        # Update scorecard data with correct product_id
        sample_scorecard_data["product_id"] = product_id
        
        # Create scorecard
        response = authenticated_client.post("/scorecards", json=sample_scorecard_data)
        assert response.status_code == 201
        assert response.json()["category"] == sample_scorecard_data["category"]
        assert response.json()["score"] is not None

    def test_get_scorecards(self, authenticated_client, sample_product_data, sample_scorecard_data):
        """Test retrieving scorecards"""
        # Create a product and scorecard first
        product_response = authenticated_client.post("/products", json=sample_product_data)
        product_id = product_response.json()["id"]
        sample_scorecard_data["product_id"] = product_id
        authenticated_client.post("/scorecards", json=sample_scorecard_data)
        
        # Get scorecards
        response = authenticated_client.get("/scorecards")
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_scorecard_by_id(self, authenticated_client, sample_product_data, sample_scorecard_data):
        """Test retrieving a specific scorecard"""
        # Create a product and scorecard first
        product_response = authenticated_client.post("/products", json=sample_product_data)
        product_id = product_response.json()["id"]
        sample_scorecard_data["product_id"] = product_id
        scorecard_response = authenticated_client.post("/scorecards", json=sample_scorecard_data)
        scorecard_id = scorecard_response.json()["id"]
        
        # Get specific scorecard
        response = authenticated_client.get(f"/scorecards/{scorecard_id}")
        assert response.status_code == 200
        assert response.json()["id"] == scorecard_id

    def test_update_scorecard(self, authenticated_client, sample_product_data, sample_scorecard_data):
        """Test updating a scorecard"""
        # Create a product and scorecard first
        product_response = authenticated_client.post("/products", json=sample_product_data)
        product_id = product_response.json()["id"]
        sample_scorecard_data["product_id"] = product_id
        scorecard_response = authenticated_client.post("/scorecards", json=sample_scorecard_data)
        scorecard_id = scorecard_response.json()["id"]
        
        # Update scorecard
        updated_data = sample_scorecard_data.copy()
        updated_data["breakdown"]["dast"] = True
        
        response = authenticated_client.put(f"/scorecards/{scorecard_id}", json=updated_data)
        assert response.status_code == 200
        assert response.json()["breakdown"]["dast"] == True

    def test_delete_scorecard(self, authenticated_client, sample_product_data, sample_scorecard_data):
        """Test deleting a scorecard"""
        # Create a product and scorecard first
        product_response = authenticated_client.post("/products", json=sample_product_data)
        product_id = product_response.json()["id"]
        sample_scorecard_data["product_id"] = product_id
        scorecard_response = authenticated_client.post("/scorecards", json=sample_scorecard_data)
        scorecard_id = scorecard_response.json()["id"]
        
        # Delete scorecard
        response = authenticated_client.delete(f"/scorecards/{scorecard_id}")
        assert response.status_code == 200
        
        # Verify deletion
        get_response = authenticated_client.get(f"/scorecards/{scorecard_id}")
        assert get_response.status_code == 404

    def test_scorecard_scoring_calculation(self, authenticated_client, sample_product_data):
        """Test that scoring calculation works correctly"""
        # Create product
        product_response = authenticated_client.post("/products", json=sample_product_data)
        product_id = product_response.json()["id"]
        
        # Test high score scenario
        high_score_data = {
            "product_id": product_id,
            "category": "security",
            "date": "2025-08-02",
            "breakdown": {
                "sast": True,
                "dast": True,
                "sast_dast_in_ci": True,
                "triaging_findings": True,
                "secrets_scanning": True
            }
        }
        
        response = authenticated_client.post("/scorecards", json=high_score_data)
        high_score = response.json()["score"]
        
        # Test low score scenario
        low_score_data = {
            "product_id": product_id,
            "category": "security",
            "date": "2025-08-01",
            "breakdown": {
                "sast": False,
                "dast": False,
                "sast_dast_in_ci": False,
                "triaging_findings": False,
                "secrets_scanning": False
            }
        }
        
        response = authenticated_client.post("/scorecards", json=low_score_data)
        low_score = response.json()["score"]
        
        # High score should be greater than low score
        assert high_score > low_score

    def test_cicd_dora_metrics_scoring(self, authenticated_client, sample_product_data):
        """Test CI/CD DORA metrics scoring"""
        # Create product
        product_response = authenticated_client.post("/products", json=sample_product_data)
        product_id = product_response.json()["id"]
        
        # Test excellent DORA metrics
        excellent_cicd = {
            "product_id": product_id,
            "category": "cicd",
            "date": "2025-08-02",
            "breakdown": {
                "deployment_frequency": 4,  # On-demand
                "lead_time": 4,  # Less than one day
                "mttr": 4,  # Less than one hour
                "change_failure_rate": 4,  # 0-15%
                "automated_builds": True,
                "automated_tests": True,
                "deployment_pipeline": True
            }
        }
        
        response = authenticated_client.post("/scorecards", json=excellent_cicd)
        excellent_score = response.json()["score"]
        
        # Test poor DORA metrics
        poor_cicd = {
            "product_id": product_id,
            "category": "cicd",
            "date": "2025-08-01",
            "breakdown": {
                "deployment_frequency": 1,  # Monthly
                "lead_time": 1,  # More than one month
                "mttr": 1,  # More than a week
                "change_failure_rate": 1,  # More than 30%
                "automated_builds": False,
                "automated_tests": False,
                "deployment_pipeline": False
            }
        }
        
        response = authenticated_client.post("/scorecards", json=poor_cicd)
        poor_score = response.json()["score"]
        
        # Excellent score should be significantly higher
        assert excellent_score > poor_score
        assert excellent_score > 70  # Should be high score
        assert poor_score < 40  # Should be low score
