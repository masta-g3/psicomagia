from st_click_detector import click_detector
import streamlit as st
import requests
import json
import os


if "queried" not in st.session_state:
    st.session_state.queried = False
if "reflexion" not in st.session_state:
    st.session_state.reflexion = ""
if "terapia" not in st.session_state:
    st.session_state.terapia = ""

with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

url = "https://api.fireworks.ai/inference/v1/completions"
fireworks_api_key = os.getenv("FIREWORKS_API_KEY")
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {fireworks_api_key}",
}

payload = {
    "model": "accounts/manolorueda-b7535c/models/psicomagia",
    "max_tokens": 4000,
    "top_p": 1,
    "top_k": 40,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "temperature": 0.8,
    "prompt": "",
}

prompt_template = """"[INST]Eres un asesor metafísico y creador de la Psicomagia. Reflexiona sobre el registro del paciente y asiste con una terapia psicomágica. Utiliza el formato XML especializado de [REFLEXION][TERAPIA] en tu respuesta. 
[REGISTRO] {registro} [/REGISTRO][/INST]"
"""


def parse_response(response):
    """Extract from tags."""
    response = response.json()["choices"][0]["text"]
    response = response.replace("\n", " ")
    reflexion_txt = response.split("[REFLEXION]")[1]
    reflexion_txt = reflexion_txt.split("[/REFLEXION]")[0]

    terapia_txt = response.split("[TERAPIA]")[1]
    terapia_txt = terapia_txt.split("[/TERAPIA]")[0]

    return reflexion_txt, terapia_txt


def main():
    st.image("terapia-psicomagica.gif")
    if not st.session_state.queried:
        registro = st.text_area("Entrada", label_visibility="collapsed", help="En qué te puedo ayudar?")
        image_html = '<a href="#" id="Image 1"><img src="https://github.com/masta-g3/assets/blob/main/ask.png?raw=true" alt="Qué te acongoja?"></a>'
        clicked = click_detector(image_html)

        if clicked and len(registro) > 0:
            with st.spinner("Consultando al psicomago..."):
                prompt = prompt_template.replace("{registro}", registro)
                payload["prompt"] = prompt
                response = requests.request(
                    "POST", url, headers=headers, data=json.dumps(payload)
                )
                reflexion, terapia = parse_response(response)
                st.session_state.reflexion = reflexion
                st.session_state.terapia = terapia
                st.session_state.queried = True
                st.rerun()

    if st.session_state.queried:
        st.markdown(st.session_state.reflexion)
        st.markdown("⊹˚₊•┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈୨୧┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈•‧₊˚⊹")
        st.markdown(st.session_state.terapia)


if __name__ == "__main__":
    main()
