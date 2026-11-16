from app import store

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_equipment_page_loads(client):
    response = client.get("/ui/equipment")
    assert response.status_code == 200

def test_renters_page_loads(client):
    response = client.get("/ui/renters")
    assert response.status_code == 200

def test_rentals_page_loads(client):
    response = client.get("/ui/rentals")
    assert response.status_code == 200
