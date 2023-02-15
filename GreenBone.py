import time, requests,re
from datetime import datetime
class GreenBone:

    def launch(self,ipList,carpetaEntrada,user,password):
        sesion = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'multipart/form-data; boundary=---------------------------301933276242805150541672282389',
            'Origin': 'http://localhost:9392',
            'Connection': 'keep-alive',
            'Referer': 'http://localhost:9392/login',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        data = '-----------------------------301933276242805150541672282389\r\nContent-Disposition: form-data; name="cmd"\r\n\r\nlogin\r\n-----------------------------301933276242805150541672282389\r\nContent-Disposition: form-data; name="login"\r\n\r\n' + user + '\r\n-----------------------------301933276242805150541672282389\r\nContent-Disposition: form-data; name="password"\r\n\r\n' + password + '\r\n-----------------------------301933276242805150541672282389--\r\n'

        login = sesion.post('http://localhost:9392/gmp', headers=headers, data=data)
        cookieGSAD_SID = login.cookies.values()[0]

        aux = re.findall('<token>.*</token>', login.text)[0]
        token = aux[7:-8]

        ########################### CREATE TARGET ##############################
        
        # current datetime
        now = datetime.now()
        current_date = now.date()
        targetList = ",".join(ipList) #FIXME Aqui hay target solo, hay que tener la lista de IPs
        #timeLaunch = {time.strftime('%Y/%m/%d-%H:%M')}
        targetName = f"Automatic_target_list_{current_date}"

        cookies = {
            'GSAD_SID': cookieGSAD_SID,
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'multipart/form-data; boundary=---------------------------407286562837231475611015594514',
            'Origin': 'http://localhost:9392',
            'Connection': 'keep-alive',
            'Referer': 'http://localhost:9392/targets',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        data = '-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="token"\r\n\r\n' + token + '\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="cmd"\r\n\r\ncreate_target\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="name"\r\n\r\n' + targetName + '\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="comment"\r\n\r\n\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="allow_simultaneous_ips"\r\n\r\n1\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="target_source"\r\n\r\nmanual\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="target_exclude_source"\r\n\r\nmanual\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="hosts"\r\n\r\n' + targetList + '\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="exclude_hosts"\r\n\r\n\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="reverse_lookup_only"\r\n\r\n0\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="reverse_lookup_unify"\r\n\r\n0\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="port_list_id"\r\n\r\n730ef368-57e2-11e1-a90f-406186ea4fc5\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="alive_tests"\r\n\r\nScan Config Default\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="port"\r\n\r\n22\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="ssh_credential_id"\r\n\r\n0\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="ssh_elevate_credential_id"\r\n\r\n0\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="smb_credential_id"\r\n\r\n0\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="esxi_credential_id"\r\n\r\n0\r\n-----------------------------407286562837231475611015594514\r\nContent-Disposition: form-data; name="snmp_credential_id"\r\n\r\n0\r\n-----------------------------407286562837231475611015594514--\r\n'

        createTargetResponse = requests.post('http://localhost:9392/gmp', cookies=cookies, headers=headers, data=data)

        aux = re.findall('<id>.*</id>', createTargetResponse.text)[0]
        idTarget = aux[4:-5]

        ########################### CREATE TASK ##############################

        taskName = f"Automatic_task{current_date}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'multipart/form-data; boundary=---------------------------279714327121866409512607194662',
            'Origin': 'http://localhost:9392',
            'Connection': 'keep-alive',
            'Referer': 'http://localhost:9392/tasks',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        data = '-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="token"\r\n\r\n' + token + '\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="cmd"\r\n\r\ncreate_task\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="add_tag"\r\n\r\n0\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="alterable"\r\n\r\n0\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="apply_overrides"\r\n\r\n1\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="auto_delete"\r\n\r\nno\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="auto_delete_data"\r\n\r\n5\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="comment"\r\n\r\n\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="config_id"\r\n\r\ndaba56c8-73ec-11df-a475-002264764cea\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="hosts_ordering"\r\n\r\nsequential\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="in_assets"\r\n\r\n1\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="max_checks"\r\n\r\n4\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="max_hosts"\r\n\r\n20\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="min_qod"\r\n\r\n70\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="name"\r\n\r\n' + taskName + '\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="scanner_id"\r\n\r\n08b69003-5fc2-4037-a479-93b440211c73\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="scanner_type"\r\n\r\n2\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="schedule_id"\r\n\r\n0\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="schedule_periods"\r\n\r\n0\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="target_id"\r\n\r\n' + idTarget + '\r\n-----------------------------279714327121866409512607194662\r\nContent-Disposition: form-data; name="usage_type"\r\n\r\nscan\r\n-----------------------------279714327121866409512607194662--\r\n'

        createTask = requests.post('http://localhost:9392/gmp', cookies=cookies, headers=headers, data=data)

        aux = re.findall('<id>.*</id>', createTask.text)[0]
        idTask = aux[4:-5]

        ########################### START TASK ##############################

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'multipart/form-data; boundary=---------------------------279651218819391665603089766527',
            'Origin': 'http://localhost:9392',
            'Connection': 'keep-alive',
            'Referer': 'http://localhost:9392/tasks',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        data = '-----------------------------279651218819391665603089766527\r\nContent-Disposition: form-data; name="token"\r\n\r\n' + token + '\r\n-----------------------------279651218819391665603089766527\r\nContent-Disposition: form-data; name="cmd"\r\n\r\nstart_task\r\n-----------------------------279651218819391665603089766527\r\nContent-Disposition: form-data; name="task_id"\r\n\r\n' + idTask + '\r\n-----------------------------279651218819391665603089766527--\r\n'

        startTask = requests.post('http://localhost:9392/gmp', cookies=cookies, headers=headers, data=data)

        ##################################### GET STATUS ###################################

        done = 0

        while done == 0:
            time.sleep(240) #4 minutos #puedo hacer el tiempo variable en funcion del porcentaje de completado que lleve el analisis
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
                'Accept': '*/*',
                'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                'Connection': 'keep-alive',
                'Referer': 'http://localhost:9392/tasks',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
            }

            params = {
                'token': token,
                'cmd': 'get_task',
                'task_id': idTask,
            }

            getStatus = requests.get('http://localhost:9392/gmp', params=params, cookies=cookies, headers=headers)


            aux = re.findall('<status>.*</status>', getStatus.text)[0]
            status = aux[8:-9]

            if status == "Done":
                print("Vulnerability analisys done")
                done=1

        aux = re.findall('report id=.[a-zA-Z_0-9]*-[a-zA-Z_0-9]*-[a-zA-Z_0-9]*-[a-zA-Z_0-9]*-[a-zA-Z_0-9]*', getStatus.text)[0]
        idReport = aux[11:]

        ######################### DESCARGAR INFORME #########################

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'http://127.0.0.1:9392/report/'+idReport,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        params = {
            'token': token,
            'cmd': 'get_report',
            'details': '1',
            'report_id': idReport,
            'report_format_id': 'c1645568-627a-11e3-a660-406186ea4fc5',
            'filter': 'apply_overrides=0 levels=hml rows=-1 min_qod=70 first=1 sort-reverse=severity notes=1 overrides=1',
        }

        getReport = requests.get('http://127.0.0.1:9392/gmp', params=params, cookies=cookies, headers=headers)

        route = carpetaEntrada + '/Reporte_greenbone.csv'
        informeCSV = open(route, 'w')
        informeCSV.write(getReport.text)
        informeCSV.close
        return route
