import streamlit as st
import regex as re
from datetime import datetime as dt
import pandas as pd
import html
import json

file_path = "diary_file.txt"

with open("translations.json", "r") as f:
    translations = json.load(f)

form_map = {
    "mood": {
        "😀": 5, "🙂": 4, "😐": 3, "😕": 2, "☹️": 1, None: 0
        },
    "phisical": {
        "💪": 4, "👍": 3, "👎": 2, "🖕": 1, None: 0
        },   
    "pride": {
        ":rainbow[Yes]": "Yes", "So so": "So so", "No": "No", None: None
        },
    "relations": {
        "💕": 4, "🤍": 3, "❤️‍🩹": 2, "💔": 1, None: 0
        }

}

def load_notes(n = 0):
    with open(file_path, 'r') as file:
        lines = file.read()

    matches = list(re.finditer(r'(\d{2}\.\d{2}\.\d{4})r\.', lines))
    notes = []
    for i in range(len(matches) - n):
        start = matches[i].end()
        end = matches[i+1].start() if i+1 < len(matches) else len(lines)
        date = matches[i].group(1)
        content = lines[start:end].strip()
        notes.append({
            "date": date,
            "content": content,
            "date_formated": dt.strptime(date, "%d.%m.%Y").date()
        })
    df = pd.DataFrame(notes).sort_values(by='date_formated', ascending=False)
    return df

def save_note_and_clear():
    today_str = dt.today().strftime('%d.%m.%Yr.')
    if "edit" in st.session_state and st.session_state["edit"] == True:
        note_text = st.session_state.edited_input.strip()
        # Wczytaj całą zawartość pliku
        with open(file_path, 'r') as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            if line.strip() == today_str:
                break
            new_lines.append(line)

        # Dodaj nową notatkę na koniec
        new_lines.append(f"{today_str}\n{note_text}\n\n")

        # Zapisz zmodyfikowany plik
        with open(file_path, 'w') as file:
            file.writelines(new_lines)

        st.success(translations["success_edit_msg"][lang])
        st.session_state["edit"] = False
                
    else:
        note_text = st.session_state.note_input.strip()
        if note_text != "":
            
            with open(file_path, 'a') as file:
                file.write(f"{today_str}\n{note_text}\n\n")
            st.session_state.note_input = "" 
            st.success(translations["success_edit_msg"][lang])
        else:
            st.warning("Cannot save an empty note.")

with st.sidebar:
    on = st.selectbox(
        " ",
        ("Polski", "English"),
    )
    if on == "Polski":
        lang = "pl"
    else:
        lang = "en" 
    with st.expander(translations["form_title"][lang]):
        with st.form("my_form", border = False):
            mood = st.pills(translations["form_mood"][lang], ["😀", "🙂", "😐", "😕", "☹️"] , selection_mode="single")

            phisical = st.pills(translations["form_phisical"][lang], ["💪", "👍", "👎", "🖕"] , selection_mode="single")
            
            pride = st.pills(translations["form_pride"][lang], [":rainbow[Yes]", "So so", "No"] , selection_mode="single")

            exercises =  st.pills(translations["form_exercises"][lang], ["Spacer 🚶🏼‍♀️", "Pływanie 🏊🏼‍♀️", "Inne ⛹🏼‍♀️", "Nic ❌"] , selection_mode="multi")
            
            slow = st.pills(translations["form_slow"][lang], ["Tak", "Nie"] , selection_mode="single")
            
            relations = st.pills(translations["form_relations"][lang], ["💕", "🤍", "❤️‍🩹", "💔"] , selection_mode="single")

            st.form_submit_button()

            stats_df = pd.DataFrame({
                "mood": form_map["mood"][mood],
                "phisical": form_map["phisical"][phisical],
                "pride": form_map["pride"][pride],
                "exercises": exercises,
                "slow": slow,
                "relations": form_map["relations"][relations],
                "date": dt.today().strftime('%d-%m-%Y')
            })
            st.write(stats_df)
            stats_df.to_csv('stats.csv', mode='a', index=False, header=False)

    st.write(translations['exercise_title'][lang])
    squats_df = pd.DataFrame({translations['exercise_exercise'][lang]: [translations['exercise_squats'][lang],
                                                                        translations['exercise_sit-ups'][lang],
                                                                        translations['exercise_push-ups'][lang]],
                                translations['exercise_count'][lang]: [0,0,0]})
    squats = st.data_editor(squats_df)


st.markdown(
    """
    <style>
    textarea {
        font-family: "Courier New", monospace !important;
        font-size: 14px !important;
        color: #333333 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.set_page_config(page_title=translations["page_title"][lang], layout="centered", page_icon="☀️")

st.title(translations["title"][lang])
st.header(translations["subtitle"][lang])

df = load_notes()
if not df.empty:
    today_note = df[
        df['date_formated'] == dt.today().date()
    ].reset_index(drop = True)
else:
    today_note = pd.DataFrame

st.text_area(
    translations["note_label"][lang],
    key="note_input",
    placeholder = translations["placeholder"][lang] if not today_note.empty else " ",
    on_change=save_note_and_clear,
    height= "content",
    disabled= True if not today_note.empty else False
)

today = dt.today().date()
today_df = df[
    (df['date_formated'].apply(lambda d: d.month) == today.month) &
    (df['date_formated'].apply(lambda d: d.day) == today.day)
].reset_index(drop = True)



for index, row in today_df.iterrows():
    if index == 0:
        with st.expander(str(row['date']), expanded=True):

            safe_text = html.escape(row['content'])  # escape HTML chars
            st.markdown(
                f"""
                <div style="
                    font-family: 'Courier New', monospace;
                    font-size: 14px;
                    color: #222;
                    white-space: pre-wrap;    /* preserve newlines */
                    line-height: 1.4;
                ">{safe_text}</div>
                """,
                unsafe_allow_html=True
            )
            col1, col2 , col3 = st.columns([2,2,1])

            with col3:
                if st.button(translations["edit"][lang]):
                    if "edit" not in st.session_state:
                        st.session_state["edit"] = True
            if "edit" in st.session_state:
                if st.session_state["edit"] == True:
                    st.text_area(
                        label = "",
                        value= safe_text,
                        key="edited_input",
                        on_change=save_note_and_clear,  
                        height= "content"
                    )
    else:
        with st.expander(str(row['date']), expanded=True):
            safe_text = html.escape(row['content'])  # escape HTML chars
            st.markdown(
                f"""
                <div style="
                    font-family: 'Courier New', monospace;
                    font-size: 14px;
                    color: #222;
                    white-space: pre-wrap;    /* preserve newlines */
                    line-height: 1.4;
                ">{safe_text}</div>
                """,
                unsafe_allow_html=True
            )
            
stats = pd.read_csv("stats.py")

