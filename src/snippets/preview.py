import os

class Colors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BACK = '\033[1A'

class Preview:
    def __init__(self, config, proxies_amount):
        self.colors = Colors()
        self.config = config
        self.proxies_amount = proxies_amount
        self.size = os.get_terminal_size().columns

        os.system('cls' if os.name == 'nt' else 'clear')
        input(f"""  __________  ____   __________  __
 / ___/ __/ |/ / /  /  _/ __/\ \/ /
/ (_ / _//    / /___/ // _/   \  / 
\___/___/_/|_/____/___/_/     /_/  

[{self.colors.MAGENTA}#{self.colors.RESET}] discord.gg/genlify

[{self.colors.MAGENTA}#{self.colors.RESET}] Made by Genlify
                                   
[{self.colors.MAGENTA}#{self.colors.RESET}] SETTINGS:
[{self.colors.MAGENTA}>{self.colors.RESET}] Threads: {self.config['browser_thread']}
[{self.colors.MAGENTA}>{self.colors.RESET}] Use Proxy: {self.config['use_proxy']}
{f"[{self.colors.MAGENTA}>{self.colors.RESET}] Proxy Protocol: {self.config['proxy_protocol']}" if self.config['use_proxy'] else f"{self.colors.BACK}"}
{f"[{self.colors.MAGENTA}>{self.colors.RESET}] Working Proxy Amount: {self.proxies_amount[0]}" if self.config['use_proxy'] else f"{self.colors.BACK}"}

[{self.colors.MAGENTA}>{self.colors.RESET}] Press "Enter" to continue.""")
