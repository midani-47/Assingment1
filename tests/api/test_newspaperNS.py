# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency
# from ...src.model.newspaper import Newspaper
from ...src.model.editors import Editor



# Please note that I made sure that each test function has an independant functinoality to make sure that all tests assess from scratch


def test_get_newspaper_should_list_all_papers(client, agency):
    # send request
    response = client.get("/newspaper/")   # <-- note the slash at the end!
    # test status code
    assert response.status_code == 200
    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)


def test_add_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)
    response = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200
    # verify

    assert len(agency.newspapers) == paper_count_before + 1
    # parse response and check that the correct data is here
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.14


def test_get_newspaper_by_id(client, agency):
    p=client.post("/newspaper/",
                           json={"name": "Simpsons Comic", "frequency": 7, "price": 3.14})
    assert p.status_code == 200
    parse = p.get_json()
    paper_id= parse["newspaper"]["paper_id"]
    d = client.get(f"/newspaper/{paper_id}")
    z=d.get_json()
    assert z["newspaper"]["name"] == "Simpsons Comic"
    assert z["newspaper"]["frequency"] == 7
    assert z["newspaper"]["price"] == 3.14




def test_update_newspaper(client, agency):
    response = client.post("/newspaper/",
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 13.14
                           })
    assert response.status_code == 200
    parsed = response.get_json()
    paper_id = parsed["newspaper"]["paper_id"]
    updated_paper = {
        "name": "Simpsons Comic",
        "frequency": 5,
        "price": 11.14
    }
    response = client.post(f"/newspaper/{paper_id}", json=updated_paper)
    assert response.status_code == 200
    response = client.get(f"/newspaper/{paper_id}")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed["newspaper"]["name"] == "Simpsons Comic"
    assert parsed["newspaper"]["frequency"] == 5
    assert parsed["newspaper"]["price"] == 11.14




def test_get_all_newspapers(client, agency):
    paper_count_before = len(agency.newspapers)
    response = client.get("/newspaper/")
    assert response.status_code == 200
    assert len(agency.newspapers) == paper_count_before
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)
    assert len(parsed["newspapers"]) == paper_count_before


def test_add_issue(client, agency):
    newspaper_response = client.post("/newspaper/",
                                     json={"name": "Simpsons Comic", "frequency": 7, "price": 3.14})
    parse=newspaper_response.get_json()
    paper_id = parse["newspaper"]["paper_id"]
    assert paper_id > 0
    new_issue = {
        "page_number": 1,
        "released": True,
        "releasedate": "2020-01-01",
        "subscribers": [0]
    }
    new_issue2= {
        "page_number": 1,
        "released": True,
        "releasedate": "2020-01-01",
        "subscribers": [0]
    }
    agency.add_issue( new_issue)
    agency.add_issue( new_issue2)
    assert len(agency.issues) == 2


def test_deliver_issue(client, agency):
    response=client.post("/newspaper/",json={"name": "Simpsons Comic", "frequency": 7, "price": 3.14})
    assert response.status_code == 200
    parse=response.get_json()
    paper_id = parse["newspaper"]["paper_id"]
    assert paper_id > 0
    new_issue = client.post(f"/newspaper/{paper_id}/issue",json={"page_number": 1, "released": True, "releasedate": "2020-01-01", "subscribers": [0]})
    assert new_issue.status_code == 200
    parse=new_issue.get_json()
    assert parse["issue"]["page_number"] == 1
    assert parse["issue"]["released"] == True
    assert parse["issue"]["releasedate"] == "2020-01-01"
    assert len(parse["issue"]["subscribers"]) == 0



def test_get_information_about_issue(client, agency):
    response=client.post("/newspaper/",json={"name": "Simpsons Comic", "frequency": 7, "price": 3.14})
    assert response.status_code == 200
    parse=response.get_json()
    paper_id = parse["newspaper"]["paper_id"]
    assert paper_id > 0
    new_issue = client.post(f"/newspaper/{paper_id}/issue",json={"page_number": 1, "released": True, "releasedate": "2020-01-01", "subscribers": [0]})
    assert new_issue.status_code == 200
    parse=new_issue.get_json()
    assert parse["issue"]["page_number"] == 1
    assert parse["issue"]["released"] == True
    assert parse["issue"]["releasedate"] == "2020-01-01"
    assert len(parse["issue"]["subscribers"]) == 0



def test_specify_editor(client, agency):
    response=client.post("/newspaper/",json={"name": "Simpsons Comic", "frequency": 7, "price": 3.14})
    assert response.status_code == 200
    parse=response.get_json()
    paper_id = parse["newspaper"]["paper_id"]
    assert paper_id > 0
    new_issue = client.post(f"/newspaper/{paper_id}/issue",json={"page_number": 1, "released": True, "releasedate": "2020-01-01", "subscribers": [0]})
    assert new_issue.status_code == 200
    editor = client.post("/editor/", json={"editor_id": 1, "name": "Midani", "address": "Krems"})
    assert editor.status_code == 200
    parsed = editor.get_json()
    assert parsed["editor"]["editor_id"] == 1
    assert len(agency.issues) == 1
    # issue.set_editor(issue_ns.payload['editor_id'])
    testo=agency.issues[0].set_editor(1)
    assert len(agency.issues) == 1
    assert agency.issues[0].editor_id == 1



