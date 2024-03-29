# libraries
from datetime import datetime
import math
import re
import subprocess
import matplotlib.pyplot as plt

class General_Chart:
    def generateChart(self, rutaRegistros, rutaInformeActual):
        rutaRegistros = rutaRegistros + "/"
        procesoFind = subprocess.Popen(["find", rutaRegistros, "-type", "f", "-ctime" ,"-20"], stdout=subprocess.PIPE) #Saca los registros de vulnerabilidades de los ultimos 20 dias
        procesoSort = subprocess.Popen("sort", stdin=procesoFind.stdout, stdout=subprocess.PIPE) 
        procesoTail = subprocess.run(["tail","-20"], stdin=procesoSort.stdout, capture_output=True,text=True)
        registrosVulnerabilidades = procesoTail.stdout.splitlines()

        fileList= list()
        if len(registrosVulnerabilidades) != 0: 
            for rutaFichero in registrosVulnerabilidades:  #Recorrer los registros vulnerabilidades de los ultimos 20 dias
                fichero = open(rutaFichero,"r")
                listaSeveridad = [0,0,0,0] #low[0], medium[1], high[2] y critic[3]
                for lineaFichero in fichero:
                    #00:00:00:00:00:04;5
                    mac = re.match('[A-Z0-9][A-Z0-9]:[A-Z0-9][A-Z0-9]:[A-Z0-9][A-Z0-9]:[A-Z0-9][A-Z0-9]:[A-Z0-9][A-Z0-9]:[A-Z0-9][A-Z0-9];[A-Z0-9]+', lineaFichero)
                    hayMac = bool(mac)

                    if hayMac == False:
                        #Meter patron vulnerabilidad para eliminar la cabecera
                        lineaPartida = lineaFichero.split(';')
                        severity = lineaPartida[2]

                        if severity == "Low\n":
                            valor = listaSeveridad[0]
                            valor = valor +1
                            listaSeveridad[0] = valor
                        elif severity == "Medium\n":
                            valor = listaSeveridad[1]
                            valor = valor +1
                            listaSeveridad[1] = valor
                        elif severity == "High\n":
                            valor = listaSeveridad[2]
                            valor = valor +1
                            listaSeveridad[2] = valor
                        elif severity == "Critical\n":
                            valor = listaSeveridad[3]
                            valor = valor +1
                            listaSeveridad[3] = valor
                fileList.append(listaSeveridad)
                fichero.close()


        ####################### Chart #######################
        ylow = list()
        ymedium = list()
        yhigh = list()
        ycritic = list()
        xDays = list()
        contador = 1
        for fichero in fileList:
            ylow.append(fichero[0])
            ymedium.append(fichero[1])
            yhigh.append(fichero[2])
            ycritic.append(fichero[3])
            xDays.append(contador)
            contador = contador + 1

        plt.plot(xDays, ylow, color='blue', linestyle='dashed', linewidth = 2, marker='o', markerfacecolor='cyan', markersize=8, label = 'Low')

        plt.plot(xDays, ymedium, color='yellow', linestyle='dashed', linewidth = 2, marker='o', markerfacecolor='black', markersize=8, label = 'Medium')

        plt.plot(xDays, yhigh, color='brown', linestyle='dashed', linewidth = 2, marker='o', markerfacecolor='white', markersize=8, label = 'High')

        plt.plot(xDays, ycritic, color='red', linestyle='dashed', linewidth = 2, marker='o', markerfacecolor='magenta', markersize=8, label = 'Critical')
        
        #Change axis x and y from decimal to integer
        elemMax = max(fileList)
        maximo = max(elemMax)
        xInteger = range(1, math.ceil(max(xDays))+1)
        plt.xticks(xInteger)
        
        yInteger = maximo + 1
        plt.ylim([0, yInteger])

        # naming the x axis
        plt.xlabel('Days')
        # naming the y axis
        plt.ylabel('Risk number')
        # giving a title to my graph
        plt.title('Chart of the last 20 days')

        # show a legend on the plot
        plt.legend()

        # function to save the plot
        now = datetime.now()
        current_date = now.date()
        name = f"General_chart_{current_date}"
        plt.savefig(rutaInformeActual + "/" + name + ".png")
