def test_redirection(app,client):
    # checking redirection
    response = client.get("/")
    assert response.status_code == 200