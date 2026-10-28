# Tests

def test_listing_all_equipment(client):
    response=client.get("/equipment")
    assert response.status_code == 200
    data = response.get_json();

'''def test_add_equipment_item(client):
    payload = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": "5",
    }

    create_item = client.post("/equipment", json=payload)
    assert '''