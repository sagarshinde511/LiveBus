import streamlit as st
import mysql.connector
from mysql.connector import OperationalError, IntegrityError

# MySQL database connection details
host = "82.180.143.66"
user = "u263681140_students"
passwd = "testStudents@123"
db_name = "u263681140_students"

# Function to fetch data from BusPass table based on RFID
def fetch_data_from_buspass(rfid=None):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        cursor = conn.cursor()

        # Query to fetch all data or filtered by RFID
        if rfid:
            query = f"SELECT * FROM BusPass WHERE RFID = '{rfid}'"
        else:
            query = "SELECT * FROM BusPass"
        
        cursor.execute(query)
        rows = cursor.fetchall()

        # Fetch column names
        col_names = [desc[0] for desc in cursor.description]

        cursor.close()
        conn.close()

        return col_names, rows
    except OperationalError as e:
        st.error(f"Database connection error: {e}")
        return None, None
    except IntegrityError as e:
        st.error(f"Database integrity error: {e}")
        return None, None

# Function to fetch Name, Gender, Age, Balance, and Photo from BusPassangers
def fetch_data_from_buspassangers(rfid):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        cursor = conn.cursor()

        # Select specific columns including photo
        query = f"SELECT Name, Gender, Age, Balance, Photo FROM BusPassangers WHERE RFID = '{rfid}'"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Set column names (excluding photo)
        col_names = ['Name', 'Gender', 'Age', 'Balance']

        # Extract photo (5th column)
        photo_data = None
        if rows:
            photo_data = rows[0][4]

        # Keep only relevant columns for display
        filtered_rows = [row[:4] for row in rows]

        cursor.close()
        conn.close()

        return col_names, filtered_rows, photo_data
    except OperationalError as e:
        st.error(f"Database connection error: {e}")
        return None, None, None
    except IntegrityError as e:
        st.error(f"Database integrity error: {e}")
        return None, None, None

# --- Streamlit App ---

st.title("🚌 Live Bus Passengers")

# Fetch BusPass data to display RFID options
col_names, rows = fetch_data_from_buspass()

if col_names and rows:
    # Display BusPass table
    st.subheader("Current Passengers from Bus")
    buspass_df = [dict(zip(col_names, row)) for row in rows]
    st.table(buspass_df)

    # Extract RFID list (assuming 3rd column is RFID)
    rfid_numbers = [row[2] for row in rows]  # Adjust index if needed
    selected_rfid = st.selectbox("Select RFID No", rfid_numbers)

    if selected_rfid:
        st.subheader(f"Passenger Info for RFID: {selected_rfid}")
        col_names, buspassangers_rows, photo_data = fetch_data_from_buspassangers(selected_rfid)

        if buspassangers_rows:
            buspassangers_df = [dict(zip(col_names, row)) for row in buspassangers_rows]
            st.table(buspassangers_df)

            if photo_data:
                if st.button("View Photo"):
                    st.image(photo_data, caption="Passenger Photo", use_column_width=True)
        else:
            st.warning("No passenger data found for selected RFID.")
else:
    st.warning("No data retrieved or connection error.")
