#MODULE FOR SQLite access
import sqlite3

#TKINTER FEATURE MODULES
from tkinter import *
import tkinter.messagebox as box
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

#MODULES FOR DATE AND TIME MANUPULATION AS 
import datetime
from datetime import *

#MODULE FOR CALENDER FORMAT
import calendar

#MODULE FOR PRINTING ACCESS
import os


#Creates a root window
root = Tk()

#Creating a full screen layout with Logo at the top
fullscren = root.attributes('-fullscreen', True)
root.title("EYEMART")
brand = Label(root, text="EYEMART", font="Arial 20 bold italic")
brand.pack(side=TOP)

#Python calender module interprets months in integer format e.g. 5 for May
#Months can be stored in a dictionary 
#When  user selects a month value, the key can be passed to the calender
#This allows user to select a value of the month in user friendly format e.g. "March"
monthDict = { 1:"January", 2:"February",3:"March",
4:"April", 5:"May", 6:"June",
7:"July", 8:"August", 9:"September",
10:"October", 11:"November", 12:"December"}

#Connection to the database is established
conn = sqlite3.connect("Eyemartdb.db")
c = conn.cursor()


class PatientFrameUI:
    
    def getPatientEntryForm(self):
        #New frame 
        self.patientFrame = Toplevel()
        frame = self.patientFrame

        #labels
        Label(frame, text="Firstname", width=25).grid(column=1, row=1, stick = E)
        Label(frame, text="Surname", width=25).grid(column=1, row=2, stick = E)
        Label(frame, text="Date of birth", width=25).grid(column=1, row=3, stick = E)
        Label(frame, text="Post Code", width=25).grid(column=1, row=4, stick = E)
        Label(frame, text="Patient id (Optional)", width=25).grid(column=1, row=8, stick = E)

        #entry boxes
        self._Firstname_Entry = Entry(frame)
        self._Surname_Entry = Entry(frame)
        self._DateOfBirth_Entry = Entry(frame)
        self._Postcode_Entry = Entry(frame)     
        self._PatientId_Entry = Entry(frame)

        #grid layout
        self._Firstname_Entry.grid(column=2, row=1)
        self._Surname_Entry.grid(column=2, row=2)
        self._DateOfBirth_Entry.grid(column=2, row=3)
        self._Postcode_Entry.grid(column=2, row=4)
        self._PatientId_Entry.grid(column=2, row=8)

        return frame 

    def getPatientFromDatabase(self, fn, sn, dob, pc, pid):
         

        self.patientId = pid
        self.firstname = fn
        self.surname = sn
        self.dateOfBirth = dob
        self.postcode = pc
            

        try:
            self.patientId= int(pid)
            
        except:
            pass
        
        #this query is executed if patient ID has not been entered
        if self.patientId == "":
            try:
                print(self.firstname, self.surname, self.dateOfBirth, self.postcode)
                #checks database if entered details exists
                c.execute('''SELECT Patient_ID, First_Name, Last_Name, Address FROM Patient
                        WHERE First_Name=? AND Last_Name=? AND
                        Date_of_Birth=? AND Post_Code=?
                        ''', (self.firstname, self.surname, self.dateOfBirth, self.postcode,))

                patient = c.fetchall()#all of details found is stored in multidimensional array
                print(patient)
                return patient
            
            except:
                #calls constructor again if no patient is found
                box.showinfo('','No patient found')
                return False
        else:
            try:
                #checks if entered patient ID exists
                c.execute('''SELECT Patient_ID, First_Name, Last_Name, Address FROM Patient WHERE Patient_ID=?''', (self.patientId,))
                patient = c.fetchall()#stores record in array
                return patient
              
            except:
              #calls constructor again if no patient is found
                box.showinfo('','No patient found')
                return False

    
    def displayPatient(self, patientToDiplay, pId):
        
        #details of the patient found in database is passed as a parameter
        self.patientDetails = patientToDiplay #this allows all methods to access the array
        patientDetails = self.patientDetails

        #patient id is assign to a new identifier that can be acccessed by other methods
        self.patientID = pId

        #Label to identifty field
        Label(self.patientFrame, text= 'First Name:', width=10).grid(column=4, row=1, stick = E)
        Label(self.patientFrame, text= 'Surname:', width=10).grid(column=4, row=2, stick = E)
        Label(self.patientFrame, text= 'Address:', width=10).grid(column=4, row=3, stick = E)

        #Label to print patient details
        Label(self.patientFrame, text= patientDetails[0][1], width=25).grid(column=5, row=1, stick = E)
        Label(self.patientFrame, text= patientDetails[0][2], width=25).grid(column=5, row=2, stick = E)
        Label(self.patientFrame, text= patientDetails[0][3], width=25).grid(column=5, row=3, stick = E)

        return self.patientFrame





class Patient(PatientFrameUI):
    def __init__(self):

        ##Frame Widgets
        #mainWindow is the main root of the program
        self._mainWindow = Toplevel()
        #a new frame is created inside the main window
        self._frame = Frame(self._mainWindow)


        ##Button Widgets
        #newPatientButton would go to the newPatient method if clicked
        self.newPatientButton = Button(self._frame, text = 'New Patient',
                                       font= "bold",fg="black", bg="white",
                                       width = 25, command = self.newPatient)
        
        #exisitingPatient Button would go to the existingPatient method if clicked
        self.exisitingPatientButton = Button(self._frame, text = 'Existing Patient',
                                             font= "bold",fg="black", bg="white",
                                             width = 25, command =  self.exisitingPatient)

        ##Packing the widgets
        self.exisitingPatientButton.pack()
        self.newPatientButton.pack()
        self._frame.pack()
        

    def newPatient(self):

        #Toplevel object is used to present a new window for new patient registration
        self.newPatientFrame = Toplevel(self._mainWindow)

        #newPatientFrame is given the name frame, so it become easier to type
        frame = self.newPatientFrame 

        #The layout is manged by the grid manager 
        #The grid manager organises widgets in a table-like structure in the parent frame widget.

        
        #Labels to prompt user which data to enter
        Label(frame, text="First Name", width=25).grid(column=1, row=1, stick = E )
        Label(frame, text="Surname", width=25).grid(column=1, row=2, stick = E)
        Label(frame, text="Date of Birth", width=25).grid(column=1, row=3, stick = E)
        Label(frame, text="Email", width=25).grid(column=1, row=4, stick = E)
        Label(frame, text="County", width=25).grid(column=1, row=5, stick = E)
        Label(frame, text="Town", width=25).grid(column=3, row=1, stick = E)
        Label(frame, text="Post Code", width=25).grid(column=3, row=2, stick = E)
        Label(frame, text="Address", width=25).grid(column=3, row=3, stick = E)
        Label(frame, text="Phone", width=25).grid(column=3, row=4, stick = E)

        #Entry boxes is where user enters data
        self.firstname = Entry(frame)
        self.surname  = Entry(frame)
        self.dateOfBirth  = Entry(frame)
        self.email = Entry(frame)
        self.county  = Entry(frame)
        self.town  = Entry(frame)
        self.postcode = Entry(frame)
        self.address  = Entry(frame)
        self.phone = Entry(frame)
        self.NHS = Checkbutton(frame, text="NHS")
        
        #Grid Layout to organise entry boxes next to appropiate label 
        self.firstname.grid(column=2, row=1)   
        self.surname.grid(column=2, row=2)   
        self.dateOfBirth.grid(column=2, row=3)   
        self.email.grid(column=2, row=4)   
        self.county.grid(column=2, row=5)   
        self.town.grid(column=4, row=1)   
        self.postcode.grid(column=4, row=2)   
        self.address.grid(column=4, row=3)   
        self.phone.grid(column=4, row=4)
        self.NHS.grid(column=4, row=5)
        

        #Buttons
        b1 = Button(frame, text = 'Save Data', font= "bold",
                    fg="black", bg="white", width=15, command = self.__newPatientValidation)


        #Grid buttons
        b1.grid(column =3, row=11)

    #A new method is created, because of the problems with parameter passing using buttons and entry boxes in tkinter
    #The method wll get all the entered inputs, and can then pass the variables to the desired subroutine
        
    def __newPatientValidation(self):

        #TRY...EXCEPT Clause used for validation
        #this ensures data is in correct integer or string form
        try:
            name = str(self.firstname.get())
            surname = str(self.surname.get())
            dateOfBirth = str(self.dateOfBirth.get())
            email = str(self.email.get())
            county = str(self.county.get())
            town = str(self.town.get())
            postcode= str(self.postcode.get())
            address = str(self.address.get())
            phone = int(self.phone.get())
            NHS = self.NHS.cget("text")

        #if there was an issue getting a string or integer format of appropiate database a message is displayed  
        except:
            box.showinfo('','Please enter appropiate data')

        #NHS field is in boolean format in database
        #In tkinker, a ticked checkbox means the checkbox would store the text inside it
        #In this case if the checkbox is clicked, it would store the string NHS, so can be passed as 'True'
        if NHS == "NHS":
            NHS = True

        else:
            NHS = False
         
        #all the data entered by user in the appropoate data type will be passed as arguments to the saveData function
        self.saveData(name, surname, dateOfBirth, email, county,
                 town, postcode, address, phone, NHS)


    def saveData(self,firstname, surname, dateOfBirth, email, county,
                         town, postcode, address, phone, NHS):      

        #Tries to insert data to the database
        try:
            c.execute('''INSERT INTO Patient (First_Name, Last_Name, Date_of_Birth, Email,	
            County,	Town, Address, Post_Code, Mobile, NHS)
                    VALUES(?,?,?,?,?,?,?,?,?,?)''',(firstname, surname, dateOfBirth,
                                              email, county, town, address, postcode,
                                              phone, NHS))
            conn.commit()
            #once the data has been saved the entry form for the new patient can be removed
            self.newPatientFrame.destroy()

        except:
            box.showinfo('','There was a problem')

    def exisitingPatient(self):

      #goes to the find patient method
        self.patientFrame = self.getPatientEntryForm()

        
        #Buttons
        b1 = Button(self.patientFrame, text="Search Data", font="bold",
                    fg="black", bg="white", width=15, command = self.__searchExistingPatient)

        #Grid buttons
        b1.grid(column =3, row=11)    
    
    def __searchExistingPatient(self):

        #passes the entries in the inherited method to get a given patient  
        patient = self.getPatientFromDatabase(self._Firstname_Entry.get(), self._Surname_Entry.get(),
                                   self._DateOfBirth_Entry.get(), self._Postcode_Entry.get(),
                                   self._PatientId_Entry.get())
        
        if patient == False:
            Patient()

        elif patient == []: #if no one matched the data
            Patient()

        else:
            dataId = patient[0][0]#patient id
            frame = self.displayPatient(patient, dataId)#method that displays pateint
   
            b1 = Button(frame, text="View Appointments", font="bold",
                        fg="black", bg="white", width=15, command = self.viewPatientAppointments)
            b1.grid(column =5, row=11)

            b2 = Button(frame, text="Edit Patient", font="bold",
                        fg="black", bg="white", width=15, command = self.editPatient)
            b2.grid(column =6, row=11)


    def viewPatientAppointments(self):

        ##Create a new window
        self.viewAppointmentWindow = Toplevel()

        #gets appointment details of entered patient
        c.execute('''SELECT Appointment.Date, Appointment.Time,
        Patient.First_Name, Patient.Last_Name,
        Optician.First_Name, Optician.Last_Name
        FROM ((Appointment INNER JOIN Patient ON Appointment.Patient_ID = Patient.Patient_ID)
        INNER JOIN Optician ON Appointment.GOC = Optician.GOC)
        WHERE Appointment.Patient_ID =?
        ORDER BY Date,Time ASC''', (self.patientID,))
        
        appointmentForPatient= c.fetchall()

        #creates a new text where appointment details will be displayed
        t = Text(self.viewAppointmentWindow)

        #prints all appointment details for the patient in the text file
        for x in range(0, len(appointmentForPatient)):
            t.insert(END, appointmentForPatient[x])
            t.insert(END, '\n')#creates a space
        t.pack()
 
     
    def editPatient(self):
        #creates a new window for editing patient 
        self.editPatient = Toplevel()

        #gets patients details where based on where the id the same
        c.execute('''SELECT * FROM Patient WHERE Patient_ID=?''', (self.patientID,))
        
        #gets all the database columns in the EYEMART database
        databaseColumn = [description[0] for description in c.description]
        del databaseColumn[0]#deletes the Patient_ID coloum

        #prints all the patient details
        #list is stored in the identifier patientAll
        patientAll=  c.fetchall()[0]
        self.patientData = list(patientAll)
        del self.patientData[0] #removes the Patient_ID record

        #a new dictionary is created where each column in the database is mapped to a variable
        self.fieldDictionary = {}
        
        #all the fields that user's can select from is stored in the field array
        fields =['firstname' ,'surname', 'Date of Birth', 'Email',
                 'County', 'Town','Address','Postcode', 'Phone','NHS']

        #this code stores sets the values in the fields array as the keys and values as database columns
        for x in range(0, len(fields)):    
            key_fields = fields[x]
            value_databaseFormat= databaseColumn[x]
            self.fieldDictionary[key_fields] = value_databaseFormat
            
        #keys in the dictioionary is presented in a menu
        variable = StringVar(self.editPatient )
        variable.set('Select a data to edit') # default value
        self.w = OptionMenu( self.editPatient , variable, *self.fieldDictionary.keys(), command = self.__editPatientEntry)
        self.w.grid(row = 0, column = 0)

    def __editPatientEntry(self, field):

        #stores the database column value of the selected field
        self.db= self.fieldDictionary.get(field)
        editPatient = self.editPatient 
        self.w.destroy()
        
        ##labels and grid layout
        label_editing = Label(editPatient, text = "You are editing "+
                              self.patientData[0]+" "+self.patientData[1]+"'s "+ field)
        label_to = Label(editPatient, text = "New "+field+":")

        #grids the labels
        label_editing.grid(row = 0, column = 0, columnspan = 2)
        label_to.grid(row = 2, column = 0, sticky = E)
 
         
        ##entryboxs and grid layout
        self.entry_update1 = Entry(editPatient)
        self.entry_update1.grid(row = 2, column = 1)
        
        ##buttons, gird layout and function binding
        button_saveChanges = Button(editPatient, text = "Save changes", command = self.saveEditPatient)
        button_saveChanges.grid(row = 4, column = 0) 
         
        ##update database field to entered change

    def saveEditPatient(self):

        #updates the Patient field selected by the user
        #new value is based on the user entry
        try:
            c.execute('''UPDATE Patient SET {} = ?
                    WHERE Patient_ID = ?'''.format(self.db),
                    (self.entry_update1.get(), self.patientID))
        except:
            box.showinfo('','There was a problem')
            #if value could not be entered, message box is displayed


    
class Booking(PatientFrameUI):
    def __init__(self, m, y):
        
        #months and years selected by the user
        self.month = m
        self.year = y

        #goes to the find patient method
        patientFrame = self.getPatientEntryForm()

        #Buttons
        b1 = Button(patientFrame, text="Search Data", font="bold",
                    fg="black", bg="white", width=15, command = self.getPatient)

        #Grid buttons
        b1.grid(column =3, row=11)

    def getPatient(self):
        
        firstname = self._Firstname_Entry.get()
        surname = self._Surname_Entry.get()
        dateOfBirth = self._DateOfBirth_Entry.get()
        postcode = self._Postcode_Entry.get()
        patientId =self._PatientId_Entry.get()
        patient = self.getPatientFromDatabase(firstname, surname, dateOfBirth, postcode, patientId)
    
        if patient == False:
            Booking(self.month, self.year)

        elif patient == []:
            Booking(self.month, self.year)

        else:
            dataId = patient[0][0]#patient id
            frame = self.displayPatient(patient, dataId)#method that displays pateint

        #Buttons
        b1 = Button(frame, text="Select Date", font="bold",
                    fg="black", bg="white", width=15, command = self.newCalender)
      
        b1.grid(column =5, row=11)
        
    def newCalender(self):
        
        #Calender window
        self._Window = Toplevel()  #New window where booking details appear
        calenderFrame = Frame(self._Window) #New frame within the window is created for the calender details

        #Calender 
        cal_data = calendar.month(int(self.year),int(self.month),w = 2, l = 1) #getting the month and year of calender
        #operation below prints the text of the calender data in a the frame
        cal_out = Label(calenderFrame, font=('courier', 12, 'bold'), bg='lightgrey', justify=LEFT, text=cal_data,)
        #padx and pady are used to allign the calender so it display similar to a real calender
        cal_out.pack(padx=3, pady=10)

        #Widgets
        datePicker = Label(calenderFrame, text="Enter Date (e.g. 01):")
        self.dateEntry = Entry(calenderFrame)
        bookButton = Button(calenderFrame, text="Select Time",command= self.dateVerfication)

        #Packing the Widgets
        calenderFrame.pack(side=LEFT)
        datePicker.pack(padx=6, pady=12)
        self.dateEntry.pack()
        bookButton.pack()      
      
    def dateVerfication(self):

        #Gets the day, year and month entries and puts it in a date format
        dateFormat = date(int(self.year), int(self.month), int(self.dateEntry.get()))
        currentDate = datetime.now().date()
        
        #Selection statement checks if the date entered has passed
        if dateFormat < currentDate:
            box.showinfo('Error','Date Has Passed')

            #if date has passed, goes back to the calender method 
            self.newCalender()
            
        else:
            #strfttime object is used to format date in DD-MM-YYYY
            self.appointmentDate = dateFormat.strftime('%d-%m-%Y')
            self.getTimeSlot()
            #if date has not passed, the timeslots methods is called

    def getTimeSlot(self):
    
        #Timeslot window
        self.timeslotFrame = Frame(self._Window)
        self.timeslotFrame.pack()
        timeslotFrame = self.timeslotFrame

            
        #GETTING DATE INTO WEEK DAY DATE
        enteredDate= self.appointmentDate 
        splitDate = enteredDate.split('-')
        dayOfWeekIndex = calendar.weekday(int(splitDate[2]),int(splitDate[1]),int(splitDate[0]))
        dayOfWeek  = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"][dayOfWeekIndex]


        #GETTING All DATA ABOUT TIMES FOR A DAY
        c.execute('''SELECT * FROM Timetable WHERE Day =?''',(dayOfWeek ,))
        allTimes = c.fetchall()

        #GETS OPTICIAN GOC
        self.goc = allTimes[0][5]

        #GETTING THE START TIME, BREAK TIME, AFTER BREAK TIME AND END TIME FOR GIVEN DAY
        start_time = allTimes[0][1]
        break_time = allTimes[0][2]
        afterBreak_time = allTimes[0][3]
        end_time = allTimes[0][4]

        #SLOT INCREMENT
        slotIncrement  = 30

        #2D ARRAY TO STORE TIMES
        listOfTimes  = [ [],[] ]

        #BEFORE WE CAN COMPARE TIME WE MUST GET TIMES FROM THE DATABASE IN A PYTHON TIME FORMAT
        startTime = datetime.strptime(start_time, '%H:%M') 
        breakTime = datetime.strptime(break_time, '%H:%M')
        afterBreak = datetime.strptime(afterBreak_time, '%H:%M')
        endTime = datetime.strptime(end_time, '%H:%M')
        #The strptime() function converts string to a time format with the format <HOUR:MINUTE>


        #GET ALL POSSIBLE TIMES
        while startTime <= breakTime and afterBreak <= endTime:
            listOfTimes[0].append(startTime.strftime("%H:%M"))
            startTime += timedelta(minutes=slotIncrement)

            listOfTimes[1].append(afterBreak.strftime("%H:%M"))
            afterBreak += timedelta(minutes=slotIncrement)

        fullListOfTimes = listOfTimes[0]+listOfTimes[1]


        #GETS BOOKED TIMES 
        c.execute('''SELECT Time FROM Appointment WHERE Date =?
                    ORDER BY Time ASC''',(enteredDate,))
        bookedTimes = c.fetchall()
     
        
        #IF LIST IS EMPTY NO TIMESLOTS ARE REMOVED
        if len(bookedTimes) == 0:
            pass

        else:
            #REMOVING BOOKED DATES          
            for i in range (0, len(bookedTimes)):
                fullListOfTimes.remove(bookedTimes[i][0])          

              

        #object creates a list box where the times will be displayed
        self.timeslotList = Listbox(timeslotFrame)

        #Displays each timeslot index in the listbox
        for x in fullListOfTimes:
            self.timeslotList.insert(END, x)

        #Packs the button
        button = Button(timeslotFrame, text=u"Confirm Booking", command=self.appointmentReason)
        self.timeslotList.pack(padx=6, pady=12)
        button.pack(side = BOTTOM)
        timeslotFrame.pack()
        
    def appointmentReason(self):

        #getting selected time
        timesInListBox = self.timeslotList.get(0, END) # tuple with text of all items in Listbox
        indexOfTime = self.timeslotList.curselection() # tuple with indexes of selected items
        self.selectedTime = [timesInListBox[item] for item in indexOfTime] # list with text of all selected items

        #New text frame is created where user enters reason for appointmet
        self.entryFrame = Toplevel()
        self.textfield = ScrolledText(self.entryFrame, wrap=WORD)
        self.textfield.insert(INSERT, "Reason for appointment:")     
        self.textfield.pack()

        #button finally confirms booking
        button = Button(self.entryFrame, text=u"Confirm Booking", command=self.savingAppointment)
        button.pack()

    def savingAppointment(self):

        #gets all values needed for the appointment
        appointmentTime = self.selectedTime[0]  
        appointmentDate = self.appointmentDate
        patientID = int(self.patientID)
        goc = int(self.goc)
        appointmentReason = str(self.textfield.get(1.0, END))


        #Uses a try except clause to check if data can be entered to table
        try:
            c.execute('''INSERT INTO Appointment (Date, Time, GOC, Patient_ID,	
                 	Appointment_Reason)
                    VALUES(?,?,?,?,?)''',(appointmentDate, appointmentTime, goc,
                                              patientID, appointmentReason))
            conn.commit()

        except:
            box.showinfo('','There was a problem')


        #once the data has been saved the entry form for the new patient can be removed
        self.entryFrame.destroy()
        self.timeslotFrame.destroy()
        self._Window.destroy()
        self.patientFrame.destroy()
        self.bookingInvoice(appointmentDate, appointmentTime, goc, patientID, appointmentReason)
    

    def bookingInvoice(self, date, time, goc, pid, reason):

        #gets the appointment ID for the newly booked appointment
        c.execute('''SELECT Appointment_No from Appointment
                    WHERE Date =? AND Time=?''', (date, time,))

        #gets appointment number of new appointment
        appointmentNo = c.fetchall()[0][0]

        #gets information about appointsment
        c.execute( '''SELECT Patient.First_Name, Patient.Last_Name,
        Optician.First_Name, Optician.Last_Name
        FROM ((Appointment INNER JOIN Patient ON Appointment.Patient_ID = Patient.Patient_ID)
        INNER JOIN Optician ON Appointment.GOC = Optician.GOC)
        WHERE Appointment_No =?''', (appointmentNo,))

        #gets patient and optician name from specific appointment
        names = c.fetchall()[0]
    
    
        #A new text file is created with the number being the name
        filename = 'Appointment Number '+ str(appointmentNo) + '.txt'

        #program tries to print a booking invoice to a text file
        try:
            #details are written to file
            with open(filename,'w+') as f:

                #writes the details of the patient
                f.writelines('Appointment Date:')
                f.writelines(date+'\n')#\n creates a new line
                             
                f.writelines('Appointment Time:')
                f.writelines(time+'\n')

                f.writelines('Optician GOC:')
                f.writelines(str(goc)+'\n')
                           
                f.writelines('Optician:')
                f.writelines(names[2]+' '+names[3]+'\n')
        
                f.writelines('PatientID:')
                f.writelines(str(pid)+'\n')

                f.writelines('Patient:')
                f.writelines(names[0]+' '+names[1]+'\n')

                f.writelines(reason)

            #the file is printed to the selected
            os.startfile(filename, "print")
            f.close()

            #message showing appointment has been booked
            box.showinfo('','Your appointment has been booked')


        except:
            #if file could not be written to this is prented
            box.showinfo('','There was an error printing your booking invoice')


class Timetable(Booking):
    def __init__(self):

        #new window for appointments is created 
        self.timetablewindow = Toplevel()
        
        #calls the method for creating the UI
        self.timetableUI()

    def timetableUI(self):

        #following sql statement gets information about all appointments
        c.execute( '''SELECT Appointment.Date, Appointment.Time,
        Patient.First_Name, Patient.Last_Name,
        Optician.First_Name, Optician.Last_Name
        FROM ((Appointment INNER JOIN Patient ON Appointment.Patient_ID = Patient.Patient_ID)
        INNER JOIN Optician ON Appointment.GOC = Optician.GOC)
        ORDER BY Date,Time ASC''')

        #stores all appointments details in the variable appointmentDetails
        self.appointmentDetails = c.fetchall()

        #stores identifiers with python 'self' in another variable that is shorter to call
        appDetails = self.appointmentDetails
        timetablewindow = self.timetablewindow

        #New treeview which is a table like structure
        self.t = ttk.Treeview(timetablewindow, columns=("Name", "Date", "Time", "Optician"))

        #heading for tree specified below
        self.t.heading("Name", text="Patient")
        self.t.heading("Date", text="Date")
        self.t.heading("Time", text="Time")
        self.t.heading("Optician", text="Optician")
        self.t.pack(padx=20, pady=10)

        #store all the details from the appointment in the table                                        
        for i in range (0, len(appDetails)):
            self.t.insert('', 'end',  text=i+1 , values=(appDetails[i][2] + " " + appDetails[i][3], appDetails[i][0],
                             appDetails[i][1], appDetails[i][4]+ " "+ appDetails[i][5]))

        #Buttons are created
        b1 = Button(timetablewindow, text = 'Delete Appointment', font= "bold",
                    fg="black", bg="white", width=15, command = self.delete)


        b2 = Button(timetablewindow, text = 'View Appointment', font= "bold",
                    fg="black", bg="white", width=15, command = self.view)

        #Grid buttons
        b1.pack(side =LEFT)
        
        #Grid buttons
        b2.pack(side =LEFT)

        #user may wish to book for a new appointment
        self.e1 = Entry(timetablewindow)
        self.e2 = Entry(timetablewindow)
        self.e1.insert(0, " Month (e.g 03)") #default value in entry
        self.e2.insert(0, " Year (e.g. 2018)")#default value in entry

        #buttons and entry is packed
        Button(timetablewindow, text='Book New', font= "bold",
                    fg="black", bg="white", width=15,command=self.bookingNew).pack(side =RIGHT)
        self.e1.pack(side =RIGHT)
        self.e2.pack(side =RIGHT)
        

    def delete(self):
        
        #gets the currently selected item and deltes it from the table  
        curItem = self.t.focus()
        newDict = self.t.item(curItem)
        self.t.delete(curItem)

        #selected item is stored in a dictonary where a list of all rows are the values
        #following statements get values of selected items
        for key, value in newDict.items():
            if key == 'values' :
                sel= value

        #deletes record from the database where date and time is the selected one by user
        c.execute("DELETE FROM Appointment WHERE Date=? AND Time=?", (sel[1], sel[2],))
        box.showinfo('',sel[1], " ", sel[2], "  has been deleted")

        conn.commit()

    def view(self):

        #likewise in delete method, this gets selected item 
        curItem = self.t.focus()
        newDict = self.t.item(curItem)
       
        for key, value in newDict.items():
            if key == 'values' :
                sel= value

        #gets the appointment details from the database 
        c.execute("SELECT * FROM Appointment WHERE Date=? AND Time=?", (sel[1], sel[2],))
        appointment= c.fetchall()
        appointmentNo = appointment[0][0]

        #gets entered file number in a format that matches an saved invoice
        appointmentFile = 'Appointment Number ' + str(appointmentNo) +'.txt'
        
        #opens correct file
        os.startfile(str(appointmentFile))

        conn.commit()


    def bookingNew(self):
        try:
            #gets the entered month and year
            month = int(self.e1.get())
            year = int(self.e2.get())
           
            #checks if year is within 1 year
            if year == int(datetime.now().year) or year == int(datetime.now().year +1):
                #checks if month is between 1 and 12
                if month >= 1 and month <= 12:
                    #calls booking class with month and year entered as arguments
                    Booking(month, year)

                #message is displayed if a month not possible is entered
                else:
                    box.showinfo('','Please enter correct month data')
                    Timetable() #calls Timetable class again
                    
            #message is displayed if wrong year is entered
            else:
                  box.showinfo('','Please enter correct year data within 1 year')
                  Timetable()#calls Timetable class again

        except:
            box.showinfo('','Month and Year format wrong')
            #if month is not an message is dispayed and Timetable class is called again
            Timetable()

def selectMonth():
    global dateWindow
    
    #New window for selecting date and month 
    dateWindow = Toplevel()

    #Creates a drop down option menu that presents all the values in the dictionary
    variable = StringVar(dateWindow)
    variable.set('Select a month') # default value

    #option menu used to create drop down menu of available months
    #the values in the month dictionary are used to create the options
    monthSelector = OptionMenu(dateWindow, variable, *monthDict.values(), command= selectYear)
    monthSelector.pack()

def selectYear(m):
    #variables are declared globally so they can be used in selectMonth subroutine
    global years
    global month
    global slider 
    
    #Gets the key for the selected value in the month dictionary
    for key, value in monthDict.items():
        if value == m :
            month = key

    #bookings can only either be for the current year or next year
    years = [datetime.now().year, datetime.now().year + 1]

    #the Scale object presents a the years tuple in a slider for the user to select
    slider = Scale(dateWindow,  from_= years[0], to=years[1],
                  orient='horizontal',)

    #bind is used so when the button is release, it goes to the goToBooking method
    #passes the values selected when the button is released as an argument
    slider.bind("<ButtonRelease-1>", goToBooking)
    slider.pack()

def timeTableMenu():
    Timetable()

def patientMenu():
    Patient()

def goToBooking(event):
    #gets year selected in slider
    year = slider.get()

    #noe year and month has been selected, the frame for it can be destroyed
    dateWindow.destroy()

    #passes the selected month and year parameters to the newCalender
    Booking(month, year)

def quitcommand():
    root.destroy()

def adminMenu():
    frame = Frame(root)

    #Menu
    optionMenu= Menu(frame) #menu class is initiated in the new frame window
    root.config(menu=optionMenu)#Setting the parameter to the created menu allows Tkinter to recognise a menu creation

    #Submenu for the functionalities the user can choose from
    subMenu = Menu(optionMenu)  
    optionMenu.add_cascade(label="Admin Functions", menu=subMenu)


    #A drop down menu is created with the label "Admin Function"
    #Cascade function allows drop down menus to be created 
    #Drop down menu is created and different method are called based on what user clicks
    subMenu.add_command(label="View and delete appointments", command= timeTableMenu)
    subMenu.add_command(label="View and edit patients", command=patientMenu)
    subMenu.add_command(label="Book a new appointment", command=selectMonth)

    #pack displays frame
    frame.pack()
    
def main():     
    adminMenu()
    
    Button(root, text="Quit", font="Arial 8 bold italic", width = 9,  activebackground=
       "turquoise", command=quitcommand).pack(side=TOP)

    
    
if __name__ == '__main__':
    main()




root.mainloop()
