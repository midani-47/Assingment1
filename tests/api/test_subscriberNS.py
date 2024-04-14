from ..fixtures import app, client, agency
# from ...src.model.subscribers import Subscriber

# Please note that I made sure that each test function has an independant functinoality to make sure that all tests assess from scratch


def test_create_subscribers(client, agency):
    before = len(agency.subscribers)
    response = client.post("/subscriber/",json={"subscriber_id": 1, "name": "Mids", "address": "Krems", "list_of_issues": [0], "list_of_newspapers": [0], "delivered_issues": [0], "special_issues": [0]})
    assert response.status_code == 200
    assert len(agency.subscribers) == before + 1


def test_get_subscriber_by_id(client, agency):
    new_subscriber = client.post("/subscriber/",json={"subscriber_id": 1, "name": "Mids", "address": "Krems", "list_of_issues": [0], "list_of_newspapers": [0], "delivered_issues": [0], "special_issues": [0]})
    assert new_subscriber.status_code == 200
    parsed = new_subscriber.get_json()
    assert parsed["subscriber"]["subscriber_id"] == 1
    assert parsed["subscriber"]["name"] == "Mids"
    assert parsed["subscriber"]["address"] == "Krems"
    assert parsed["subscriber"]["list_of_issues"] == None
    assert parsed["subscriber"]["list_of_newspapers"] == []
    assert parsed["subscriber"]["delivered_issues"] == []
    assert parsed["subscriber"]["special_issues"] == []


def test_remove_subscriber(client, agency):
    before = len(agency.subscribers)
    new_subscriber = client.post("/subscriber/",json={"subscriber_id": 1, "name": "Mids", "address": "Krems", "list_of_issues": [0], "list_of_newspapers": [0], "delivered_issues": [0], "special_issues": [0]})
    assert new_subscriber.status_code == 200
    assert len(agency.subscribers) == before + 1
    new_subscriber = client.delete("/subscriber/1")
    assert new_subscriber.status_code == 200
    assert len(agency.subscribers) == before



def test_update_subscriber_by_id(client, agency):
    subscriber=client.post("/subscriber/",json={"subscriber_id": 1, "name": "Mids", "address": "Krems", "list_of_issues": [0], "list_of_newspapers": [0], "delivered_issues": [0], "special_issues": [0]})
    assert subscriber.status_code == 200
    parsed = subscriber.get_json()
    assert parsed["subscriber"]["subscriber_id"] == 1
    subscriber2=client.post("/subscriber/",json={"subscriber_id": 1, "name": "Midani", "address": "Vienna", "list_of_issues": [0], "list_of_newspapers": [0], "delivered_issues": [0], "special_issues": [0]})
    assert subscriber2.status_code == 200
    parsed2 = subscriber2.get_json()
    assert parsed2["subscriber"]["name"] != parsed["subscriber"]["name"]
    assert parsed2["subscriber"]["address"] != parsed["subscriber"]["address"]
    assert parsed2["subscriber"]["list_of_newspapers"] == parsed["subscriber"]["list_of_newspapers"]
    assert parsed2["subscriber"]["list_of_issues"] == parsed["subscriber"]["list_of_issues"]
    assert parsed2["subscriber"]["delivered_issues"] == parsed["subscriber"]["delivered_issues"]
    assert parsed2["subscriber"]["special_issues"] == parsed["subscriber"]["special_issues"]



def subscribe_to_newspaper(client, agency):
    before = len(agency.newspapers.subscribers)
    subscriber=client.post("/subscriber/",json={"subscriber_id": 1, "name": "Mids", "address": "Krems", "list_of_issues": [0], "list_of_newspapers": [0], "delivered_issues": [0], "special_issues": [0]})
    assert subscriber.status_code == 201
    newspaper = client.post("/newspaper/",
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert newspaper.status_code == 201
    parsed = newspaper.get_json()
    paper_id = parsed["newspaper"]["paper_id"]
    response = client.post(f"/newspaper/{paper_id}/subscribe/1")
    assert response.status_code == 201
    parsed = response.get_json()
    assert parsed["newspaper"]["name"] == "Simpsons Comic"
    assert len(agency.newspapers.subscribers) == before + 1
    assert len(agency.subscribers) == before + 1
    assert len(agency.subscribers[0].list_of_newspapers) == 1


def test_missing_id(client, agency):
    response = client.post("/newspaper/", json={"name": "Simpsons Comic", "frequency": 7, "price": 3.14})
    assert response.status_code == 200
    parsed = response.get_json()
    paper_id = parsed["newspaper"]["paper_id"]
    response = client.post(f"/newspaper/{paper_id}/subscribe/")
    assert response.status_code == 404

