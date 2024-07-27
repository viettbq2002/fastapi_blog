def test_create_user(client):
    data = {"email":"testuser@nofoobar.com","password":"tingggggtes"}
    response = client.post("/auth/register",json=data)
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True