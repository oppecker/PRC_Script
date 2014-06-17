# Script to automate creating a new thread for the weekly Poetry Recurring Contest on mtgsalvation forums.

#using selenium (2.42.1)
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import argparse

class AutomatePosting():
  def __init__(self):
    """
    Add Docstring
    """
    self.url = "http://www.mtgsalvation.com/forums/creativity/personal-writing"
    login_info = self.get_login_info()
    self.username = login_info[0]
    self.password = login_info[1]
    self.post_title = self.arg_parse()
    self.post_text = unicode(self.get_post_text(), errors='ignore')
    self.driver = self.open_webpage()
    
  def arg_parse(self):
    """
    Parse the arguments sent to script
    The script accepts parameter -t <string>.
    This will be returned and used for the new threads title.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--post_title", type=str, help="Use this string for the post title")
    args = parser.parse_args()
    #Require that a Title be passed in. The title must be different for each new thread created.
    if not (args.post_title):
      parser.error('Need to send a Post Title as a parameter')
    return args.post_title
    
  def get_login_info(self):
    """
    open file 'account_info.txt' for reading and get the first two lines, which contain the username and password to be used.
    """
    handle = open('account_info.txt', 'r')
    login_info = handle.read().split('\n')
    handle.close()
    return login_info[0], login_info[1]
    
  def get_post_text(self):
    """
    open file 'PRC_Post.txt', which contains the text to post (created by prc_script.py).
    returns the text to write.
    """
    handle = open('PRC_Post.txt', 'r')
    return handle.read()
    
  def open_webpage(self):
    """
    Accepts a url, opens a webdriver firefox object, loads the url, then returns the webdriver object
    """
    driver = webdriver.Firefox()
    driver.get(self.url)
    return driver
    
  def close_webpage(self):
    """
    accepts the webdriver and uses that to close the webdriver window.
    """
    self.driver.close()
    
  def login_to_page(self):
    """
    accepts the webdriver object, and user and password.
    Logs into the page, then returns the driver object
    """
    #Locate and click the Login Link to get prompt to enter username and password
    login_link = self.driver.find_element_by_link_text("Login")
    login_link.click()

    #Wait for availability of username field, then enter username, password, and click the login button
    login_name = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "field-username")))
    login_name.send_keys(self.username)
    login_password = self.driver.find_element_by_id("field-loginFormPassword")
    login_password.send_keys(self.password)
    login_button = self.driver.find_element_by_name("login")
    login_button.click()
    
  def create_and_submit_post(self):
    """
    accept webdriver, title for new thread post, and text for the new thread.
    returns driver.
    """
    #Find and click the new thread button(link)
    self.driver.find_element_by_link_text("New Thread")
    new_thread_button = self.driver.find_element_by_link_text("New Thread")
    new_thread_button.click()

    #Enter the post title and post text
    thread_title = self.driver.find_element_by_id("field-title")
    thread_title.send_keys(self.post_title)
    thread_text = self.driver.find_element_by_id("field-post")
    thread_text.send_keys(self.post_text)

    #Submit the new post
    thread_submit_button = self.driver.find_element_by_id("field-submit")
    thread_submit_button.click()
    
  def logout_from_page(self):
    """
    Accepts webdriver object.
    Logs out of the web page, then returns the webdriver
    """
    logout_link = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='t-netbar-account t-netbar-section my-profile-link u-dropdown']")))
    logout_link.click()
    logout_link = self.driver.find_element_by_xpath("//ul[@class='t-netbar-account t-netbar-section my-profile-link u-dropdown']//li[@class='logout']//a[@class='ajax-post']")
    logout_link.click()
    
  def main(self):
    """
    Add Docstring
    """
    self.login_to_page()
    self.create_and_submit_post()
    self.logout_from_page()
    self.close_webpage()
    
    
if __name__ == "__main__":
  run_script = AutomatePosting()
  run_script.main()