import pytest
from ...src.model.newspaper import Newspaper
from ..fixtures import app, client, agency
from ...src.model.editors import Editor
from ...src.model.newspaper import Issue
from ...src.model.subscribers import Subscriber

# Please note that I made sure that each test function has an independant functinoality to make sure that all tests assess from scratch

def test_add_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Thje Times",
                          frequency=7,
                          price=999)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1
    assert new_paper in agency.all_newspapers()



def test_add_newspaper_same_id_should_raise_error(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    # first adding of newspaper should be okay
    agency.add_newspaper(new_paper)
    new_paper2 = Newspaper(paper_id=999,
                          name="Simpsons Comics",
                          frequency=7,
                          price=13.14)
    with pytest.raises(AssertionError, match='This id already exists'):  # <-- this allows us to test for exceptions
        # this one should rais ean exception!
        agency.add_newspaper(new_paper2)


def test_remove_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="The Guardian",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1
    agency.remove_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before

def test_add_editor(agency):
    before = len(agency.editors)
    new_editor = Editor(editor_id=1,
                        name="Abed",
                        address="Krems")
    agency.add_editor(new_editor)
    assert len(agency.all_editors()) == 1
    assert len(agency.all_editors()) == before + 1
    assert new_editor in agency.all_editors()


def test_get_newspaper(agency):
    new_paper = Newspaper(paper_id=123,
                          name="The Guardian",
                          frequency=7,
                          price=3)
    agency.add_newspaper(new_paper)
    assert agency.get_newspaper(123) == new_paper

def test_add_subscriber(agency):
    before = len(agency.subscribers)
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Abed",
                                address="Krems",
                                list_of_newspapers=[1],
                                list_of_issues=[1])
    agency.add_subscriber(new_subscriber)
    assert len(agency.all_subscribers()) == 1
    assert len(agency.all_subscribers()) == before + 1
    assert new_subscriber in agency.all_subscribers()


def test_all_newspapers(agency):
    assert len(agency.all_newspapers()) == len(agency.newspapers)

def test_all_editors(agency):
    new_editor = Editor(editor_id=1,
                        name="Abed",
                        address="Krems")
    agency.add_editor(new_editor)
    assert len(agency.all_editors()) == len(agency.editors)

def test_get_editor(agency):
    new_editor = Editor(editor_id=1,
                        name="Abed",
                        address="Krems")
    agency.add_editor(new_editor)
    assert agency.get_editor(1) == new_editor

def test_remove_editor(agency):
    new_editor = Editor(editor_id=1,
                        name="Abed",
                        address="Krems")
    agency.add_editor(new_editor)
    assert len(agency.all_editors()) == 1
    agency.remove_editor(new_editor)
    assert len(agency.all_editors()) == 0
    assert new_editor not in agency.all_editors()


def test_remove_issue(agency):
    new_editor = Editor(editor_id=1,
                        name="Abed",
                        address="Krems")
    agency.add_editor(new_editor)
    assert len(agency.all_editors()) == 1
    agency.remove_editor(new_editor)
    assert len(agency.all_editors()) == 0

def test_add_sub_same_id_raise_error(agency):
    before = len(agency.subscribers)
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Abed",
                                address="Krems",
                                list_of_newspapers=[1],
                                list_of_issues=[1])
    agency.add_subscriber(new_subscriber)
    assert len(agency.subscribers) == before +1
    new_subscriber2 = Subscriber(subscriber_id=1,
                                name="Abed",
                                address="Krems",
                                list_of_newspapers=[1],
                                list_of_issues=[1])
    with pytest.raises(AssertionError, match='This id already exists'):
        agency.add_subscriber(new_subscriber2)


def test_add_issue(agency):
    before = len(agency.issues)
    new_issue = Issue(issue_id=999,
                      page_number=1,
                      released=True,
                      releasedate="2020-01-01")
    agency.add_issue(new_issue)
    assert len(agency.issues) == before + 1

def test_get_issue(agency):
    new_issue = Issue(issue_id=999,
                      page_number=1,
                      released=True,
                      releasedate="2020-01-01")
    agency.add_issue(new_issue)
    assert agency.get_issue(999) == new_issue

