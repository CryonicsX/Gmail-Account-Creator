from src.snippets import CLI
from urllib.request import urlopen
import random, string, sys, threading


from src.worker.generator import worker


ua = open("./config/useragents.txt", "+r", encoding="utf-8").read().splitlines()

def get_name():
    x = urlopen("https://raw.githubusercontent.com/CryonicsX/SpotifyStreamBot/main/x.txt")
    a = x.read().splitlines()
    return random.choice(a).decode("utf-8")


def get_random_string(length):  # Letters and numbers
    pool = string.ascii_lowercase + string.digits
    return "".join(random.choice(pool) for _ in range(length))

class Igniter:
    def __init__(self, config, proxies = None) -> None:
        self.proxies = proxies
        self.config = config

        self.count = self.config["account_count"]
        self.thread = self.config["browser_thread"]
        self.remaining = self.config['account_count']
        self.CLI = CLI(self.thread)

        if proxies:
            self.proxies = proxies[0]


    def thread_function(self, thread_id):
        while self.remaining > 0:
            
            full_name = [get_name(), get_name()]


            data = None
            data = worker(full_name, f"{full_name[0]}{full_name[1]}{random.randint(1,999)}", get_random_string(12), random.choice(ua), self.config["api_key"], self.CLI, thread_id, random.choice(self.proxies) if self.proxies else None).create_account()

            if data:
                self.remaining -= data 
            else:
                pass

        for thread_id in range(0, self.thread):
            self.CLI.set(index=thread_id, status='Completed.')
            
        sys.exit()



    def thread_base(self):
        threads = []
        for thread_id in range(0, self.thread):
            t = threading.Thread(target=self.thread_function, daemon=True, args=(thread_id,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def main(self):
        self.thread_base()

    
    