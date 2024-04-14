from ..fixtures import app, client, agency
# from ...src.model.editors import Editor

# Please note that I made sure that each test function has an independant functinoality to make sure that all tests assess from scratch

def test_get_an_editors_information(client, agency):
    editor = client.post("/editor/", json={"editor_id": 1, "name": "Midani", "address": "Krems"})
    assert editor.status_code == 200
    parsed = editor.get_json()
    assert parsed["editor"]["editor_id"] == 1
    assert parsed["editor"]["name"] == "Midani"
    assert parsed["editor"]["address"] == "Krems"


def test_add_editor(client, agency):
    before = len(agency.editors)
    editor = client.post("/editor/", json={"editor_id": 1, "name": "Mids", "address": "Krems"})
    assert editor.status_code == 200
    assert len(agency.editors) == before + 1



def test_list_all_editors(client, agency):
    response = client.get("/editor/")   # <-- note the slash at the end!
    assert response.status_code == 200
    parsed = response.get_json()
    assert len(parsed["editor"]) == len(agency.editors)


def test_get_editor_info(client, agency ):
    before = len(agency.editors)
    response = client.post("/editor/", json={"editor_id": 1, "name": "Draymond Green", "address": "Hell"})
    assert response.status_code == 200
    response = client.get("/editor/")
    assert response.status_code == 200
    parsed = response.get_json()
    assert len(parsed["editor"]) == before + 1
    assert parsed["editor"][0]["name"] == "Draymond Green"
    assert parsed["editor"][0]["address"] == "Hell"


def test_update_editor_info(client, agency):
    editor=client.post("/editor/",json={"editor_id": 1, "name": "Mids", "address": "Krems"})
    assert editor.status_code == 200
    parsed = editor.get_json()
    editor2=client.post("/editor/",json={"editor_id": 1, "name": "Midani", "address": "Vienna"})
    parsed2=editor2.get_json()
    assert editor2.status_code == 200
    assert parsed["editor"]["name"] != parsed2["editor"]["name"]
    assert parsed["editor"]["address"] != parsed2["editor"]["address"]



def test_delete_editor(client, agency):
    before = len(agency.editors)
    editor1 = client.post("/editor/", json={"editor_id": 1, "name": "Mids", "address": "Krems"})
    assert editor1.status_code == 200
    assert len(agency.editors) == before + 1
    client.delete("/editor/1")
    assert len(agency.editors) == before




