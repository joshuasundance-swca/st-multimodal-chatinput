import streamlit as st

from st_multimodal_chatinput import multimodal_chatinput


class History:
    def __init__(self):
        self.input_history = []

    def add_human_message(self, human_message):
        self.input_history.append({"type": "human", "data": human_message})

    def add_ai_message(self, ai_message):
        self.input_history.append({"type": "ai", "data": ai_message})

    def reset(self):
        self.input_history = []

    def render(self):
        for inp in self.input_history:
            with st.chat_message(inp["type"]):
                if inp["data"]["textInput"]:
                    st.text(inp["data"]["textInput"])
                for img in inp["data"].get("uploadedImages", []):
                    st.image(img)

    def handle_mm_inp(self, mm_inp):
        if mm_inp and any(mm_inp.values()):
            self.add_human_message(mm_inp)
            self.add_ai_message({"textInput": "ACK"})

    def await_mm_inp(self, *args, **kwargs):
        self.handle_mm_inp(multimodal_chatinput(*args, **kwargs))


if "input_history" not in st.session_state:
    st.session_state.input_history = History()

with st.sidebar:
    text_color = st.selectbox("Text Color", ["black", "white", "blue", "green", "purple"])
    reset_button = st.button("Reset", on_click=st.session_state.input_history.reset)

with st.container():
    st.session_state.input_history.render()

with st.container():
    st.session_state.input_history.await_mm_inp(text_color=text_color)
