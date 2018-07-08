import os, datetime, time, unittest, pyautogui, warnings, HtmlTestRunner
from selenium import webdriver
from natsort import natsorted

link_to_game = 'https://www.netent.com/en/game/starburst-2/'
lvls_imgs = natsorted(os.listdir('{}{}'.format(os.getcwd(), '\\Imgs\\levels\\')))
bets_imgs = natsorted(os.listdir('{}{}'.format(os.getcwd(), '\\Imgs\\bets\\')))


class ScreenTests(unittest.TestCase):
    def get_screen(self):
        for i in range(5):
            pyautogui.screenshot('{}{}{}'.format(os.getcwd(),
                                                 '\\',
                                                 '{}_{}.png'.format(self, datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')))
                                 )

    def find_image(self, image_name, dir, min_seatch_time = 0, **kwargs):
        return pyautogui.locateOnScreen('{}{}{}'.format(os.getcwd(), dir, image_name),
                                        min_seatch_time, **kwargs)

    def click_to_center(self, button):
        x, y = pyautogui.center(button)
        pyautogui.click(x=x, y=y)

    def setUp(self):
        ''''''
        '''ignore insides warnings'''
        warnings.simplefilter("ignore", ResourceWarning)
        warnings.simplefilter("ignore", DeprecationWarning)

        '''open chrome'''
        self.driver = webdriver.Chrome('{}\chromedriver.exe'.format(os.path.dirname(__file__)))
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

        '''go to game page'''
        self.driver.get(link_to_game)

        '''click to over 18 button'''
        self.click_to_center(self.find_image('over_18.png', '\\Imgs\\', 10))
        time.sleep(1)

        '''Touch to start Game'''
        pyautogui.click()
        time.sleep(5)

        '''accept cooke policy'''
        self.click_to_center(self.find_image('yes_cooke.png', '\\Imgs\\', 10))
        time.sleep(1)

        '''click to continue'''
        self.click_to_center(self.find_image('continue.png', '\\Imgs\\', 10))
        time.sleep(1)

    def test_change_lvl_and_bets(self):
        ''''''
        '''find button lvl_right_arrow'''
        self.lvl_right_arrow = self.find_image('lvl_right_arrow.png', '\\Imgs\\', 10)
        if self.lvl_right_arrow:
            for lvl_img, bets in zip(lvls_imgs, bets_imgs):
                '''check level and bets'''
                with self.subTest():
                    self.assertTrue(self.find_image(lvl_img, '\\Imgs\\levels\\', 10), msg="{} not finded".format(lvl_img))
                    self.assertTrue(self.find_image(bets, '\\Imgs\\bets\\', 10), msg="{} not finded".format(bets))
                '''click to lvl_right_arrow button'''
                self.click_to_center(self.lvl_right_arrow)
        else:
            self.get_screen()
            raise ValueError("lvl_right_arrow isn't fided")

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    # unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='{}\\1.html'.format(os.getcwd()), report_title='Autotesting report'), verbosity=2)
    unittest.main()
