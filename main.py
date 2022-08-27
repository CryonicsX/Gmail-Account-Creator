from src.snippets import Booter, Reader, Proxy, Preview
from src.igniter import Igniter


class Main:
    def __init__(self):
        # INIT BOOTER
        self.booter = Booter()

        # CONFIG
        self.booter.set('Reading config.')
        self.config = Reader().read()
        if not self.config[0]:
            self.booter.set(self.config[1], 'ERROR')
        if self.config[1]:
            self.config = self.config[1]

        '''
        # LICENSE CHECKER
        self.booter.set('Checking license.')
        self.license = License(self.config).check()
        if not self.license[0]:
            self.booter.set(self.license[1], 'ERROR')
        '''

        # PROXY CHECKER
        self.proxy_amount = [0]
        self.proxies = None
        if not self.config['use_proxy']:
            self.booter.set('Passed proxy checking.')
        else:
            self.booter.set('Checking proxies.')
            self.proxies = Proxy(self.config).check_proxies()
            if not self.proxies[0]:
                self.booter.set(self.proxies[1], 'ERROR')
            if self.proxies[1]:
                self.booter.set(f'Proxies checked.')
                if self.config['use_proxy']:
                    self.booter.set(f'{self.proxies[2]} working proxies.')
                self.proxy_amount = [self.proxies[2]]
                self.temp_proxies = [self.proxies[1]]
                self.proxies = []
                self.proxies = self.temp_proxies.copy()

        # PREVIEW
        Preview(config=self.config, proxies_amount=self.proxy_amount)

    def main(self):
        Igniter(
            config=self.config,
            proxies=self.proxies
        ).main()


if __name__ == "__main__":
    Main().main()
