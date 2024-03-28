import streamlit as st
import datetime,json
import pandas as pd

current_date = datetime.date.today()

with open("patients.json") as file:
    users = json.load(file)
    id_name_list = []
    for user in users:
        id = user["id"]
        name = user["personal_data"]["name"]
        id_name = f"{id}-{name}"
        id_name_list.append(id_name)


patient = st.sidebar.selectbox(
   "Select patient:",
   id_name_list,
   index=0,
)


section = st.sidebar.radio("Section",("Notes Summary","Explore Notes"))
if section == "Notes Summary":
    
    patient_id = patient.split("-")[0]
    patient_id = int(patient_id)
    for user in users:
        id = user["id"]
        if id == patient_id:
            personal_data = user["personal_data"]
            personal_data_df = pd.DataFrame([personal_data])
            notes = user["notes"]
            summary = user["summary"]
            key_takeways = user["key_takeways"]
            break
    
    ## show patient info
    st.subheader("Patient Information")
    st.dataframe(personal_data_df,hide_index=True)
    ## show summary
    st.subheader("Medical summary")
    st.markdown(summary)
    ## show summary
    st.subheader("Medical Key Takeways")
    for key_takeway in key_takeways:
        st.markdown(key_takeway)

    ## show summary
    st.subheader("Medical notes")
    # Create notes tabs
    note_dates = [note['date'] for note in notes]
    note_dates_tabs = st.tabs(note_dates)
    # Iterate through each tab and build content
    for note_dates_tab, note in zip(note_dates_tabs, notes):
        with note_dates_tab:
            note_text = note["text"]
            print(note_text)
            note_text = note_text.replace("\n","  \n ")
            st.markdown(f"Note:{note_text}")
            note_summary = note["summary"]
            note_summary = note_summary.replace("\n","  \n ")
            st.markdown(f"Summary:{note_summary}")



    with st.sidebar:        
        txt = st.text_area("Write a note",height = 200)
        uploaded_file  = st.file_uploader("Attach document")
        btn_add_note = st.button("Add note")
        if btn_add_note:
            pass
if section == "Explore Notes":
    st.title("Explore Notes")