# LABORATORY REPORT MANAGER
This is a project that sets the stage to build an integrated laboratory management system that laboratory scientists can rely on run their activities, and send results. You can find out more in this [YouTube video](https://youtu.be/DxRCCoJTMTs).

## The inspiration
As a molecular biologist working in the largest COVID-19 testing facility in Ghana, we were faced with a great challenge of dealing with large volumes of cases, sometimes over 2000 cases, each day without a proper laboratory management system. As a newly established facility to deal with the steep shortage of molecular testing capacity in Ghana, the laboratory does have a web-based application for registering and sending results to patients, and nothing more. Already, I have designed an excel workbook some of the functions in this project. However, the focus here is to find a way to integrate the offline management system with the web application in a way that streamlines things and cuts down the laboratory’s turnaround time.

## What it does.
### Patient Registration
In registry.py is a program to register a patient into a database. The program requests for the patient’s basic biographic information. A unique code is also generated for each patient in the database upon registration.

### Reading Results
In the laboratory, a PCR investigation for SARS-CoV-2 provides an excel file with the CT values obtained during the experiment. The exported excel sheet does not indicate whether a patient is positive or negative. This is the responsibility of the scientist to make that interpretation based on the CT values obtained for the patient. Two viral target genes, N-gene as ROX and ORF-1ab as FAM are important for determining if a patient is positive, while the internal control, Cy5, is to determine wither the test is valid.
So, project.py makes a request for an excel file. It also has a function to make sure the file being entered is an excel file and that it exists in the directory. After reading the file and obtaining the CT values for ROX, FAM, and Cy5, a Covid class from covid.py is called upon to store these details for each patient using their unique patient ID. The Covid class also has a function to interpret whether a test is positive or negative depending on the details for that patient.
All of this is done taking into account whether a patient ID from the exported excel file actually exists in the database. So that if an ID from the excel file is not matched in the database, it is added to a list of unknown patient ids. This is an error checking mechanism to make sure that all patients to whom results is being calculated for are in the database, and that we know those all those for whom a wrong ID was entered so it can be addressed.

### Checking Controls if they passed
After results have been interpreted, the read_results() returns a set containing a list of patients with their tests results as well as all the wrong ids in the excel file. LUmped together with the patients is also results for the controls that were run with the tests. A function then checks whether the controls passed the test, and therefore it is safe to write the results to the database or not. A positive control must be positive while a negative control must be invalid. If any of the controls fails, the test results cannot be assigned and a message that "Control Failed" is printed to the screen.

### Assigning results to the database
When all the test controls pass, the list of patients – each an instance of the Covid class – is used to write their results into the covid_19_results table that is linked to the patients table on the patient_id. And that is how each patient can have their results assigned to them in the database.

## Challenges
This project was very personal for me where I hope to build on it so it can be used in the real world. Thus, while I am proud of what this can do, it is my dream to see it incorporated into the current web application we have. And so, I am inspired by this experience to learn Django framework for web development so I can work adequately with the software engineers who built the web application in bringing this idea into reality.
