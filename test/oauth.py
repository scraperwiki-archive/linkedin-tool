import os
import time

from splinter import Browser

browser = Browser()

def setUp():
  browser.visit('http://x.scraperwiki.com/dataset/fello3q/settings')
  browser.find_by_css('#username').fill(os.environ['X_INT_USER'])
  browser.find_by_css('#password').fill(os.environ['X_INT_PASS'])
  browser.find_by_css('#login').click()
  browser.visit('http://x.scraperwiki.com/dataset/fello3q/settings')

def ensure_i_am_on_the_settings_page():
  assert browser.is_text_present('Settings', wait_time=10)
  assert browser.is_text_present('LinkedIn', wait_time=10)

def ensure_authenticate_button_present_if_not_authed():
  container = browser.find_by_css('iframe').first
  with browser.get_iframe(container['name']) as container:
    tool_content = container.find_by_css('iframe').first
    with container.get_iframe(tool_content['name']) as tool_content:
      assert tool_content.is_element_present_by_css('#authenticate', wait_time=10)

def it_should_redirect_to_twitter_when_auth_clicked():
  container = browser.find_by_css('iframe').first
  with browser.get_iframe(container['name']) as container:
    tool_content = container.find_by_css('iframe').first
    with container.get_iframe(tool_content['name']) as tool_content:
      auth_button = tool_content.find_by_css('#authenticate')
      time.sleep(1)
      auth_button.click()
  assert 'linkedin.com' in browser.url

def it_should_redirect_to_the_tool_when_authorised():
  # fill in linkedin username/pass
  # auth
  # check we're back to the tool settings page
  pass

def ensure_tool_tells_user_that_it_is_getting_data():
  # check for a spinner?
  pass

def ensure_data_is_in_database():
  # access sqlite endpoint, or view in table
  pass

# reload button?
# cron?
