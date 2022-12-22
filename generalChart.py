# libraries
import re
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
rutaRegistros = "/home/user/Escritorio/Registro_datos" + "/"
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


####################### Grafico #######################

# Make a data frame
'''
for columna in listaSeveridad:
    dicColum = {'low': columna[0], 'medium':columna[1], 'high': columna[2], 'critic':columna[3]}


    
df=pd.DataFrame({'x': range(1,11), 'y1': np.random.randn(10), 'y2': np.random.randn(10)+range(1,11), 'y3': np.random.randn(10)+range(11,21), 'y4': np.random.randn(10)+range(6,16)})
 
# Change the style of plot
plt.style.use('seaborn-darkgrid')
 
# Create a color palette
palette = plt.get_cmap('Set1')
 
# Plot multiple lines
num=0
for column in df.drop('x', axis=1):
    num+=1
    plt.plot(df['x'], df[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)

# Add legend
plt.legend(loc=2, ncol=2)
 
# Add titles
plt.title("A (bad) Spaghetti plot", loc='left', fontsize=12, fontweight=0, color='orange')
plt.xlabel("Time")
plt.ylabel("Score")

# Show the graph
plt.show()



plt.xlim(0,20) #El eje X es el unico fijo
#for i in range(0,20,1):
i = 0
for colum in fileList:
    i = i+1
    for j in range(0,len(colum),1):
        plt.plot(i,colum[j],color="red",linewidth=2.0)

plt.show()
'''