import sqlite3
import csv

class DBHandler:
    def __init__(self, DBName):
        self.connection = sqlite3.connect(DBName, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def initaliseTables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Plants (
            PlantID INTEGER PRIMARY KEY AUTOINCREMENT,
            PlantName TEXT NOT NULL,
            PlantSpecies TEXT NOT NULL,
            PlantOwner TEXT NOT NULL
            )                    
        """) # Could Have Whole Table For Owner Details But Is Unneccesary
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Recordings (
            RecordingID INTEGER PRIMARY KEY AUTOINCREMENT,
            PlantID INTEGER NOT NULL,
            Humidity REAL NOT NULL,
            Temperature REAL NOT NULL,
            TimeRecorded DATETIME NOT NULL,
            FOREIGN KEY (PlantID) REFERENCES Plants(PlantID)
            )           
        """)
        self.connection.commit()
    
    def updatePlant(self, plantId,  newName, newOwner, newSpecies):
        try:
            updates = []
            values = []
            num = 0
            updateQuery = """UPDATE Plants SET """
            if newName is not None and newName != "":
                updates.append("PlantName = ?")
                values.append(newName)
                num = num+1
            if newOwner is not None and newOwner != "":
                updates.append("PlantOwner = ?")
                values.append(newOwner)
                num=num+1
            if newSpecies is not None and newSpecies != "":
                updates.append("PlantSpecies = ?")
                values.append(newSpecies)
                num=num+1
            if num == 0:
                    return "No Paraaters So No Change"
            if updates:
                updateQuery += ", ".join(updates)
                updateQuery += " WHERE PlantId = ?"
                values.append(plantId)
                self.cursor.execute(updateQuery, values)
                self.connection.commit()
                return "Update Successfull!"
        except sqlite3.OperationalError:
            return "SQL Operational Error"
        except sqlite3.IntegrityError:
            return "SQL Integrity Error"
        

    

    def selectPlant(self, plantId, plantName, plantSpecies, plantOwner):
        filters = []
        values = []
        selectQuery = """
        SELECT * FROM Plants WHERE 1=1
        """
        if plantId is not None and plantId != "":
            filters.append("PlantId = ?")
            values.append(plantId)
        if plantName is not None and plantName != "":
            filters.append("PlantName = ?")
            values.append(plantName)
        if plantSpecies is not None and plantSpecies != "":
            filters.append("PlantSpecies = ?")
            values.append(plantSpecies)
        if plantOwner is not None and plantOwner != "":
            filters.append("PlantOwner = ?")
            values.append(plantOwner)
        
        if filters:
            selectQuery += " AND " + " AND ".join(filters)
        self.cursor.execute(selectQuery, values)
        result = self.cursor.fetchall()
        return result
    
    def selectRecording(self, recordingId, plantId, humidMin, humidMax, tempMin, tempMax, timeRecordedMin, timeRecordedMax):
        filters = []
        values = []
        selectQuery = """
        SELECT * FROM Recordings WHERE 1=1
        """
        if recordingId is not None and recordingId != "":
            filters.append("RecordingID = ?")
            values.append(recordingId)
        if plantId is not None and plantId != "":
            filters.append("PlantID = ?")
            values.append(plantId)
        if humidMin is not None and humidMin != "":
            filters.append("Humidity >= ?")
            values.append(humidMin)
        if humidMax is not None and humidMax != "":
            filters.append("Humidity <= ?")
            values.append(humidMax)
        if tempMin is not None and tempMin != "":
            filters.append("Temperature >= ?")
            values.append(tempMin)
        if tempMax is not None and tempMax != "":
            filters.append("Temperature <= ?")
            values.append(tempMax)
        if timeRecordedMin is not None and timeRecordedMin != "":
            filters.append("TimeRecorded >= ?")
            values.append(timeRecordedMin)
        if timeRecordedMax is not None and timeRecordedMax != "":
            filters.append("TimeRecorded <= ?")
            values.append(timeRecordedMax)

        if filters:
            selectQuery += " AND " + " AND ".join(filters)
        self.cursor.execute(selectQuery, values)
        result = self.cursor.fetchall()
        return result

    
    def addPlant(self, plantName, plantSpecies ,plantOwner):
        try:
            insertQuery = """
            INSERT INTO Plants                 
            (PlantName, PlantSpecies, PlantOwner)
            VALUES (?, ?, ?)
            """
            self.cursor.execute(insertQuery, (plantName, plantSpecies, plantOwner))
            self.connection.commit()
            return "Plant Added Successfully"
        except  sqlite3.OperationalError as error:
            return "Operational Error Encountered -> " + str(error)
        except sqlite3.IntegrityError as error:
            return "Integrity Error Encountered -> " + str(error)
            
    def removePlant(self, plantId):
        try:
            deleteQuery = """
            DELETE FROM Plants
            WHERE Plants.PlantID = ?
            """
            deleteRelatedRecordings = """
            DELETE FROM Recordings
            WHERE Recordings.PlantID = ?
            """ #Code Is Structured In A Way That A Recording No Longer Exists If Related Plant Is Deleted, Recording Is Deleted First As To Avoid Errors
            self.cursor.execute(deleteRelatedRecordings, (plantId, ))
            self.cursor.execute(deleteQuery, (plantId, ))
            self.connection.commit()
            return "Plant Successfully Removed!"
        except  sqlite3.OperationalError as error:
            return "Operational Error Encountered -> " + str(error)
        except sqlite3.IntegrityError as error:
            return "Integrity Error Encountered -> " + str(error)
            
    def addRecording(self, plantId, humidity, tempLevel, timerecorded):
        try:
            insertQuery = """
            INSERT INTO Recordings
            (PlantID, Humidity, Temperature, TimeRecorded)
            VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(insertQuery, (plantId, humidity, tempLevel, timerecorded))
            self.connection.commit() 
            return "Recording Successfully Added!"
        except  sqlite3.OperationalError as error:
            return "Operational Error Encountered -> " + str(error)
        except sqlite3.IntegrityError as error:
            return "Integrity Error Encountered -> " + str(error)
            
    def removeRecording(self, recordingId):
        try:
            deleteQuery = """
            DELETE FROM Recordings
            WHERE Recordings.RecordingID = ?
            """
            self.cursor.execute(deleteQuery, (recordingId, ))
            self.connection.commit()
            return "Recording(s) Successfully Removed"
        except  sqlite3.OperationalError as error:
            return "Operational Error Encountered -> " + str(error)
        except sqlite3.IntegrityError as error:
            return "Integrity Error Encountered -> " + str(error)