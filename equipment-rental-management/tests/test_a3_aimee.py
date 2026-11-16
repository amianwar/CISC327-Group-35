from datetime import date, timedelta
from app.models.rental import Rental
import pytest

# Notification system test
def test_notification_system_feature(client):
    '''
    Checks out a rental to test if the notification system is working.
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
        "membership_date": date.today().isoformat(),
    }
    
    create_renter = client.post("/renters", json=payload_2)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]
    
    payload_3 = {
        "equipment_id": equipment_id,
        "renter_id": renter_id,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=7)).isoformat(),
        "deposit_amount": 0.0,
        "deposit_released": False,
    }
    
    create_rental = client.post("/rentals", json=payload_3)
    assert create_rental.status_code == 201

    client.__setattr__("app.rental.send_notification", lambda recipient, subject, message: False)

    assert create_rental.get_json()["status"] == "successful"
    assert create_rental.get_json()["rental_date"] == date.today().isoformat()


# Baseline tests:
def test_checkout_outofservice_equipment(client):
    '''
    Attempts to checkout an equipment item that is marked as unavailable.
    This test is meant to fail, revealing the intentional bug found 
    in set_equipment_status.
    '''
    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 5,
        "available_units": 5,
        "is_available": False
    }

    create_item = client.post("/equipment", json=payload)
    assert create_item.status_code == 201
    equipment_id = create_item.get_json()["id"]
    
    
    payload_2 = {
        "name": "John Doe",
        "email": "johndoe@test.com",
        "membership_date": date.today().isoformat(),
    }
    
    create_renter = client.post("/renters", json=payload_2)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]
    
    payload_3 = {
        "equipment_id": equipment_id,
        "renter_id": renter_id,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=7)).isoformat(),
        "return_date": (date.today() + timedelta(days=3)).isoformat(),
        "deposit_amount": 0.0,
        "deposit_released": False,
    }

    item_unavail = client.patch(f"/equipment/{equipment_id}/status", json={"is_available": False})
    assert item_unavail.status_code == 200

    create_rental = client.post("/rentals", json=payload_3)
    assert create_rental.status_code == 400

def test_list_rentals_store_id(client):
    '''
    Checking if rentals can be listed through the store_id route.
    '''
    response = client.get("/store_id")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_extend_rental_store_id(client):
    '''
    Checking if a rental's due date can be extended via the store_id route.
    '''
    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 5
    }
    
    create_item = client.post("/equipment", json=payload)
    assert create_item.status_code == 201
    equipment_id = create_item.get_json()["id"]
    
    payload_2 = {
        "name": "John Doe",
        "email": "johndoe@test.com",
        "membership_date": date.today().isoformat(),
    }
    
    create_renter = client.post("/renters", json=payload_2)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]
    
    payload_3 = {
        "equipment_id": equipment_id,
        "renter_id": renter_id,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=7)).isoformat(),
        "return_date": (date.today() + timedelta(days=3)).isoformat(),
        "deposit_amount": 0.0,
        "deposit_released": False,
    }
    
    create_rental = client.post("/rentals", json=payload_3)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]

    extend_rental = client.put(f"/store_id/{rental_id}/extend", json={"extend_days": 1})
    assert extend_rental.status_code == 200
    assert extend_rental.get_json()["due_date"] == (date.today() + timedelta(days=8)).isoformat()

def test_release_deposit_store_id(client):
    '''
    Checking that the damage deposit can be released for a returned rental.
    '''
    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 5
    }
    
    create_item = client.post("/equipment", json=payload)
    assert create_item.status_code == 201
    equipment_id = create_item.get_json()["id"]
    
    payload_2 = {
        "name": "John Doe",
        "email": "johndoe@test.com",
        "membership_date": date.today().isoformat(),
    }
    
    create_renter = client.post("/renters", json=payload_2)
    assert create_renter.status_code == 201
    renter_id = create_renter.get_json()["id"]
    
    payload_3 = {
        "equipment_id": equipment_id,
        "renter_id": renter_id,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=7)).isoformat(),
        "deposit_amount": 30.0,
        "deposit_released": False,
    }
    
    create_rental = client.post("/rentals", json=payload_3)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]

    return_rental = client.put(f"/store_id/{rental_id}/return", json={"return_date": (date.today()).isoformat()})
    assert return_rental.status_code == 200
    assert return_rental.get_json()["return_date"] == (date.today()).isoformat()

    release_dep = client.put(f"/store_id/{rental_id}/deposit/release")
    assert release_dep.status_code == 200


