import os, time, unittest, warnings
from selenium import webdriver


link_to_game = 'http://slotmachinescript.com/'

class Page:
    def __init__(self, driver):
        self.last_win = driver.find_element_by_id('lastWin')
        self.total_spins = driver.find_element_by_id('credits')
        self.bet = driver.find_element_by_id('bet')
        self.bet_spin_up = driver.find_element_by_id('betSpinUp')
        self.spin_button = driver.find_element_by_id('spinButton')
        self.slots_outer_container = driver.find_element_by_id('SlotsOuterContainer')

    def get_last_win(self):
        if self.last_win.text:
            return self.last_win.text
        return 0

    def wait_for_spin_button(self):
        while True:
            if not self.spin_button.get_attribute("class"):
                break
            time.sleep(0.5)


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
        self.prev_total_spins = self.page.total_spins.text
        self.page.spin_button.click()
        self.page.wait_for_spin_button()

        '''BET changing'''
        for _ in range(2):
            self.page.bet_spin_up.click()

        '''first round after change BAT'''
        self.prev_total_spins = self.page.total_spins.text
        self.page.spin_button.click()
        self.page.wait_for_spin_button()
        with self.subTest():
            self.assertTrue(int(self.prev_total_spins) - int(self.page.bet.text) + int(self.page.get_last_win()) == int(self.page.total_spins.text))

        '''play until win'''
        self.page.last_win = 0
        while not self.page.last_win:
            self.prev_total_spins = self.page.total_spins.text
            self.page.spin_button.click()
            self.page.wait_for_spin_button()
            if self.page.slots_outer_container.get_attribute("class"):
                self.page.last_win = self.driver.find_element_by_id('lastWin')
        self.assertTrue(int(self.prev_total_spins) - int(self.page.bet.text) + int(self.page.last_win.text) == int(self.page.total_spins.text))

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

