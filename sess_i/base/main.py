"""
Session-State interface module

Create class containing the whole sess_i interface. The class contains two subclasses:
    * Object space: contains the logic for handling tool calculation layer and communication with the widget spaces
    * Widget space(s): contains the logic for handling data persistency throughout page switching in the GUI
The main class when initialized will automatically generate an object space. Widget spaces will be generated with a
specific command. This is because while there is only one object space, there can be multiple widget spaces (one for
each page).
"""

import typing

import streamlit as st
from pydantic import BaseModel


# Object Space
class ObjectSpace:
    pass


# Widget Space
class WidgetSpace:
    """
    Every widget space must contain a two base parameters:
        * The id of the page it communicates with
        * A container with the widgets and their state metadata (key & value)
        * a classmethod to check session state and get the data

    """

    def __init__(self, page, session_state):

        self.page = page
        self.session_state = session_state
        self.widgets = {}

        for key, value in session_state.items():
            if str(self.page) in key:
                self.widgets.update({key: value})

    @classmethod
    def initialize_session(cls, page, session_state):
        if "Global_Widget_Space" not in session_state.keys():
            space = WidgetSpace(page, session_state)
            session_state["Global_Widget_Space"] = {page: space}
            return st.session_state["Global_Widget_Space"][page]
        else:
            if page not in session_state["Global_Widget_Space"]:
                session_state["Global_Widget_Space"].update({page: WidgetSpace(page, session_state)})
            return st.session_state["Global_Widget_Space"][page]

    def check_session(self):
        if not self.session_state["Global_Widget_Space"][self.page]:
            raise KeyError(
                f"Widget space for page '{self.page}' not initialized"
            )
        for key, value in self.session_state.items():
            if str(self.page) in key:
                self.widgets.update({key: value})

class ObjectSpace:

    def __init__(self, page, session_state):

        self.page = page
        self.session_state = session_state
        self._objects = {}

    @property
    def add_object(self, object):
        pass

# # Main interface for communicating with object and widget spaces
# class SessI(BaseModel):
#
#     def __int__(self, session_state):
#
#         self.session_state = session_state
#         if "Global_Widget_Space" in session_state.keys():
#             for key in session_state["Global_Widget_Space"]:
#                 # self.widget_spaces
#                 pass


if __name__ == "__main__":
    pass
