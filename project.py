from covid import Covid
import pandas as pd
import sqlite3
import os



def main():

    file_path = "/workspaces/17855489/cs50_python/final/pcr test.xlsx"
    #file_path = request_file_path()
    db_name = "patient_registry.db"

    assigned_results, uncaptured_results = read_results(file_path, db_name)

    if checking_controls(assigned_results):
        results_to_db(assigned_results)
    else:
        print("Control failed")

    print(f"List of  Uncaptured results: {sorted(uncaptured_results)}")


    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''SELECT patients.id,
            patients.first_name, patients.last_name,
            covid_19_results.results
            FROM patients
            INNER JOIN covid_19_results ON patients.id = covid_19_results.patient_id
        ''')

    for row in c.fetchall():
        print(row)
    conn.close()


    # Function to read and assign results to patients
def read_results(file_path, database_name):
        # Creating a list and set to track all patients in the results sheet
    patients = []
    patient_ids = set()
    wrong_ids = set()

    db_ids = database_ids(database_name)

    reader = read_file(file_path)

    for row in reader:
        row["ID"] = str(row["ID"])
            # First, check to make sure you're only working with results which has a patient_id is in the database
        if row["ID"] not in db_ids and row["ID"].lower() not in ["positive ctrl", "positive control", "negative ctrl", "negative control"]:
            wrong_ids.add(int(row["ID"]))
            continue

            # Get the patient ID, and change the " - "to its numeric equivalent: 45
        if row["Ct"] == " - ":
            row["Ct"] = 45

        if row["ID"] not in patient_ids:
            patient = Covid(row["ID"])
            patient_ids.add(row["ID"])
            patients.append(patient)

        for patient in patients:
            assign_results(patient, row)

    return (patients, wrong_ids)



    # Asking the user for a correct file_path
def request_file_path():

    while True:
        file_path = input("Enter the path to the Excel file: ")

            # Check if the file exists.
        if not os.path.exists(file_path):
            print("The file does not exist.")
            continue

            # Check if the file is an Excel file.
        if not os.path.isfile(file_path) or not file_path.endswith(".xlsx"):
            print("The file is not an Excel file.")
            continue
        break

    return file_path


    # Function to create a dictionary out of an excel file
def read_file(file_path):
    try:
        data = pd.read_excel(file_path)
        result = data.to_dict(orient="records")
        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []


    # Get all the patient id in the database
def database_ids(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute("SELECT id FROM patients")
    ids = [str(row[0]) for row in c.fetchall()]
    conn.close()
    return ids


    # Helper Function to do the results assignment
def assign_results(patient,row):
    if patient.id == row["ID"]:
        if row["Reporter"] == "ROX":
            patient.rox = float(row["Ct"])

        elif row["Reporter"] == "FAM":
            patient.fam = float(row["Ct"])

        elif row["Reporter"] == "Cy5":
            patient.cy5 = float(row["Ct"])
    patient.calculate_results()


    # Function to check if the controls are good to accept the results
def checking_controls(results_file):
    for patient in results_file:
        if patient.id in ["positive ctrl", "positive control"]:
            if patient.results != "Positive":
                return False

        elif patient.id in ["invalid"]:
            if patient.results != "Negative":
                return False
    return True

    # Function to write the results to the database
def results_to_db(results_file):

    # Create a database connection.
    conn = sqlite3.connect("patient_registry.db")
    c = conn.cursor()

    # Create COVID-19 Results table if it doesn't exist.
    c.execute('''CREATE TABLE IF NOT EXISTS covid_19_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        rox FLOAT NOT NULL,
        fam FLOAT NOT NULL,
        cy5 FLOAT NOT NULL,
        results TEST NOT NULL,
        time_of_results TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )''')

        # Reading through the results and jumping over the controls
    for result in results_file:

            # Check if patient already has results in the database
        c.execute("SELECT COUNT(*) FROM covid_19_results WHERE patient_id = ?", (result.id,))
        count = c.fetchone()[0]

        if count > 0 or result.id.lower() in ["positive ctrl", "positive control", "negative ctrl", "negative control"]:
            continue
        else:
            c.execute('''INSERT INTO covid_19_results (patient_id, rox, fam, cy5, results)
            VALUES (?, ?, ?, ?, ?)''',
            (result.id, result.rox, result.fam, result.cy5, result.results, )
            )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
