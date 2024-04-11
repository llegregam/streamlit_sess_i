import pytest

# Import the classes from the module
from sess_i.base.main import SessI, ObjectSpace, WidgetSpace

def test_object_space_initialization():
    session_state = {}
    object_space = ObjectSpace(session_state)
    assert object_space.session_state == session_state
    assert object_space.objects == {}

def test_object_space_set_item():
    session_state = {}
    object_space = ObjectSpace(session_state)
    object_space["test"] = "value"
    assert object_space.objects["test"] == "value"
    assert session_state["Object_Space"]["test"] == "value"

def test_widget_space_initialization():
    session_state = {}
    widget_space = WidgetSpace(session_state, "page1")
    assert widget_space.session_state == session_state
    assert widget_space.page == "page1"
    assert widget_space.widgets == {}

def test_widget_space_set_widget_defaults():
    session_state = {}
    widget_space = WidgetSpace(session_state, "page1")
    widget_space.set_widget_defaults(test="value")
    assert widget_space.widgets["test"] == "value"

def test_sess_i_initialization():
    session_state = {}
    sess_i = SessI(session_state, "page1")
    assert sess_i.session_state == session_state
    assert sess_i.page == "page1"
    assert isinstance(sess_i.object_space, ObjectSpace)
    assert isinstance(sess_i.widget_space, WidgetSpace)

def test_sess_i_register_object():
    session_state = {}
    sess_i = SessI(session_state, "page1")
    sess_i.register_object("value", "test")
    assert sess_i.object_space["test"] == "value"

def test_sess_i_register_widgets():
    session_state = {}
    sess_i = SessI(session_state, "page1")
    sess_i.register_widgets(test="value")
    assert sess_i.widget_space.widgets["test"] == "value"

def test_widget_space_initialize_session():
    session_state = {}
    widget_space = WidgetSpace.initialize_session(session_state, "page1")
    assert isinstance(widget_space, WidgetSpace)
    assert widget_space.page == "page1"
    assert widget_space.session_state == session_state

def test_widget_space_initialize_session_global_space():
    session_state = {"Global_Widget_Space": {"page1": WidgetSpace({}, "page1")}}
    widget_space = WidgetSpace.initialize_session(session_state, "page1")
    assert isinstance(widget_space, WidgetSpace)
    assert widget_space.page == "page1"
    assert widget_space.session_state == session_state

def test_widget_space_initialize_session_no_page():
    session_state = {}
    widget_space = WidgetSpace.initialize_session(session_state)
    assert isinstance(widget_space, WidgetSpace)
    assert widget_space.page.endswith("main")
    assert widget_space.session_state == session_state

def test_widget_space_register_widgets_no_page():
    session_state = {"Global_Widget_Space": {}}
    widget_space = WidgetSpace(session_state, "page1")
    with pytest.raises(KeyError):
        widget_space.register_widgets(test="value")