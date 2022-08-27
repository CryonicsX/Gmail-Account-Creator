from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import Proxy, ProxyType


from ..config import *
from ..snippets.services import *
import time, traceback, random


def write(file: str, text: str):
    with open(file, "a+") as f:
        f.write(text)

class worker:
    def __init__(self,name: list, username: str, password: str, useragent: str, apikey: str, CLI, thread_id: str, proxy: dict = None) -> None:
        self.name = name
        self.username = username
        self.password = password
        self.proxy = proxy
        self.ua = useragent
        self.apikey = apikey
        self.CLI = CLI
        self.thread_id = thread_id



        self.wait_time = 60
        self.endpoint = "https://accounts.google.com/"

        self.options = Options()
        arguments = ["--no-sandbox", "--disable-dev-shm-usage", f"user-agent={self.ua}", "--log-level=3"]

        capabilities = None
        if proxy: 
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = self.proxy
            proxy.ssl_proxy = self.proxy

            capabilities = webdriver.DesiredCapabilities.CHROME
            proxy.add_to_capabilities(capabilities)
            arguments.append(f"--proxy-server={self.proxy}")



        for args in arguments:
            self.options.add_argument(args)

            
        self.driver = webdriver.Chrome(options=self.options, desired_capabilities=capabilities)
        


    def create_account(self) -> list:
        self.CLI.set(index=self.thread_id, status='Initiating.')
        
        try:
            
            self.driver.delete_all_cookies()
            self.driver.get(self.endpoint)
            self.CLI.set(index=self.thread_id, status=f"Endpoint opening.")


            # CREATE ACCOUNT BUTTON
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath.create_account_button)))
            self.driver.find_element(by=By.XPATH, value=xpath.create_account_button).click()
            self.CLI.set(index=self.thread_id, status=f"Account creation started.")
            
            # FOR MY BUTTON
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath.for_my)))
            self.driver.find_element(by=By.XPATH, value=xpath.for_my).click()

            # FIRST NAME
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath.first_name)))
            self.driver.find_element(by=By.XPATH, value=xpath.first_name).send_keys(self.name[0])
            

            # LAST NAME
            self.driver.find_element(by=By.XPATH, value=xpath.last_name).send_keys(self.name[1])


            # USERNAME
            self.driver.find_element(by=By.XPATH, value=xpath.username).send_keys(self.username)


            # PASSWORD
            self.driver.find_element(by=By.XPATH, value=xpath.password).send_keys(self.password)
            self.driver.find_element(by=By.XPATH, value=xpath.re_password).send_keys(self.password)


            # NEXT BUTTON
            self.driver.find_element(by=By.XPATH, value=xpath.next_button).click()
            self.CLI.set(index=self.thread_id, status=f"Entering account information.")


            # PHONE EDIT
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath.phone_input)))
            
            sms = smsactive(self.apikey)
            number = sms.get_number()
            if number["error"] == 1:
                self.CLI.set(index=self.thread_id, error=True)
                return False


            self.CLI.set(index=self.thread_id, status=f"Number: {number['number']}")
            '''
            self.driver.find_element(by=By.XPATH, value=xpath.country_list_button).click()
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath.flag_tr)))
            self.driver.find_element(by=By.XPATH, value=xpath.flag_tr).click()
            time.sleep(0.5)
            '''
            self.driver.find_element(by=By.XPATH, value=xpath.phone_input).send_keys(number["number"])
            time.sleep(0.5)
            self.driver.find_element(by=By.XPATH, value=xpath.next_buton_2).click()
            time.sleep(3)
            if "This phone number cannot be used for verification." in self.driver.page_source:
                self.CLI.set(index=self.thread_id, status="This phone number cannot be used for verification.", error=True)
                sms.delete_number(number["proc_id"])
                return False

            # VERIFY PHONE
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath.verify_phone_input)))
            self.CLI.set(index=self.thread_id, status=f"Waiting for verification code.")
            code = sms.wait_for_code(number["proc_id"])
            if code["error"] != 0:
                self.CLI.set(index=self.thread_id, error=True)
                return False


            self.CLI.set(index=self.thread_id, status=f"Code: {code['code']['code']}")
            self.driver.find_element(by=By.XPATH, value=xpath.verify_phone_input).send_keys(code["code"]["code"])
            self.driver.find_element(by=By.XPATH, value=xpath.verify_button).click()


            # EDIT PROFILE DETAILS
            self.CLI.set(index=self.thread_id, status=f"Editing profile detailes.")
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath.day)))
            self.driver.find_element(by=By.XPATH, value=xpath.day).send_keys(random.randint(1,20))
            select = Select(self.driver.find_element_by_xpath(xpath.month))
            select.select_by_value(str(random.randint(1,12)))
            self.driver.find_element(by=By.XPATH, value=xpath.year).send_keys(random.randint(1970, 2003))
            select = Select(self.driver.find_element_by_xpath(xpath.gender))
            select.select_by_value(str(random.randint(1,3)))
            self.driver.find_element(by=By.XPATH, value=xpath.next_button_3).click()


            # PASS SOME THINGS..
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath.next_button_4)))
            self.driver.find_element(by=By.XPATH, value=xpath.next_button_4).click()
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath.accept_button)))
            time.sleep(5)


            self.driver.find_element(by=By.XPATH, value=xpath.accept_button).click()
            self.CLI.set(index=self.thread_id, status=f"Account Created.")
            self.CLI.set(index=self.thread_id, creating=True)
            write("./out/accounts.txt", f"{self.username}@gmail.com:{self.password}\n")

            #time.sleep(9999)

            

        except:
            self.CLI.set(index=self.thread_id, error=True)
            traceback.print_exc()



