# Tests

def test_listing_all_renters(client):
    '''
    Checks that all renters can be listed.
    '''
    response = client.get("/renters")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_create_and_get_one_renter(client):
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

def test_create_two_renters_with_same_email(client):
    '''
    Checks that two renters cannot be created with the same email.
    '''
    
    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }
    payload2 = {
        "name": "John Doe",
        "email": "jane.doe@example.com"
    }
    create_renter = client.post("/renters", json=payload)
    assert create_renter.status_code == 201

    create_second_renter = client.post("/renters", json=payload2)
    assert create_second_renter.status_code == 400

def test_create_renter_with_invalid_email(client):
    '''
    Checks that renter cannot be created with an invalid email.
    '''
    
    payload = {
        "name": "Jane Doe",
        "email": "invalid-email"
    }
    create_renter = client.post("/renters", json=payload)
    assert create_renter.status_code == 400

def test_create_and_update_renter(client):
    '''
    Checks that renter that is POSTed to /renters can be updated with PUT.
    '''
    
    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }
    update_payload = {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }

    create_renter = client.post("/renters", json=payload)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]
    
    update_renter = client.put(f"/renters/{renter_id}", json=update_payload)
    assert update_renter.status_code == 200
    updated_data = update_renter.get_json()
    assert updated_data["name"] == "John Doe"
    assert updated_data["email"] == "john.doe@example.com"

def test_create_and_delete_renter(client):
    '''
    Checks that renter that is POSTed to /renters can be deleted with DELETE.
    '''
    
    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }
    create_renter = client.post("/renters", json=payload)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]
    delete_renter = client.delete(f"/renters/{renter_id}")
    assert delete_renter.status_code == 204

def test_listing_all_rentals(client):
    '''
    Checks that all rentals can be listed.
    '''
 
    response = client.get("/rentals")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)    

def test_look_up_rental_by_renter(client):
    '''
    Checks that a rental can be looked up by renter.
    '''
    
    renter_payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }

    create_renter = client.post("/renters", json=renter_payload)
    assert create_renter.status_code == 201

def test_look_up_rentals_for_renter_with_no_rentals(client):
    '''
    Checks that a renter with no rentals gets an empty list.
    '''

    renter_payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }

    create_renter = client.post("/renters", json=renter_payload)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]

    response = client.get(f"/rentals?renter_id={renter_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_look_up_rentals_for_nonexistent_renter(client):
    '''
    Checks that it is not possible to look up rentals for a 
    renter that does not exist.
    '''
 
    response = client.get("/rentals?renter_id=999999")
    assert response.status_code == 400
