import streamlit as st
import pandas as pd
import time

# Fake auth system (for demo)
def login(username, password):
    return username == "doctor" and password == "1234"

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame(columns=["Name", "Age", "Condition", "Progress"])

# Login page
if not st.session_state.authenticated:
    st.title("🔒 AI Wound Healing Monitor - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state.authenticated = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")
else:
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Patients", "Add Patient", "Logout"])

    if page == "Dashboard":
        st.title("📊 Dashboard")
        st.metric("Total Patients", len(st.session_state.patients))
        st.metric("Healing Well", sum(st.session_state.patients["Progress"] > 70))
        st.metric("Need Attention", sum(st.session_state.patients["Progress"] < 40))

    elif page == "Patients":
        st.title("👩‍⚕️ Patients List")
        if st.session_state.patients.empty:
            st.info("No patients added yet.")
        else:
            for _, row in st.session_state.patients.iterrows():
                with st.expander(f"{row['Name']} - {row['Condition']}"):
                    st.write(f"Age: {row['Age']}")
                    st.write(f"Wound Condition: {row['Condition']}")
                    st.progress(int(row['Progress']))

    elif page == "Add Patient":
        st.title("➕ Add New Patient")
        name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        condition = st.text_area("Wound Condition")
        progress = st.slider("Healing Progress (%)", 0, 100, 0)
        if st.button("Save"):
            new_patient = {"Name": name, "Age": age, "Condition": condition, "Progress": progress}
            st.session_state.patients = pd.concat(
                [st.session_state.patients, pd.DataFrame([new_patient])],
                ignore_index=True
            )
            st.success(f"Patient {name} added successfully!")

    elif page == "Logout":
        st.session_state.authenticated = False
        st.rerun()
