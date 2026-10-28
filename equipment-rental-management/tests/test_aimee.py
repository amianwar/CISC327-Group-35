# Tests

def test_listing_all_equipment(client):
    response=client.get("/equipment")
    assert response.status_code == 200
    data = response.get_json()

def test_add_equipment_item_and_check_availability(client):
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