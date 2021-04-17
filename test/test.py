def test_redirection(app,client):
    print(client)
    # checking redirection
    response = client.get("/")
    assert response.status_code == 200