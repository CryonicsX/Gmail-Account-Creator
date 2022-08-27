import os, sys, datetime, time

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


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Booter:
    def __init__(self):
        self.colors = Colors()
        clear()
        os.system('title Genlify - Gmail Account Creator')

    def set(self, arg, type=None):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if type is None:
            print(f'{self.colors.YELLOW}[Boot][{current_time}]{self.colors.RESET} {arg}')
        elif type == 'ERROR':
            print(f'{self.colors.RED}[Error][{current_time}]{self.colors.RESET} {arg}')
            sys.exit()


def prepare(each):
    data = []
    for thread_raw in range(each):
        data.append(
            {
                'thread': {
                    'id': thread_raw + 1,
                    'status': 'Initiating',
                    'Total_Creating': 0,
                    'error': 0
                }
            }
        )
    return data


lock = False


class CLI:
    def __init__(self, each):
        self.data = prepare(each)
        print(self.data)
        self.colors = Colors()
        self.total_created = 0
        self.total_error = 0

    def render(self):
        global lock
        if not lock:
            lock = True
            clear()
            print(f'Thread status:')
            print(f"[ALL] | {self.colors.UNDERLINE}{'Working'}{self.colors.RESET} | {self.colors.GREEN}Created:{self.colors.RESET} {self.total_created} - {self.colors.RED}Errors:{self.colors.RESET} {self.total_error}")
            for data in self.data:
                if data['thread']['id'] < 10:
                    print(f"[00{data['thread']['id']}] | {self.colors.UNDERLINE}{data['thread']['status']}{self.colors.RESET} | {self.colors.GREEN}Creating:{self.colors.RESET} {data['thread']['Total_Creating']} - {self.colors.RED}Errors:{self.colors.RESET} {data['thread']['error']}")
                elif data['thread']['id'] < 100:
                    print(f"[0{data['thread']['id']}] | {self.colors.UNDERLINE}{data['thread']['status']}{self.colors.RESET} | {self.colors.GREEN}Creating:{self.colors.RESET} {data['thread']['Total_Creating']} - {self.colors.RED}Errors:{self.colors.RESET} {data['thread']['error']}")
                elif data['thread']['id'] < 1000:
                    print(f"[{data['thread']['id']}] | {self.colors.UNDERLINE}{data['thread']['status']}{self.colors.RESET} | {self.colors.GREEN}Creating:{self.colors.RESET} {data['thread']['Total_Creating']} - {self.colors.RED}Errors:{self.colors.RESET} {data['thread']['error']}")
            lock = False

    def set(self, index, creating=None, status=None, error=None):
        if status:
            self.data[index]['thread']['status'] = status
        
        if creating:
            self.data[index]['thread']['Total_Creating'] += 1
            self.total_created += 1
        
        if error:
            self.data[index]['thread']['error'] += 1
            self.total_error += 1
        self.render()

