import sqlite3
import datetime


def main():
    create_patient_registry()
    conn = sqlite3.connect("patient_registry.db")
    c = conn.cursor()
    c.execute("SELECT * FROM patients")

    for row in c.fetchall():
        print(row)
    conn.close()


    # A function to get patient details.
def create_patient_registry():
    first_name = input("Patient's first name: ")
    last_name = input("Patient's last name: ")
    gender = get_gender()
    date_of_birth = get_date_of_birth()
    email_address = input("Patient's email address: ")

    add_patient_to_db(first_name, last_name, gender, date_of_birth, email_address)


    # Get patient date of birth
def get_date_of_birth():
    while True:
        date_of_birth = input("Patient's date of birth (YYYY-MM-DD): ")

        try:
            datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
            return date_of_birth
        except ValueError:
            print("Invalid date of birth.")
            continue


    # Get patient gender
def get_gender():
    valid_genders = ["male", "female"]

        # Get a valid gender
    while True:
        gender = input("Patient's gender (male/female): ")
        if gender.lower() not in valid_genders:
            print("Invalid gender.")
            continue
        break
    return gender


    # Add patient details to database
def add_patient_to_db(first_name, last_name, gender, date_of_birth, email_address):

    # Create a database connection.
    conn = sqlite3.connect("patient_registry.db")
    c = conn.cursor()

    # Create  patient table if it does not exist.
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        date_of_birth TEXT NOT NULL,
        email_address TEXT NOT NULL,
        date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )''')

    # Insert the patient data into the database.
    c.execute('''INSERT INTO patients
                (first_name, last_name, gender, date_of_birth, email_address)
                VALUES (?, ?, ?, ?, ?)''',
                (first_name, last_name, gender, date_of_birth, email_address)
                )

    # Commit the changes to the database.
    conn.commit()

    # Close the database connection.
    conn.close()



if __name__ == "__main__":
    main()