import streamlit as st
from st_multimodal_chatinput import multimodal_chatinput

if "input_history" not in st.session_state:
    st.session_state.input_history = []

if "current_input" not in st.session_state:
    st.session_state.current_input = None

def reset():
    st.session_state.input_history = []
    st.session_state.current_input = None

top = st.container()
bottom = st.container()

with st.sidebar:
    text_color = st.selectbox("Text Color", ["black", "white", "blue", "green", "purple"])

with bottom:
    user_inp = multimodal_chatinput(text_color=text_color, key='zzz')

with top:
    history_without_current = [
        inp for inp in st.session_state.input_history if inp != st.session_state.current_input
    ]
    if history_without_current:
        st.markdown("# History")
        for inp in history_without_current:
            st.write(inp)

    if any(user_inp.values()):
        st.session_state.input_history.append(user_inp)
        st.session_state.current_input = user_inp
    else:
        if st.session_state.current_input:
            st.markdown("# Current")
            st.write(st.session_state.current_input)
            st.session_state.current_input = None

reset_button = st.button("Reset", on_click=reset)
