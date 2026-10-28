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

