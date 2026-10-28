# Tests
from datetime import date, timedelta

def test_listing_all_equipment(client):
    response=client.get("/equipment")
    assert response.status_code == 200
    data = response.get_json()

def test_add_equipment_item_and_check_availability(client):
    '''
    Checks that equipment that is POSTed to /equipment can be deleted (from examples).
    '''
    
    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 5,
    }

    create_item = client.post("/equipment", json=payload)
    assert create_item.status_code == 201
    equipment_id = create_item.get_json()["id"]

    avail_item = client.get(f"/equipment/{equipment_id}/availability")
    assert avail_item.status_code == 200
    data = avail_item.get_json()
    assert data["available_units"] == 5
    assert data["is_available"] is True

def test_add_and_get_one_equipment_item(client):
    '''
    Checks that equipment that is POSTed to /equipment can be retrieved with GET.
    '''
    
    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 5,
    }
    
    create_item = client.post("/equipment", json=payload)
    assert create_item.status_code == 201
    equipment_id = create_item.get_json()["id"]

    item = client.get(f"/equipment/{equipment_id}")
    assert item.status_code == 200
    data = item.get_json()
    assert data["total_units"] == 5

def test_add_and_update_equipment_item(client):
    '''
    Checks that equipment that is POSTed to /equipment can be updated with PUT.
    '''
    
    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 5,
    }
        
    create_item = client.post("/equipment", json=payload)
    assert create_item.status_code == 201
    equipment_id = create_item.get_json()["id"]

    updated_payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 3,
    }
    update_item  = client.put(f"/equipment/{equipment_id}", json=updated_payload)
    assert update_item.status_code == 200
    updated_data = update_item.get_json()
    assert updated_data["total_units"] == 3


def test_add_and_delete_equipment_item(client):
    '''
    Checks that equipment that is POSTed to /equipment can be deleted with DELETE.
    '''
    
    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 5,
    }
            
    create_item = client.post("/equipment", json=payload)
    assert create_item.status_code == 201
    equipment_id = create_item.get_json()["id"]

    delete_item = client.delete(f"/equipment/{equipment_id}")
    assert delete_item.status_code == 204
    get_deleted_item = client.get(f"/equipment/{equipment_id}")
    assert get_deleted_item.status_code == 404

def test_add_two_items_delete_one(client):
    '''
    Checks that multiple equipment items can be POSTed to /equipment, and that
    one item can be deleted at a time.
    '''
    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 5,
    }

    payload_2 = {
        "name": "Canoe",
        "category": "Boats",
        "total_units": 3,
    }

    create_kayak = client.post("/equipment", json=payload)
    assert create_kayak.status_code == 201
    canoe_id = create_kayak.get_json()["id"]

    create_canoe = client.post("/equipment", json=payload_2)
    assert create_canoe.status_code == 201
    kayak_id = create_canoe.get_json()["id"]

    delete_kayak = client.delete(f"/equipment/{kayak_id}")
    assert delete_kayak.status_code == 204
    
    get_deleted_kayak = client.get(f"/equipment/{kayak_id}")
    assert get_deleted_kayak.status_code == 404
    get_canoe = client.get(f"/equipment/{canoe_id}")
    assert get_canoe.status_code == 200

def test_add_and_checkout(client):
    '''
    Checks that a renter and item can be POSTed to /renters and /equipment
    (respectively), and that a rental can be POSTed to /rentals.
    '''

    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 5,
    }
                
    create_item = client.post("/equipment", json=payload)
    assert create_item.status_code == 201
    equipment_id = create_item.get_json()["id"]

    payload_2 = {
        "name": "John Doe",
        "email": "johndoe@test.com",
        "membership_date": date.today(),
    }

    create_renter = client.post("/renters", json=payload_2)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]

    payload_3 = {
        "equipment_id": equipment_id,
        "renter_id": renter_id,
        "rental_date": date.today(),
        "due_date": date.today() + timedelta(days=7),
        "return_date": date.today() + timedelta(days=3),
        "deposit_amount": 0.0,
        "deposit_released": False,
    }

    create_rental = client.post("/rentals", json=payload_3)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]

    rental_data = create_rental.get_json()
    assert rental_data["equipment_id"] == equipment_id
    assert rental_data["renter_id"] == renter_id

def test_checkout_and_return(client):
    '''
    Checks that a rental can be checked out (POSTed to /rentals) and then
    returned (PUT to /rentals).
    '''
    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 5,
    }
    
    create_item = client.post("/equipment", json=payload)
    assert create_item.status_code == 201
    equipment_id = create_item.get_json()["id"]
    
    payload_2 = {
        "name": "John Doe",
        "email": "johndoe@test.com",
        "membership_date": date.today(),
    }
    
    create_renter = client.post("/renters", json=payload_2)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]
    
    payload_3 = {
        "equipment_id": equipment_id,
        "renter_id": renter_id,
        "rental_date": date.today(),
        "due_date": date.today() + timedelta(days=7),
        "return_date": date.today() + timedelta(days=3),
        "deposit_amount": 0.0,
        "deposit_released": False,
    }
    
    create_rental = client.post("/rentals", json=payload_3)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]

    return_rental = client.put(f"/rentals/{rental_id}/return")
    assert return_rental.status_code == 200
    