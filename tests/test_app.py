import pytest


def test_get_activities(client):
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    # Verify structure of an activity
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_for_activity(client):
    """Test signing up for an activity"""
    email = "test@mergington.edu"
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity"""
    email = "test@mergington.edu"
    activity = "NonExistentClub"
    
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_email(client):
    """Test signing up with duplicate email"""
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
    )
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_unregister_participant(client):
    """Test unregistering a participant"""
    # First sign up
    email = "newuser@mergington.edu"
    activity = "Basketball"
    
    signup_response = client.post(
        f"/activities/{activity}/signup?email={email}",
    )
    assert signup_response.status_code == 200
    
    # Now unregister
    unregister_response = client.delete(
        f"/activities/{activity}/unregister?email={email}",
    )
    assert unregister_response.status_code == 200
    data = unregister_response.json()
    assert "Unregistered" in data["message"]
    assert email in data["message"]


def test_unregister_activity_not_found(client):
    """Test unregister for non-existent activity"""
    email = "test@mergington.edu"
    activity = "NonExistentClub"
    
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}",
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_participant_not_found(client):
    """Test unregistering a participant not in activity"""
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}",
    )
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_root_redirect(client):
    """Test root path redirects to static index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"
