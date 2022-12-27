# libraries
from datetime import datetime
import re
import subprocess
import matplotlib.pyplot as plt

class General_Chart:
    def generateChart(self, rutaRegistros, rutaInformeActual):
        rutaRegistros = rutaRegistros + "/"
        procesoFind = subprocess.run(["find", rutaRegistros, "-type", "f", "-ctime" ,"-20"], capture_output=True,text=True) #Saca los registros de vulnerabilidades de los ultimos 20 dias
        registrosVulnerabilidades = procesoFind.stdout.splitlines()

        fileList= list()
        if len(registrosVulnerabilidades) != 0: 
            for rutaFichero in registrosVulnerabilidades:  #Recorrer los registros vulnerabilidades de los ultimos 20 dias
                fichero = open(rutaFichero,"r")
                listaSeveridad = [0,0,0,0] #low[0], medium[1], high[2] y critic[3]
                for lineaFichero in fichero:
                    #00:00:00:00:00:04;5
                    mac = re.match('[0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9];[0-9]+', lineaFichero)
                    hayMac = bool(mac)

                    if hayMac == False:
                        #Meter patron vulnerabilidad para eliminar la cabecera
                        lineaPartida = lineaFichero.split(';')
                        severity = lineaPartida[2]

                        if severity == "low\n":
                            valor = listaSeveridad[0]
                            valor = valor +1
                            listaSeveridad[0] = valor
                        elif severity == "medium\n":
                            valor = listaSeveridad[1]
                            valor = valor +1
                            listaSeveridad[1] = valor
                        elif severity == "high\n":
                            valor = listaSeveridad[2]
                            valor = valor +1
                            listaSeveridad[2] = valor
                        elif severity == "critic\n":
                            valor = listaSeveridad[3]
                            valor = valor +1
                            listaSeveridad[3] = valor
                fileList.append(listaSeveridad)
                fichero.close()


        ####################### Chart #######################

        xlow = list()
        ylow = list()
        contador = 0
        for fichero in fileList:
            ylow.append(fichero[0])
            xlow.append(contador)
            contador = contador + 1

        # plotting the line 1 points
        plt.plot(xlow, ylow, color='blue', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='cyan', markersize=12, label = 'Low')

        xmedium = list()
        ymedium = list()
        contador = 0
        for fichero in fileList:
            ymedium.append(fichero[1])
            xmedium.append(contador)
            contador = contador + 1

        # plotting the line 2 points
        plt.plot(xmedium, ymedium, color='yellow', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='black', markersize=12, label = 'Medium')

        xhigh = list()
        yhigh = list()
        contador = 0
        for fichero in fileList:
            yhigh.append(fichero[2])
            xhigh.append(contador)
            contador = contador + 1

        # plotting the line 3 points
        plt.plot(xhigh, yhigh, color='brown', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='white', markersize=12, label = 'High')

        xcritic = list()
        ycritic = list()
        contador = 0
        for fichero in fileList:
            ycritic.append(fichero[3])
            xcritic.append(contador)
            contador = contador + 1

        # plotting the line 4 points
        plt.plot(xcritic, ycritic, color='red', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='magenta', markersize=12, label = 'Critic')

        # naming the x axis
        plt.xlabel('Days')
        # naming the y axis
        plt.ylabel('Num.Vulnerabilities')
        # giving a title to my graph
        plt.title('Chart of the last 20 days')

        # show a legend on the plot
        plt.legend()

        # function to save the plot
        now = datetime.now()
        current_date = now.date()
        name = f"General_chart_{current_date}"
        plt.savefig(rutaInformeActual + "/" + name + ".png")
