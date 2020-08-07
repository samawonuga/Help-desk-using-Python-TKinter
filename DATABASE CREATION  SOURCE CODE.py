import sqlite3

conn= sqlite3.connect("EYEMARTdb.db")
c= conn.cursor()

c.execute('''INSERT INTO Timetable
                  VALUES('Monday, 9:00, 14:00, 14:45, 18:00, 986763)'''

 
patientQuery = ''' CREATE TABLE Patient (
	Patient_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
	First_Name VARCHAR(30) NOT NULL,
	Last_Name VARCHAR(30) NOT NULL,
	Date_of_Birth DATE NOT NULL,
	Email VARCHAR(50),
	County VARCHAR(50) NOT NULL,
	Town VARCHAR(50) NOT NULL,
	Address VARCHAR(50) NOT NULL,
	Post_Code VARCHAR(10) NOT NULL,
	Mobile INTEGER(11),
	NHS BOOLEAN NOT NULL)'''

opticianQuery   = ''' CREATE TABLE Optician (
	GOC INTEGER PRIMARY KEY NOT NULL,
	First_Name VARCHAR (100) NOT NULL,
	Last_Name VARCHAR (100) NOT NULL
	)'''

appointmentQuery = ''' CREATE TABLE Appointment (
        Appointment_No INTEGER PRIMARY KEY AUTOINCREMENT,
	Date DATE NOT NULL,
	Time TIME NOT NULL,
	GOC INTEGER NOT NULL,
	Patient_ID INTEGER NOT NULL,
	Appointment_Reason VARCHAR(100),
	Status VARCHAR(50),
	FOREIGN KEY(Patient_ID) REFERENCES Patients(Patient_ID),
	FOREIGN KEY(GOC) REFERENCES Optician(GOC))'''

timeTableQuery =''' CREATE TABLE Timetable (
	Day  VARCHAR(8) PRIMARY KEY NOT NULL,
	Start_Time TIME NOT NULL,
	Break_Time TIME NOT NULL,
	After_Break_Time TIME NOT NULL,
	End_Time TIME NOT NULL,
	Optician INTEGER NOT NULL,
	FOREIGN KEY(Optician) REFERENCES Optician(GOC))'''

c.execute(patientQuery)
c.execute(appointmentQuery)
c.execute(opticianQuery)
c.execute(timeTableQuery)

conn.commit()
conn.close()
