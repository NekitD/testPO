from locust import HttpUser, task, between
# from requests.auth import HTTPBasicAuth

class openBmcTester(HttpUser):
    
    host = 'https://127.0.0.1:5555'
    #auth = HTTPBasicAuth('root', '0penBmc')

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task(1)
    def sys_info(self):
        try:
            response = self.client.get('/redfish/v1/Systems/system', verify= False)
            data = response.json()
            has_Status = 'Status' in data
            has_Power = 'PowerState' in data
            if(not has_Status): print("NO STATUS")
            if(not has_Power): print("NO POWER")
            return response != None and has_Status and has_Power
        except Exception:
            print("OpenBMC API DOESN'T ANSWER")
            return False
 
    @task(2)
    def power_info(self):
        try:
            response = self.client.get(self.host + '/redfish/v1/Systems/system', verify= False)
            data = response.json()

            try:
                power = data('PowerState')
            except Exception:
                print("THERE'S NO FIELD PowerState in the API")
                return False 

            return (power != None)
        except Exception:
            print("OpenBMC API DOESN'T ANSWER")
            return False
        
