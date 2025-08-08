# 5-Years-Diary-Notes
This project is a simple Streamlit web app that allows you to maintain a personal diary and automatically parses your text notes into structured JSON data. It displays all notes from the same day (month and day match) in the last 5 years, if such notes exist.

The project aimed to create a digital version of paper notebooks, each page corresponding to a day of the year, but divided into several sections. This allows for the ability to record notes over several years, reflecting on how we felt and experienced on the same day in previous years. This method of note-taking is intended to provide perspective and reinforce the therapeutic value of taking daily notes.

A big advantage of the digital version of the notebook is that we are not limited by the space available on the paper page.
---

## Features
- **Add daily notes** through a web interface
- **Instantly display** new notes after saving (no manual refresh needed)
- **Automatic date tagging** - each note is stored with the current date
- **Daily history view** - see all notes from this day across years
- **Persistent storage** in a local text file (`diary_file.txt`)

---

## How It Works - Very Easy
1. **User writes a note** in the text area  
2. **Click "Save Note"** - note is saved to `diary_file.txt` with the current date  
3. **The app reloads notes** and displays them without refreshing the browser  

Notes are stored in the following format:

    DD.MM.YYYY.
    Your note text here...

    DD.MM.YYYY.
    Another note here...

## Running the App
Open terminal in main.py location and run:

    streamlit run main.py
