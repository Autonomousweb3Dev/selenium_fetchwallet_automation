import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

load_dotenv(".env")

EXTENSION_PATH = f"{os.getcwd()}/fetchwallet.crx"  # Path of crx file
print(f"EXTENSION_PATH: {EXTENSION_PATH}")
if not os.path.exists(EXTENSION_PATH):
    raise FileNotFoundError(f"The specified crx file does not exist: {EXTENSION_PATH}")

EXTENSION_ID = "ellkdbaphhldpeajbepobaecooaoafpg"
MNEMONIC_SEED = os.environ.get("MNEMONIC_SEED")


class FetchWallet:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_extension(EXTENSION_PATH)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        print("Extension has been loaded")
        self.driver.implicitly_wait(20)

    def import_account(self):
        print("Importing account...")
        self.driver.get(f"chrome-extension://{EXTENSION_ID}/popup.html#/register")
        self.driver.maximize_window()
        self.driver.find_element(
            By.XPATH, "//*[text()='Import existing account']"
        ).click()
        self.driver.find_element(By.NAME, "words").send_keys(MNEMONIC_SEED)
        self.driver.find_element(By.NAME, "name").send_keys("Import account")
        self.driver.find_element(By.NAME, "password").send_keys("11111111")
        self.driver.find_element(By.NAME, "confirmPassword").send_keys("11111111")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)

    def open_fetch_wallet(self):
        print("Opening FetchWallet...")
        self.driver.get(f"chrome-extension://{EXTENSION_ID}/popup.html")

    def network_change(self):
        print("Changing network...")
        self.driver.find_element(
            By.XPATH, '//div[@class="chain-list-container-3lVS1ADkLvCaYJqwFSxJY0"]'
        ).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[text()='Dorado']").click()
        time.sleep(3)

    def send(self):
        print("Sending tokens...")
        self.driver.find_element(By.XPATH, "//button[text()='Send']").click()
        self.driver.find_element(By.XPATH, "//input[@type='text']").send_keys(
            "fetch1sgjd58298xtgmyce2wva5kkjjrelmlcvu9pewt"
        )
        self.driver.find_element(By.XPATH, "//input[@type='number']").send_keys(
            "0.0001"
        )
        time.sleep(3)
        action = ActionChains(self.driver)
        action.move_to_element(
            self.driver.find_element(By.XPATH, "//button[@type='submit']")
        ).perform()
        time.sleep(3)
        action.click().perform()
        self.driver.find_element(By.XPATH, "//*[text()='Approve']").click()
        time.sleep(3)

    def stake(self):
        print("Staking tokens...")
        self.driver.find_element(By.XPATH, "//button[text()='Stake']").click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element(By.XPATH, "//button[text()='Connect Wallet']").click()
        self.driver.switch_to.window(self.driver.window_handles[2])
        self.driver.find_element(By.XPATH, "//button[text()='Approve']").click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Stake']"))
        ).click()
        self.driver.find_element(By.XPATH, "//input[@placeholder='Amount']").send_keys(
            "0.000000001"
        )
        self.driver.find_element(By.XPATH, "//button[text()='Stake']").click()
        time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[2])
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Approve']"))
        ).click()
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(2)

    def claim(self):
        print("Claiming tokens...")
        self.driver.find_element(By.XPATH, "//button[text()='Claim']").click()
        self.driver.find_element(By.XPATH, "//*[text()='Approve']").click()
        time.sleep(3)

    def create_account(self):
        print("Creating new account...")
        self.driver.switch_to.new_window()
        self.driver.get(f"chrome-extension://{EXTENSION_ID}/popup.html#/register")
        self.driver.find_element(By.XPATH, "//*[text()='Create new account']").click()
        text = self.driver.find_element(By.XPATH, "//div[@class='form-group'][1]").text
        seeds = text.split()
        self.driver.find_element(By.NAME, "name").send_keys("new account")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)

        for i in seeds:
            self.driver.find_element(By.XPATH, f"//button[text()='{i}']").click()
            time.sleep(1)

        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, "//button[text() = 'Done' ]").click()
        time.sleep(3)


if __name__ == "__main__":
    fetch_wallet = FetchWallet()
    fetch_wallet.import_account()
    fetch_wallet.open_fetch_wallet()
    fetch_wallet.network_change()
    fetch_wallet.send()
    fetch_wallet.stake()
    fetch_wallet.claim()
    fetch_wallet.create_account()
