# Tests

def test_listing_all_equipment(client):
    response=client.get("/rentals")
    
