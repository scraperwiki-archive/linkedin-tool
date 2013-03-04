import os
import time

from splinter import Browser

browser = Browser()

def setUp():
  browser.cookies.delete()
  browser.visit('http://x.scraperwiki.com/dataset/fello3q/settings')
  browser.find_by_css('#username').fill(os.environ['X_INT_USER'])
  browser.find_by_css('#password').fill(os.environ['X_INT_PASS'])
  browser.find_by_css('#login').click()
  browser.visit('http://x.scraperwiki.com/dataset/fello3q/settings')

def ensure_i_am_on_the_settings_page():
  assert browser.is_text_present('Settings', wait_time=10)
  assert browser.is_text_present('LinkedIn', wait_time=10)

def ensure_there_is_a_textarea():
  container = browser.find_by_css('iframe').first
  with browser.get_iframe(container['name']) as container:
    tool_content = container.find_by_css('iframe').first
    with container.get_iframe(tool_content['name']) as tool_content:
      assert tool_content.is_element_present_by_css('textarea', wait_time=10)
      # TODO: move
      tool_content.execute_script("scraperwiki.exec('rm access_token.json')")
      tool_content.execute_script("scraperwiki.exec('rm scraperwiki.sqlite')")
      browser.reload()

source_list = """P Parker
K Clark
B Wayne"""

def it_should_redirect_to_linkedin_when_auth_clicked():
  container = browser.find_by_css('iframe').first
  with browser.get_iframe(container['name']) as container:
    tool_content = container.find_by_css('iframe').first
    with container.get_iframe(tool_content['name']) as tool_content:
      textarea = tool_content.find_by_css('textarea')[0]
      textarea.fill(source_list)
      auth_button = tool_content.find_by_css('#authenticate')
      time.sleep(1)
      auth_button.click()
  time.sleep(1)
  assert 'linkedin.com' in browser.url

def it_should_redirect_to_the_tool_when_authorised():
  email = browser.find_by_xpath('//*[@id="session_key-oauth2SAuthorizeForm"]')
  email.fill(os.environ['LINKEDIN_USER'])
  password =  browser.find_by_xpath('//*[@id="session_password-oauth2SAuthorizeForm"]')
  password.fill(os.environ['LINKEDIN_PASS'])

  browser.find_by_name('authorize').click()
  assert 'fello3q' in browser.url

def ensure_tool_tells_user_that_it_is_authenticated():
  container = browser.find_by_css('iframe').first
  with browser.get_iframe(container['name']) as container:
    tool_content = container.find_by_css('iframe').first
    with container.get_iframe(tool_content['name']) as tool_content:
      assert tool_content.is_text_present('Authenticated', wait_time=7)

def ensure_textarea_is_already_populated():
  container = browser.find_by_css('iframe').first
  with browser.get_iframe(container['name']) as container:
    tool_content = container.find_by_css('iframe').first
    with container.get_iframe(tool_content['name']) as tool_content:
      
      textarea = tool_content.find_by_css('textarea')[0]
      print "textarea", repr(textarea.value)
      print "source_list", repr(source_list)
      assert textarea.value == source_list
