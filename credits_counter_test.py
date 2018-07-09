import os, time, unittest, warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


link_to_game = 'http://slotmachinescript.com/'

class Page:
    def __init__(self, driver):
        self.spin_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'spinButton')))
        self.last_win = 0
        for sec in range(13):
            print(sec)
            try:
                self.last_win = int(driver.find_element_by_id('lastWin').text)
                if self.last_win:
                    break
            except:
                self.last_win = 0
            time.sleep(1)
        self.total_spins = int(driver.find_element_by_id('credits').text)
        self.bet = int(driver.find_element_by_id('bet').text)
        self.bet_spin_up = driver.find_element_by_id('betSpinUp')

class UITests(unittest.TestCase):
    def setUp(self):
        ''''''
        '''ignore insides warnings'''
        warnings.simplefilter("ignore", ResourceWarning)
        warnings.simplefilter("ignore", DeprecationWarning)

        '''open chrome'''
        self.driver = webdriver.Chrome('{}\chromedriver'.format(os.path.dirname(__file__)))
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

        '''go to game page'''
        self.driver.get(link_to_game)

    def test_credits_counter(self):
        ''''''
        '''first round'''
        self.page = Page(self.driver)
        self.prev_total_spins = self.page.total_spins
        self.page.spin_button.click()
        self.page = Page(self.driver)
        print('first spin: ', self.prev_total_spins, self.page.bet, self.page.last_win, self.page.total_spins)

        '''BET changing'''
        for _ in range(2):
            self.page.bet_spin_up.click()

        '''first round after change BAT'''
        self.prev_total_spins = self.page.total_spins
        self.page.spin_button.click()
        self.page = Page(self.driver)
        with self.subTest():
            print('first spin with 3: ', self.prev_total_spins, self.page.bet, self.page.last_win, self.page.total_spins)
            self.assertTrue(self.prev_total_spins - self.page.bet + self.page.last_win == self.page.total_spins)

        '''play until win'''
        self.page.last_win = 0

        while not self.page.last_win:
            self.prev_total_spins = self.page.total_spins
            self.page.spin_button.click()
            self.page = Page(self.driver)
            print('while spin: ', self.prev_total_spins, self.page.bet, self.page.last_win, self.page.total_spins)

        print(self.prev_total_spins, self.page.bet, self.page.last_win, self.page.total_spins)
        self.assertTrue(self.prev_total_spins - self.page.bet + self.page.last_win == self.page.total_spins)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

