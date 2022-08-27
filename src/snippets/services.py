import requests, time

class smsactive:
    
    def __init__(self, apikey: str, proxy: str = None) -> None:
        self.apikey = apikey
        self.proxy = proxy
        self.session = requests.Session()
        self.session.proxies.update(proxy) if proxy else ""
        self.id = None
        self.country = "62"
        self.service = "go"

    def get_number(self) -> dict:
        try:
            response = self.session.get(f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.apikey}&action=getNumber&service={self.service}&ref=1715152&country={self.country}").text
            
            if ":" not in response:
                return {"error": 1}
            
            self.id = response.split(":")[1]
            self.number = response.split(":")[2]
            return {"error": 0, "number": self.number, "proc_id": self.id}
        
        except:
            return {"error": 1}

    def sent(self, id: str) -> dict:
        try:
            self.session.get(f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.apikey}&action=setStatus&status=1&id={id}")
            return {"error": 0}
        except:
            return {"error": 1}

    def done(self, id: str):
        try:
            self.session.get(f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.apikey}&action=setStatus&status=6&id={id}")
            return {"error": 0}
        except:
            return {"error": 1}

    def delete_number(self, id: str) -> dict:
        try:
            self.session.get(f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.apikey}&action=setStatus&status=8&id={id}")
            return {"error": 0}
        except:
            return {"error": 1}

    def check_inbox(self, id: str) -> dict:
        try:
            response = self.session.get(f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.apikey}&action=getStatus&id={id}").text
            if "STATUS_OK" not in response:
                return {"error": 1}

            return {"error": 0, "code": response.split(":")[1]}

        except Exception as e:
            return {"error": 1, "desc": e}

    def wait_for_code(self, id: str) -> dict:
        self.sent(id)
        tries = 0
        while tries < 23:
            time.sleep(2)
            value = self.check_inbox(id)
            if value["error"] != 1:
                self.done(id)
                return {"error": 0, "code": value}
            tries += 1
        self.delete_number(id)
        return {"error": 1}
