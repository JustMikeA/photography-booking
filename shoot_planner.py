
import streamlit as st
import json

# Demo password for the photographer dashboard
PHOTOGRAPHER_PASSWORD = "Photo!"

from pathlib import Path

# Set up the website
st.set_page_config(
    page_title="Photography Booking",
    page_icon="📷",
    layout="centered"
)

# This file will store the bookings
booking_file = Path(__file__).with_name("bookings.json")


# Function to load existing bookings
def load_bookings():
    try:
        with open(booking_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Function to save a new booking
def save_booking(booking):
    bookings = load_bookings()
    bookings.append(booking)

    with open(booking_file, "w") as file:
        json.dump(bookings, file, indent=4)


# Website heading
st.title("📷 Photography Booking Studio")
st.write("Let's capture your story!")
st.write("Complete the form below to request a photography session.")

st.divider()

# Client information
st.header("1. Your Information")

with st.form("booking_form", clear_on_submit=True):

    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")

    st.header("2. Photography Session")

    shoot_type = st.selectbox(
        "What type of photoshoot would you like?",
        ["Portrait", "Couples", "Graduation", "Event", "Other"]
    )

    shoot_date = st.date_input("Preferred Photoshoot Date")

    location = st.text_input("Preferred Location")

    st.header("3. Camera Preference")

    camera = st.radio(
        "Which camera brand do you prefer?",
        ["Sony", "Fujifilm", "Nikon"]
    )

    st.header("4. Photography Packages")

    package = st.radio(
        "Choose your photography package:",
        [
            "$100 - 20 Photos",
            "$200 - 60 Photos",
            "$300 - 100 Photos"
        ]
    )

    st.header("5. Additional Notes")

    client_notes = st.text_area(
        "Is there anything else you'd like your photographer to know?",
        placeholder="Special requests, creative ideas, poses, or other details..."
    )

    submitted = st.form_submit_button("Submit Booking")

# Check the form when the client submits
if submitted:

    if not name.strip() or not email.strip() or not phone.strip():
        st.error("Please complete your name, email, and phone number.")

    elif "@" not in email or "." not in email:
        st.error("Please enter a valid email address.")

    elif not location.strip():
        st.error("Please enter a photoshoot location.")

    else:

        # Store the booking in a dictionary
        booking = {
            "name": name,
            "email": email,
            "phone": phone,
            "shoot_type": shoot_type,
            "date": str(shoot_date),
            "location": location,
            "camera": camera,
            "package": package,
            "client_notes": client_notes,
            "photographer_notes": "",
            "status": "Upcoming"
        }

        # Save the client's booking
        save_booking(booking)

        st.success("Your booking request has been submitted!")

        st.subheader("Your Booking Confirmation")
        st.write("Name:", name)
        st.write("Session:", shoot_type)
        st.write("Date:", shoot_date)
        st.write("Location:", location)
        st.write("Camera:", camera)
        st.write("Package:", package)
        st.write("Additional Notes:", client_notes or "None")

        st.info("This is a booking request, not a confirmed appointment.")


# Photographer dashboard
st.divider()
st.header("Photographer Dashboard")

# Ask for the photographer password
password = st.text_input(
    "Enter photographer password",
    type="password"
)

# Only show the dashboard if the password is correct
if password == PHOTOGRAPHER_PASSWORD:

    st.success("Photographer access granted!")

    # Load saved client bookings
    bookings = load_bookings()

    st.subheader("Your Bookings")
    st.write("Total bookings:", len(bookings))

    if len(bookings) == 0:
        st.info("No bookings have been submitted yet.")

    else:
        # Show each client booking
        for index, booking in enumerate(bookings):

            with st.expander(
                booking["name"] + " - " + booking["date"]
            ):

                st.write("Email:", booking["email"])
                st.write("Phone:", booking["phone"])
                st.write("Session:", booking["shoot_type"])
                st.write("Location:", booking["location"])
                st.write("Camera:", booking["camera"])
                st.write("Package:", booking["package"])
                st.write("Client Notes:", booking["client_notes"])

                # Photographer's private notes
                photographer_notes = st.text_area(
                    "Private Photographer Notes",
                    value=booking.get("photographer_notes", ""),
                    key=f"notes_{index}"
                )

                # Update booking status
                status_options = [
                    "Upcoming",
                    "Confirmed",
                    "Completed",
                    "Cancelled"
                ]

                current_status = booking.get("status", "Upcoming")

                status = st.selectbox(
                    "Booking Status",
                    status_options,
                    index=status_options.index(current_status)
                    if current_status in status_options else 0,
                    key=f"status_{index}"
                )

                # Save changes
                if st.button("Save Changes", key=f"save_{index}"):

                    bookings[index]["photographer_notes"] = photographer_notes
                    bookings[index]["status"] = status

                    with open(booking_file, "w") as file:
                        json.dump(bookings, file, indent=4)

                    st.success("Booking updated successfully!")

elif password:
    st.error("Incorrect password.")
