from cProfile import label
import subprocess
import matplotlib.pyplot as plot
import numpy as np
import matplotlib.patches as mpatches

class Valorador_riesgo:
    def azul():
        return "blue"

    def amarillo():
        return "yellow"

    def marron():
        return "brown"

    def rojo():
        return "red"

    switchSeveridad = {
        "Low": azul,
        "Medium": amarillo,
        "High": marron,
        "Critical": rojo,
    }

    def aplicarFormula(self,rutaRegistros, vulnerabilidad):
        factorTiempo = 0
        impacto = float(vulnerabilidad.impacto)
        numRepeticiones = self.consultarRegistroRiesgos(rutaRegistros,vulnerabilidad)

        if impacto >= 9.0: #Riesgo considerado critico
            if numRepeticiones <=10: 
                resta = 10 - impacto
                porcentaje = resta / 10
                factorTiempo = porcentaje * numRepeticiones
                valorVulnerabilidad = impacto + factorTiempo
            else:
                valorVulnerabilidad = 10
        else:
            valorCVSS = impacto * 0.8
            factorTiempo = 0
            if numRepeticiones <= 20: #20 como numero de referencia en el que se hace al menos 1 analisis por dia
                factorTiempo = numRepeticiones * 0.1
            else: #Si satura por encima de 20 porque se han hecho mas de 20 analisis en 20 dias, entonces acotar a 2 puntos como maximo
                factorTiempo = 2
            valorVulnerabilidad = valorCVSS + factorTiempo
        return str(valorVulnerabilidad)

    def consultarRegistroRiesgos(self,rutaRegistros,vulnerabilidad):
        rutaRegistros = rutaRegistros + "/"
        procesoFind = subprocess.run(["find", rutaRegistros, "-type", "f", "-ctime" ,"-20"], capture_output=True,text=True) #Saca los registros de vulnerabilidades de los ultimos 20 dias
        registrosVulnerabilidades = procesoFind.stdout.splitlines()
        contador_vulnerabilidad = 0

        if len(registrosVulnerabilidades) != 0: 
            for rutaFichero in registrosVulnerabilidades:  #Recorrer los registros vulnerabilidades de los ultimos 20 dias
                fichero = open(rutaFichero,"r")
                procesoGrepMac = subprocess.run(['grep', vulnerabilidad.hostname, rutaFichero],capture_output=True,text=True)
                hayMac= procesoGrepMac.stdout.splitlines()
                
                if len(hayMac) != 0:
                    hayMacPartido = hayMac[0].split(';')
                    repeticion = hayMacPartido[1]
                    procesoGrepMac = subprocess.run(['grep', vulnerabilidad.hostname, "-A", repeticion, rutaFichero],capture_output=True,text=True)
                    lineasVuln= procesoGrepMac.stdout.splitlines()
                    for vulnerability in lineasVuln:
                        vul = vulnerabilidad.nombreVulnerabiliad + ";" + vulnerabilidad.protocoloYpuerto
                        if vul in vulnerability:
                            contador_vulnerabilidad+=1
                fichero.close()

        return contador_vulnerabilidad

    def revaluarSeveridad(self, valorVulneravilidad):
        if valorVulneravilidad < 5.0:
            return "Low"
        elif valorVulneravilidad < 7.0:
            return "Medium"
        elif valorVulneravilidad < 9.0:
            return "High"
        else:
            return "Critical"

    def dibujarMatriz(self,matrizX,matrizY, mac, ip,severidad,rutaMatrizRiesgos):
            plot.ylim(0,10) #El eje Y es el unico fijo
            for i in range(0,len(matrizX),1):
                plot.scatter(matrizX[i],matrizY[i],marker="o",color=self.switchSeveridad.get(severidad[i])()) #cada vulnerabilidad se pinta segun su severidad
            plot.xlabel("Number of the risk")
            plot.ylabel("Range 0 to 10")
            plot.title("Device: " + mac + ";" + ip)
            
            #Incluir leyenda
            leyendaAzul = mpatches.Patch(color="blue",label="Low")
            leyendaAmarillo = mpatches.Patch(color="yellow",label="Medium")
            leyendaMarron = mpatches.Patch(color="brown",label="High")
            leyendaRoja = mpatches.Patch(color="red",label="Critical")

            plot.legend(handles=[leyendaAzul,leyendaAmarillo,leyendaMarron,leyendaRoja],loc="best") #Se coloca automaticamente en la mejor posicion sin cortar los datos
            plot.savefig(rutaMatrizRiesgos + "/Matriz de riesgos: " + mac + ";" + ip + ".png")
            plot.close() #Limpia el grafico para que no se superponga cada vez que se pinta una matriz

    def valoracionRiesgo(self,conjuntoTarget,rutaMatrizRiesgos,rutaRegistros):

        for target in conjuntoTarget:
            if len(target.listaVulnerabilidades) > 0: #Comprobar que ese target tiene al menos una vulnerabilidad en la lista
                numVulnerabilidad = 0
                matrizX = list()
                matrizY = list()
                listaSeveridad = list()
                for vulnerabilidad in target.listaVulnerabilidades:
                    valorVulneravilidad = self.aplicarFormula(rutaRegistros, vulnerabilidad) 
                    vulnerabilidad.impacto = valorVulneravilidad #Cambio del impacto como riesgo
                    vulnerabilidad.severidad = self.revaluarSeveridad(float(valorVulneravilidad)) #Para saber si ha sido bajo, medio, alto o critico de forma cualitativa tambien
                    matrizX.append(numVulnerabilidad) #Se guarda la coordenada X como el numero de vulnerabilidad
                    matrizY.append(float(valorVulneravilidad)) #Se guarda la coordenada Y como el impacto final
                    listaSeveridad.append(vulnerabilidad.severidad) #Se guarda la severidad en orden por cada impacto final
                    numVulnerabilidad +=1
                self.dibujarMatriz(matrizX,matrizY,target.mac,target.ip,listaSeveridad,rutaMatrizRiesgos) #Dibuja la matriz de los target que tienen vulnerabilidades
        return conjuntoTarget