# Tests

from datetime import date, timedelta


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
    
    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }

    create_renter = client.post("/renters", json=payload)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]

    payload_2 = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 2,
        "available_units": 2
    }

    create_equipment = client.post("/equipment", json=payload_2)
    assert create_equipment.status_code == 201
    equipment_id = create_equipment.get_json()["id"]

    payload_3 = {
        "renter_id": renter_id,
        "equipment_id": equipment_id,
        "rental_date": date.today().isoformat(),
        "return_date": None,
        "due_date": (date.today() + timedelta(days=3)).isoformat()
    }
    
    create_rental = client.post("/rentals", json=payload_3)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]

    response = client.get(f"/rentals?renter_id={renter_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_look_up_rentals_for_renter_with_no_rentals(client):
    '''
    Checks that a renter with no rentals gets an empty list.
    '''

    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }

    create_renter = client.post("/renters", json=payload)
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

def test_extend_rental_by_one_day(client):
    '''
    Checks that a rental can be extended by 1 day.
    '''

    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }
    payload_2 = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 1,
        "available_units": 1
    }

    create_renter = client.post("/renters", json=payload)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]

    create_equipment = client.post("/equipment", json=payload_2)
    assert create_equipment.status_code == 201
    equipment_id = create_equipment.get_json()["id"]

    payload_3 = {
        "renter_id": renter_id,
        "equipment_id": equipment_id,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=3)).isoformat()
    }
    create_rental = client.post("/rentals", json=payload_3)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]

    extend_rental = client.put(f"/rentals/{rental_id}/return", json={"extend_days": 1})
    assert extend_rental.status_code == 200
    assert extend_rental.get_json()["due_date"] == (date.today() + timedelta(days=4)).isoformat()

def test_extend_rental_by_over_two_days(client):
    '''
    Checks that a rental cannot be extended by 2+ days.
    '''

    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }
    payload_2 = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 1,
        "available_units": 1
    }

    create_renter = client.post("/renters", json=payload)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]

    create_equipment = client.post("/equipment", json=payload_2)
    assert create_equipment.status_code == 201
    equipment_id = create_equipment.get_json()["id"]

    payload_3 = {
        "renter_id": renter_id,
        "equipment_id": equipment_id,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=3)).isoformat()
    }
    create_rental = client.post("/rentals", json=payload_3)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]

    extend_rental = client.put(f"/rentals/{rental_id}/return", json={"extend_days": 3})
    assert extend_rental.status_code == 400


def test_extend_nonexistent_rental(client):
    '''
    Checks that extending a rental that does not exist returns 404.
    '''

    extend_rental = client.put("/rentals/999999/return", json={"extend_days": 1})
    assert extend_rental.status_code == 404

def test_extend_rental_blocked_by_another_booking(client):
    '''
    Checks that a rental cannot be extended into a period another customer has booked.
    '''

    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }
    payload_2 = {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    payload_equipment = {
        "name": "Mountain Bike",
        "category": "Bikes",
        "total_units": 1,
        "available_units": 1
    }

    create_renter = client.post("/renters", json=payload)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]

    create_second_renter = client.post("/renters", json=payload_2)
    assert create_second_renter.status_code == 201
    second_renter_id = create_second_renter.get_json()["id"]

    create_equipment = client.post("/equipment", json=payload_equipment)
    assert create_equipment.status_code == 201
    equipment_id = create_equipment.get_json()["id"]

    payload_rental = {
        "renter_id": renter_id,
        "equipment_id": equipment_id,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=3)).isoformat()
    }
    create_rental = client.post("/rentals", json=payload_rental)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]

    payload_rental_2 = {
        "renter_id": second_renter_id,
        "equipment_id": equipment_id,
        "rental_date": (date.today() + timedelta(days=4)).isoformat(),
        "due_date": (date.today() + timedelta(days=7)).isoformat()
    }
    create_second_rental = client.post("/rentals", json=payload_rental_2)
    assert create_second_rental.status_code == 201

    extend_rental = client.put(f"/rentals/{rental_id}/return", json={"extend_days": 2})
    assert extend_rental.status_code == 409