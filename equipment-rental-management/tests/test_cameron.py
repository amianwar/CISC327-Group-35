# Tests

def test_listing_all_renters(client):
    '''
    Checks that all renters can be listed.
    '''
    response = client.get("/renters")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_add_and_get_one_renter(client):
    '''
    Checks that renter that is POSTed to /renters can be retrieved with GET.
    '''
    
    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }

    create_renter = client.post("/renters", json=payload)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]

    item = client.get(f"/renters/{renter_id}")
    assert item.status_code == 200
    data = item.get_json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane.doe@example.com"