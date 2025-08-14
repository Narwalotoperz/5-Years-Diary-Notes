import streamlit as st
import regex as re
from datetime import datetime as dt
import pandas as pd
import html

file_path = "diary_file.txt"


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

        st.success("Note edited successfully!")
        st.session_state["edit"] = False
                
    else:
        note_text = st.session_state.note_input.strip()
        if note_text != "":
            
            with open(file_path, 'a') as file:
                file.write(f"{today_str}.\n{note_text}\n\n")
            st.session_state.note_input = "" 
            st.success("Note saved successfully!")
        else:
            st.warning("Cannot save an empty note.")

st.set_page_config(page_title="Note", layout="centered", page_icon="☀️")

st.title("Diary Note")
st.header("How was your day?")

st.text_area(
    "Wright something about your day:",
    key="note_input",
    on_change=save_note_and_clear,
    height= "content"
)

df = load_notes()
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
                if st.button("Edit"):
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
            
