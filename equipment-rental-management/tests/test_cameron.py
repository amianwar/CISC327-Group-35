# Tests

def test_listing_all_renters(client):
    '''
    Checks that all renters can be listed.
    '''
    response = client.get("/renters")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

