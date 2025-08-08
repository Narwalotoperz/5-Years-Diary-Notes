import streamlit as st
import regex as re
from datetime import datetime as dt
import pandas as pd

def load_notes():
    with open('diary_file.txt', 'r') as file:
        lines = file.read()

    matches = list(re.finditer(r'(\d{2}\.\d{2}\.\d{4})r\.', lines))
    notes = []
    for i in range(len(matches)):
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
    note_text = st.session_state.note_input.strip()
    if note_text != "":
        today_str = dt.today().strftime('%d.%m.%Yr')
        with open('diary_file.txt', 'a') as file:
            file.write(f"{today_str}.\n{note_text}\n\n")
        st.session_state.note_input = "" 
        st.success("Note saved successfully!")
    else:
        st.warning("Cannot save an empty note.")

st.set_page_config(page_title="My First Streamlit App", layout="centered", page_icon="☀️")

st.title("Diary Notes")
st.header("How was your day?")

st.text_area(
    "Write a new note for today:",
    key="note_input",
    on_change=save_note_and_clear
)

df = load_notes()
today = dt.today().date()
today_df = df[
    (df['date_formated'].apply(lambda d: d.month) == today.month) &
    (df['date_formated'].apply(lambda d: d.day) == today.day)
]

for index, row in today_df.iterrows():
    with st.expander(row['date'], expanded=True):
        st.write(row['content'])
