from app import store
from datetime import date, timedelta
import pytest

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_add_and_delete_equipment_in_window(client):
    '''
    Checks that equipment POSTed to /ui/equipment is stored and listed,
    and can be deleted from /ui/equipment/<id>/delete.
    '''

    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": "5",
    }

    create_item = client.post("/ui/equipment", data=payload)
    assert create_item.status_code == 302
    equipment_id = list(store.equipment.keys())[0]

    delete_equipment = client.post(f"/ui/equipment/{equipment_id}/delete")
    assert delete_equipment.status_code == 302

    response = client.get("/ui/equipment")
    assert response.status_code == 200

def test_add_and_delete_renter_in_window(client):
    '''
    Checks that a renter POSTed to /ui/renters is stored and listed,
    and can be deleted from /ui/renters/<id>/delete.
    '''

    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
    }

    create_renter = client.post("/ui/renters", data=payload)
    assert create_renter.status_code == 302

    renter_id = list(store.renters.keys())[0]
    delete_renter = client.post(f"/ui/renters/{renter_id}/delete")
    assert delete_renter.status_code == 302

    response = client.get("/ui/renters")
    assert response.status_code == 200

def test_add_and_return_rental_in_window(client):
    '''
    Checks that a rental POSTed to /ui/rentals is stored,
    and can be returned from /ui/rentals/<id>/return.
    '''

    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": "5",
    }

    client.post("/ui/equipment", data=payload)
    equipment_id = list(store.equipment.keys())[0]

    payload_2 = {
        "equipment_id": str(equipment_id),
        "renter_id": "1",
    }

    create_rental = client.post("/ui/rentals", data=payload_2)
    assert create_rental.status_code == 302
    rental_id = list(store.rentals.keys())[0]

    return_rental = client.post(f"/ui/rentals/{rental_id}/return")
    assert return_rental.status_code == 302

    response = client.get("/ui/rentals")
    assert response.status_code == 200

def test_return_rental(client):
    '''
    Checks that a rental POSTed to /rentals can be returned with PUT and that
    the unit is added back.
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
        "equipment_id": equipment_id,
        "renter_id": 1,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=7)).isoformat(),
    }

def test_extend_rental(client):
    '''
    Checks that a rental POSTed to /rentals can be extended with PUT.
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
        "equipment_id": equipment_id,
        "renter_id": 1,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=7)).isoformat(),
    }

    create_rental = client.post("/rentals", json=payload_2)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]
    original_due_date = store.rentals[rental_id].due_date

    extend_rental = client.put(f"/rentals/{rental_id}/extend", json={"days": 3})
    assert extend_rental.status_code == 200
    assert store.rentals[rental_id].due_date == original_due_date + timedelta(days=3)

def test_release_deposit_before_return(client):
    '''
    Checks that a deposit cannot be released before the equipment is returned.
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
        "equipment_id": equipment_id,
        "renter_id": 1,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=7)).isoformat(),
    }

    create_rental = client.post("/rentals", json=payload_2)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]

    release = client.put(f"/rentals/{rental_id}/deposit/release")
    assert release.status_code == 400

def test_release_deposit_after_return(client):
    '''
    Checks that the deposit of a returned rental can be released.
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
        "equipment_id": equipment_id,
        "renter_id": 1,
        "rental_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=7)).isoformat(),
    }

    create_rental = client.post("/rentals", json=payload_2)
    assert create_rental.status_code == 201
    rental_id = create_rental.get_json()["id"]

    client.put(f"/rentals/{rental_id}/return")

    release = client.put(f"/rentals/{rental_id}/deposit/release")
    assert release.status_code == 200