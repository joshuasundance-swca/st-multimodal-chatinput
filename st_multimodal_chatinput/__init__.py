import os

import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "st_multimodal_chatinput",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_multimodal_chatinput", path=build_dir)

def multimodal_chatinput(default=None, disabled=False, key=None, placeholder="Ask me anything..", text_color="white") -> dict[str, str] | None:
    """
    Create and return a new instance of the "multimodal_chatinput" component.

    This function initializes and renders a multimodal chat input component, which includes
    functionalities for handling text input, image uploads, and document uploads (PDF, DOCX, XLSX).
    The component's interactivity can be enabled or disabled. The function returns a dictionary
    containing the current state of the chat input, specifically the text input and any uploaded files.

    Parameters
    ----------
    default : Any
        Output of the chat input when it is first initialized.
    disabled : bool
        A flag to determine whether the chat input component should be disabled. If True, the component is non-interactive.
    key : str, optional
        An optional key that can be used to identify this component in Streamlit callbacks.
    placeholder : str, optional
        The placeholder text to display in the chat input when it is empty.
    text_color : str, optional
        The color of the text in the chat input.

    Returns
    -------
    dict
        A dictionary with the following structure:
        {
            'uploadedFiles': list of dictionaries containing file information,
            'uploadedImages': list of base64 encoding of uploaded images (for backward compatibility),
            'textInput': str
        }
        Each file dictionary in 'uploadedFiles' has the following structure:
        {
            'name': str (filename),
            'type': str (MIME type),
            'content': str (base64 encoded file content)
        }
        'uploadedImages' contains only the base64 encoded content of image files.
        'textInput' is a string representing the current text input.

    If no files are uploaded and the text input is empty, the function returns None.
    """
    component_value = _component_func(
        default=default,
        disabled=disabled,
        key=key,
        placeholder=placeholder,
        text_color=text_color,
    )

    if isinstance(component_value, dict):
        # Ensure backward compatibility for uploadedImages
        if 'uploadedFiles' in component_value.keys():
            component_value['uploadedImages'] = [
                file['content'] for file in component_value['uploadedFiles']
                if file['type'].startswith('image/')
            ]
        if any(component_value.values()):
            return component_value

    return None
