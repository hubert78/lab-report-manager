import pytest
import pandas as pd
import os
import copy
import sqlite3
from covid import Covid
from project import database_ids, read_results, assign_results, checking_controls, results_to_db

# Test database connection
def test_database_ids():
    database_name = "patient_registry.db"
    ids = database_ids(database_name)
    assert isinstance(ids, list) and isinstance(ids[0], str)


# Test read_results function
def test_read_results():
    file_name = "/workspaces/17855489/cs50_python/final/pcr test.xlsx"
    database_name = "patient_registry.db"

    patients, results_not_captured = read_results(file_name, database_name)

    assert len(patients) > 0
    assert len(results_not_captured) >= 0

    # Check that the first patient has the correct results
    patient = patients[0]
    assert patient.id == "1"
    assert patient.rox == 29.2
    assert patient.fam == 38.96
    assert patient.cy5 == 26.22
    assert patient.results == "Positive"


    # Tests the assign_results function
def test_assign_results():

    patient = Covid("1")
    row = {"ID": "1", "Reporter": "ROX", "Ct": "45"}

    assign_results(patient, row)

    # Check that the patient's rox attribute is set correctly.
    assert patient.rox == 45

    # Check that the patient's fam attribute is set to None.
    assert patient.fam is None

    # Check that the patient's cy5 attribute is set to None.
    assert patient.cy5 is None


# Test checking_controls function
def test_checking_controls():
    positive = Covid("positive ctrl")
    positive.rox = 36.7
    positive.fam = 38.2
    positive.cy5 = 27.3
    positive.calculate_results()

    negative = Covid("negative ctrl")
    negative.rox = 45
    negative.fam = 45
    negative.cy5 = 31
    negative.calculate_results()

    results_file = [positive, negative]

    assert checking_controls(results_file) is True

    # Test with a failed positive control
    pos_results_file = copy.deepcopy(results_file)

    pos_results_file[0].rox = 45
    pos_results_file[0].fam = 45
    pos_results_file[0].calculate_results()

    assert checking_controls(pos_results_file) is False

    # Test with a failed negative control
    neg_results_file = copy.deepcopy(results_file)
    neg_results_file[1].rox = 32.6
    neg_results_file[1].fam = 34.7
    neg_results_file[1].calculate_results()

    assert checking_controls(neg_results_file) is False

# Test results_to_db function
def test_results_to_db():

    patient1 = Covid("Test 1")
    patient1.rox = 36.7
    patient1.fam = 38.2
    patient1.cy5 = 27.3
    patient1.calculate_results()

    patient2 = Covid("Test 2")
    patient2.rox = 45
    patient2.fam = 45
    patient2.cy5 = 31
    patient2.calculate_results()

    results_file = [patient1, patient2]

    results_to_db(results_file)

    # Connect to the database and check that the results were inserted correctly
    conn = sqlite3.connect("patient_registry.db")
    c = conn.cursor()

    c.execute("SELECT * FROM covid_19_results WHERE patient_id IN ('Test 1', 'Test 2')")
    results = []
    for row in c.fetchall():
        results.append(row[1:-1])

    assert results[0] == ("Test 1", 36.7, 38.2, 27.3, "Positive")
    assert results[1] == ("Test 2", 45, 45, 31, "Negative")

    conn.close()


