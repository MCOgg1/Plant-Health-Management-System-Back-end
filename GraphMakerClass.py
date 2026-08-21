import csv
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import io
import base64
from enum import Enum
from MeasurementEnumClass import Measurement

class GraphHandler:

    def __init__(self, dbHandler, csvFile):
        self.dbHandler = dbHandler
        self.speciesData = {}
        with open(csvFile, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.speciesData[row["Species"]] = row

    def avgHumidity(self):
        query = """
        SELECT Plants.PlantName, AVG(Humidity)
        FROM Recordings
        INNER JOIN Plants ON Recordings.PlantID = Plants.PlantID
        GROUP BY Plants.PlantID
        """
        self.dbHandler.cursor.execute(query)
        result = self.dbHandler.cursor.fetchall()
        
        dataF = pd.DataFrame(result, columns=["PlantName", "AverageHumidity"])
        fig, ax = plt.subplots()
        sns.barplot(data=dataF, x="PlantName", y="AverageHumidity",ax=ax)
        ax.set_xlabel("Plants")
        ax.set_ylabel("Recorded Values")
        plt.xticks(rotation=45)
        fig.tight_layout()

        myBuffer = io.BytesIO()
        fig.savefig(myBuffer, format="png")
        myBuffer.seek(0)
        image = base64.b64encode(myBuffer.getvalue()).decode("utf-8")
        plt.close(fig)
        myBuffer.close()
        return image
    
    def avgTemp(self):
        query = """
        SELECT Plants.PlantName, AVG(Temperature)
        FROM Recordings
        INNER JOIN Plants ON Recordings.PlantID = Plants.PlantID
        GROUP BY Plants.PlantID
        """
        self.dbHandler.cursor.execute(query)
        result = self.dbHandler.cursor.fetchall()
        
        dataF = pd.DataFrame(result, columns=["PlantName", "AverageTemperature"])

        fig, ax = plt.subplots()
        sns.barplot(data=dataF, x="PlantName", y="AverageTemperature",ax=ax)
        ax.set_xlabel("All Plants")
        ax.set_ylabel("Recorded Temperature")
        plt.xticks(rotation=45)
        fig.tight_layout()

        myBuffer = io.BytesIO()
        fig.savefig(myBuffer, format="png")
        myBuffer.seek(0)
        image = base64.b64encode(myBuffer.getvalue()).decode("utf-8")
        plt.close(fig)
        myBuffer.close()
        return image

    def humidityOT(self, plantId):
        query = """
        SELECT Humidity, TimeRecorded
        FROM Recordings
        WHERE PlantID = ?
        """
        self.dbHandler.cursor.execute(query, (plantId,))
        result = self.dbHandler.cursor.fetchall()

        dataF = pd.DataFrame(result, columns=["Humidity", "TimeRecorded"])
        dataF["TimeRecorded"] = pd.to_datetime(dataF["TimeRecorded"])

        fig, ax = plt.subplots()
        sns.lineplot(data=dataF, x="TimeRecorded", y="Humidity", ax=ax)

        locator = mdates.AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

        ax.set_title("Humidity of Given Plant Over Time")
        ax.set_xlabel("Time Recorded")
        ax.set_ylabel("Humidity Value Recorded")
        plt.xticks(rotation=45)
        fig.tight_layout()

        myBuffer = io.BytesIO()
        fig.savefig(myBuffer, format="png")
        myBuffer.seek(0)
        image = base64.b64encode(myBuffer.getvalue()).decode("utf-8")
        plt.close(fig)
        myBuffer.close()
        return image

    def temperatureOT(self, plantId):
        query = """
        SELECT Temperature, TimeRecorded
        FROM Recordings
        WHERE PlantID = ?
        """
        self.dbHandler.cursor.execute(query, (plantId,))
        result = self.dbHandler.cursor.fetchall()

        dataF = pd.DataFrame(result, columns=["Temperature", "TimeRecorded"])
        dataF["TimeRecorded"] = pd.to_datetime(dataF["TimeRecorded"])
        fig, ax = plt.subplots()
        sns.lineplot(data=dataF, x="TimeRecorded", y="Temperature", ax=ax)

        locator = mdates.AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

        ax.set_title("Temperature Levels at Given Plants Location Over Time")
        ax.set_xlabel("Time Recorded")
        ax.set_ylabel("Temperature Recorded")
        plt.xticks(rotation=45)
        fig.tight_layout()

        myBuffer = io.BytesIO()
        fig.savefig(myBuffer, format="png")
        myBuffer.seek(0)
        image = base64.b64encode(myBuffer.getvalue()).decode("utf-8")
        plt.close(fig)
        myBuffer.close()
        return image

    def compToIdealHumidity(self, plantId):
         query = ("""
         SELECT PlantSpecies
         FROM Plants
         WHERE PlantID = ?
         """)
         self.dbHandler.cursor.execute(query, (plantId,))
         result = self.dbHandler.cursor.fetchall()
         if not result:
             return self._errorImage("Plant not found")
         species = result[0][0] #First Field First Column
         reccValue = self._dataLookup(species, Measurement.HUMIDITY)
         if(reccValue == "N/A Species"):
             return self._errorImage("Plant not found!")
         else:
            reccValue = float(reccValue)
            query2 = ("""SELECT AVG(Humidity) FROM Recordings WHERE PlantID = ?""")
            self.dbHandler.cursor.execute(query2, (plantId,))
            averageValue = self.dbHandler.cursor.fetchall()[0][0]

            dataF = pd.DataFrame({"Type": ["Reccomended", "Average"], "Value": [reccValue, averageValue]})
            fig, ax = plt.subplots()
            sns.barplot(data=dataF, x="Type", y= "Value",ax=ax)
            ax.set_title("Recorded Average vs Reccomended Humidity Value")
            ax.set_xlabel("Reccomended vs Recorded Average")
            ax.set_ylabel("Value")
            plt.xticks(rotation=45)
            fig.tight_layout()

            myBuffer = io.BytesIO()
            fig.savefig(myBuffer, format="png")
            myBuffer.seek(0)
            image = base64.b64encode(myBuffer.getvalue()).decode("utf-8")
            plt.close(fig)
            myBuffer.close()
            return image
    
    def compToIdealTemperature(self, plantId):
        query = ("""
         SELECT PlantSpecies
         FROM Plants
         WHERE PlantID = ?
         """)
        self.dbHandler.cursor.execute(query, (plantId,))
        result = self.dbHandler.cursor.fetchall()
        if not result:
            return self._errorImage("Plant not Found!")
        species = result[0][0] #First Field First Column
        
        reccValue = self._dataLookup(species, Measurement.TEMPERATURE)

        if(reccValue == "N/A Species"):
            return self._errorImage("Plant not found!")
        else:
            reccValue = float(reccValue)
            query2 = ("""SELECT AVG(Temperature) FROM Recordings WHERE PlantID = ?""")
            self.dbHandler.cursor.execute(query2, (plantId,))
            averageValue = self.dbHandler.cursor.fetchall()[0][0]

            dataF = pd.DataFrame({"Type": ["Reccomended", "Average"], "Value": [reccValue, averageValue]})
            fig, ax = plt.subplots()
            sns.barplot(data=dataF, x="Type", y= "Value",ax=ax)
            ax.set_title("Recorded Average vs Reccomended Temperature Value")
            ax.set_xlabel("Reccomended vs Recorded Average")
            ax.set_ylabel("Value")
            plt.xticks(rotation=45)
            fig.tight_layout()
            myBuffer = io.BytesIO()
            fig.savefig(myBuffer, format="png")
            myBuffer.seek(0)
            image = base64.b64encode(myBuffer.getvalue()).decode("utf-8")
            plt.close(fig)
            myBuffer.close()
            return image

    def _dataLookup(self, species, measurementType):
        species = species.strip().upper()
        if self.speciesData.get(species) is  None:
            return "N/A Species"
        elif (measurementType == Measurement.TEMPERATURE):
            return self.speciesData[species]["IdealTemperature"]
        elif (measurementType == Measurement.HUMIDITY):
            return self.speciesData[species]["IdealHumidity"]
        
    def _errorImage(self, message):
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=12, color="red")
        ax.axis("off")
        myBuffer = io.BytesIO()
        fig.savefig(myBuffer, format="png")
        myBuffer.seek(0)
        image = base64.b64encode(myBuffer.getvalue()).decode("utf-8")
        plt.close(fig)
        myBuffer.close()
        return image
