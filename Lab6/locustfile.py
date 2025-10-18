from locust import HttpUser, task
from requests.auth import HTTPBasicAuth

class openBmcTester(HttpUser):
    
    host = 'https://127.0.0.1:2443'
    auth = HTTPBasicAuth('root', '0penBmc')

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task(1)
    def sys_info(self):
        try:
            response = self.client.get('/redfish/v1/Systems/system', auth=self.auth, verify= False)
            data = response.json()
            has_Status = 'Status' in data
            has_Power = 'PowerState' in data
            if(not has_Status): print("NO STATUS")
            if(not has_Power): print("NO POWER")
            return response != None and has_Status and has_Power
        except Exception:
            print("API DOESN'T ANSWER")
            return False
 
    @task(2)
    def power_info(self):
        try:
            response = self.client.get(self.host + '/redfish/v1/Systems/system', auth=self.auth, verify= False)
            data = response.json()

            try:
                power = data('PowerState')
            except Exception:
                print("THERE'S NO FIELD PowerState in the API")
                return False 

            return (power != None)
        except Exception:
            print("API DOESN'T ANSWER")
            return False
        


class shikimoriTester(HttpUser):
    host = 'https://shikimori.one/NekitD'
    auth = HTTPBasicAuth('NekitD', 'rfgbnjirf88')
    
    def on_start(self):
        pass

    def on_stop(self):
        pass
    
    @task(1)
    def anime_list(self):
        try:
            response = self.client.get('/list/anime?order=name', auth=self.auth, verify= False)
            data = response.json()
            has_Name = 'name' in data
            has_Rate = 'rate_score' in data
            has_Eps = 'episodes' in data
            has_Kind = 'kind' in data
            if(not has_Name): print("LIST: NO NAME")
            if(not has_Rate): print("LIST: NO RATE SCORE")
            if(not has_Eps): print("LIST: NO EPISODES")
            if(not has_Kind): print("LIST: NO KIND")
            return response != None and has_Name and has_Kind and has_Eps and has_Rate
        except Exception:
            print("API DOESN'T ANSWER")
            return False
    
    @task(2)
    def get_first(self):
        try:
            response = self.client.get('/list/anime?order=name', auth=self.auth, verify= False)
            data = response.json()
            first = data[0]
            has_Name = 'name' in first
            has_Rate = 'rate_score' in first
            has_Eps = 'episodes' in first
            has_Kind = 'kind' in first
            if(not has_Name): print("FIRST: NO NAME")
            if(not has_Rate): print("FIRST: NO RATE SCORE")
            if(not has_Eps): print("FIRST: NO EPISODES")
            if(not has_Kind): print("FIRST: NO KIND")

            if(first['name'] == "Аля иногда кокетничает со мной по-русски"): return True
            else: return False
            
        except Exception:
            print("API DOESN'T ANSWER")
            return False

