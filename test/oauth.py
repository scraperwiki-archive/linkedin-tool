import os
import unittest
from splinter import Browser
browser = Browser()

class WhenIVisitTheDatasetSettingsPage(unittest.TestCase):
  def setUp(self):
    browser.visit('http://x.scraperwiki.com/dataset/fello3q/settings')
    browser.find_by_css('#username').fill(os.environ['X_INT_USER'])
    browser.find_by_css('#password').fill(os.environ['X_INT_PASS'])
    browser.find_by_css('#login').click()
    browser.visit('http://x.scraperwiki.com/dataset/fello3q/settings')

  def ensure_i_am_on_the_settings_page(self):
    assert browser.is_text_present('Settings', wait_time=10)
    assert browser.is_text_present('LinkedIn', wait_time=10)

#class IfIHaveNotAuthorised(unittest.TestCase):
#
#  def ensure_authorise_button_present(self):
#    assert browser.find_by_css('#authorise')
