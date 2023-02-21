import json


class Generador_informe:

    def generarInforme(self,conjuntoTarget,rutaInformeActual):

        informe = {}

        for target in conjuntoTarget:
            if len(target.listaVulnerabilidades) > 0: #Solo sacar en el informe los target que tienen vulnerabilidades
                
                dicVulnerabilidades = {}
                #Recorrer la lista de vulnerabilidades y hacer un diccionario con los datos de cada vulnerabilidad
                for vulnerabilidad in target.listaVulnerabilidades:
                    dicVulnerabilidades[vulnerabilidad.nombreVulnerabiliad] = ({
                        "Name of the risk" : vulnerabilidad.nombreVulnerabiliad,
                        "Port and protocol" : vulnerabilidad.protocoloYpuerto,
                        "Value" : vulnerabilidad.impacto,
                        "Severity" : vulnerabilidad.severidad,
                        "List of CVEs" : vulnerabilidad.cves,
                        "Solution" : vulnerabilidad.solucion,
                        "Result" : vulnerabilidad.resultado,
                        "Summary" : vulnerabilidad.resumen,
                    })
                #Rellenar el informe
                informe[target.mac + ";" + target.ip] = []
                informe[target.mac + ";" + target.ip] = ({
                    "MAC" : target.mac,
                    "IP" : target.ip,
                    "Risk list": dicVulnerabilidades
                })

        #Guardar informe
        with open(rutaInformeActual +'/Informe.json', 'w') as file:
            json.dump(informe, file, indent=4)