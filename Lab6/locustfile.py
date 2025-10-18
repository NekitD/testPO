from locust import HttpUser, task

class openBmcTester(HttpUser):
    
    api_url = 'https://127.0.0.1:2443'

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task(1)
    def sys_info(self):
        try:
            response = self.client.get(self.api_url + 'Systems/system')
            data = response.json()
            has_Status = 'Status' in data
            has_Power = 'PowerState' in data
            if(not has_Status): print("NO STATUS")
            if(not has_Power): print("NO POWER")
            return response != None and has_Status and has_Power
        except:
            print("API DOESN'T ANSWER")
 
    @task(2)
    def power_info(self):
        try:
            response = self.client.get(self.api_url + 'Systems/system')
            data = response.json()

            try:
                power = data('PowerState')
            except:
                print("THERE'S NO FIELD PowerState in the API") 

            return (power != None)
        except:
            print("API DOESN'T ANSWER")