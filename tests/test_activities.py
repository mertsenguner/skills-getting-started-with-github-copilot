import pytest


def test_get_activities_returns_activity_list(client):
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Training",
        "Art Club",
        "Drama Club",
        "Math Olympiad",
        "Science Club",
        "SikSok Klübü2",
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert set(expected_activities).issubset(set(data.keys()))
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    test_email = "teststudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {test_email} for {activity_name}"}

    activity_response = client.get("/activities")
    assert test_email in activity_response.json()[activity_name]["participants"]


def test_signup_for_activity_fails_when_already_signed_up(client):
    # Arrange
    activity_name = "Programming Class"
    existing_participant = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={existing_participant}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_participant(client):
    # Arrange
    activity_name = "Gym Class"
    participant_email = "john@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={participant_email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {participant_email} from {activity_name}"}

    activity_response = client.get("/activities")
    assert participant_email not in activity_response.json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_error(client):
    # Arrange
    activity_name = "Science Club"
    missing_email = "ghost@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={missing_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found for this activity"


def test_unregister_from_nonexistent_activity_returns_error(client):
    # Arrange
    activity_name = "Nonexistent Club"
    participant_email = "teststudent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={participant_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
