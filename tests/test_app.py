def test_root_redirects(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"


def test_signup_for_activity(client):
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    get_response = client.get("/activities")
    assert email in get_response.json()["Chess Club"]["participants"]


def test_signup_existing_student_returns_400(client):
    email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_missing_activity_returns_404(client):
    response = client.post("/activities/Nonexistent Activity/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant(client):
    email = "daniel@mergington.edu"
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}

    get_response = client.get("/activities")
    assert email not in get_response.json()["Chess Club"]["participants"]


def test_remove_missing_participant_returns_404(client):
    response = client.delete("/activities/Chess Club/participants", params={"email": "nobody@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_activity_not_found_returns_404(client):
    response = client.delete("/activities/Nonexistent Activity/participants", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
