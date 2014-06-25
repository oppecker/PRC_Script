# Script to automatically create the text of the weekly post for the "poetry running contest" on the mtgsalvation forums.

# using beautifulsoup4 (4.3.2) for this script
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import urllib2
import argparse
import sys
import re

#using selenium (2.42.1)
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PRCForumTools(object):
  def __init__(self):
    """
    Initialize PrcScript variables
    self.days     posts less then <self.days> days old will be used
    self.pages    posts from <self.pages> thread pages back will be considered
    self.output   post text output will be written to file <self.output>
    self.url      url of thread to get post information from
    """
    self.personal_writing_url = 'http://www.mtgsalvation.com/forums/creativity/personal-writing'
    self.submission_thread_url = 'http://www.mtgsalvation.com/forums/creativity/personal-writing/494511-poetry-running-contest-submission-thread'
    self.last_round, self.current_round, self.next_round = self.get_last_current_next_round()
    #print "Outputting post text to file: < " + self.output + " >"
    login_info = self.get_login_info()
    self.username = login_info[0]
    self.password = login_info[1]

  def parse_parameters(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str, default="PRC_Post.txt", help="Write post output to <file> indicated here")
    args = parser.parse_args()
    return args.output
    
  def get_url_contents(self, page_url):
    """
    Opens and reads the contents of page_url
    Creates and returns a BeautifulSoup object using the contents of page_url
    """
    content = urllib2.urlopen(page_url).read()
    return BeautifulSoup(content)

  def get_post_date(self, post):
    """
    Using the post passed in, find the date of the post (format mm/dd/yyyy)
    Return a datetime object for the date the post was made.
    """
    post_date = post.find('span', {'itemprop' : 'dateCreated'}).string.split(" ")[0]
    return datetime.strptime(post_date, "%m/%d/%Y")
    
  def get_post_link(self, post):
    """
    Return the link to the post passed in to the function.
    """
    return post.find('a', 'j-comment-link')['href']
    
  def get_poster_name(self, post):
    """
    Return the name of the poster for the post passed in to the function.
    """
    return post.find('span', {'itemprop' : 'name'}).string
    
  def get_post_title(self, post):
    """
    Find the posts first line of text.
    The if statements check for the first line a few different ways. This is to account for the different ways people seem to format their posts.
    If a first line can not be determined, it is set as "Error: Could Not Figure Out A Title", so that it can be manually figured out.
    Return the first line of text, striped of any formatting that might be present.
    """
    post_title = post.find('div', {'itemprop' : 'text'}).contents[0].string
    if post_title == None:
      post_title = post.find('div', {'itemprop' : 'text'}).contents[0].text
      if post_title == None:
        post_title = "Error: Could Not Figure Out A Title"

    return post_title.strip()
    
  def get_last_current_next_round(self):
    soup = self.get_url_contents(self.personal_writing_url)
    thread_titles = soup.findAll('a', 'title')
    prc_title_pattern = re.compile('^PRC \d\d\d$')
    thread_numbers = []
    for title in thread_titles:
      if prc_title_pattern.match(str(title.contents[0])):
        thread_numbers.append(int(title.contents[0].split(" ")[1]))
    thread_numbers.sort()
    last_round = thread_numbers[-1]
    current_round = last_round + 1
    next_round = current_round + 1
    return last_round, current_round, next_round
    
  def write_post_to_output(self, post_text):
    try:
      with open(self.output, 'w') as output_file:
        output_file.write(post_text)
        output_file.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit()
        
  def get_login_info(self):
    """
    open file 'account_info.txt' for reading and get the first two lines, which contain the username and password to be used.
    """
    handle = open('account_info.txt', 'r')
    login_info = handle.read().split('\n')
    handle.close()
    return login_info[0], login_info[1]
    
  """
  Selenium Functions Below Here:
  """
  def logout_from_page(self):
    """
    Accepts webdriver object.
    Logs out of the web page, then returns the webdriver
    """
    logout_link = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='t-netbar-account t-netbar-section my-profile-link u-dropdown']")))
    logout_link.click()
    logout_link = self.driver.find_element_by_xpath("//ul[@class='t-netbar-account t-netbar-section my-profile-link u-dropdown']//li[@class='logout']//a[@class='ajax-post']")
    logout_link.click()

  def post_submission_thread_update(self, post_text):
    """
    Add Docstring
    """
    #self.login_to_page()
    
    content = urllib2.urlopen(self.submission_thread_url).read()
    soup = BeautifulSoup(content)
    page_links = soup.find('ul', 'b-pagination-list').findAll('a', 'b-pagination-item')
    final_page_number = int(page_links[-1].contents[0])
    final_thread_page_url = '{0}?page={1}'.format(self.submission_thread_url, str(final_page_number))
    print final_thread_page_url
    
    driver = webdriver.Firefox()
    driver.get(self.submission_thread_url)
    
    
    
    login_link = driver.find_element_by_link_text("Login")
    login_link.click()

    #Wait for availability of username field, then enter username, password, and click the login button
    login_name = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "field-username")))
    login_name.send_keys(self.username)
    login_password = driver.find_element_by_id("field-loginFormPassword")
    login_password.send_keys(self.password)
    login_button = driver.find_element_by_name("login")
    login_button.click()
    
    driver.get(final_thread_page_url)
    
    text_area = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "field-body")))
    text_area.send_keys(post_text)
    
    #Submit the new post
    #thread_submit_button = driver.find_element_by_id("field-submit")
    #thread_submit_button.click()
    
    #self.logout_from_page()
    #self.close_webpage()
    
  def create_and_submit_new_round_post(self, post_text):
    """
    accept webdriver, title for new thread post, and text for the new thread.
    returns driver.
    """
    
    driver = webdriver.Firefox()
    driver.get(self.personal_writing_url)
    login_link = driver.find_element_by_link_text("Login")
    login_link.click()

    #Wait for availability of username field, then enter username, password, and click the login button
    login_name = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "field-username")))
    login_name.send_keys(self.username)
    login_password = driver.find_element_by_id("field-loginFormPassword")
    login_password.send_keys(self.password)
    login_button = driver.find_element_by_name("login")
    login_button.click()
    
    
    
    
    #Find and click the new thread button(link)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.LINK_TEXT, "New Thread")))    #driver.find_element_by_link_text("New Thread")
    new_thread_button = driver.find_element_by_link_text("New Thread")
    new_thread_button.click()

    #Enter the post title and post text
    thread_title = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "field-title")))   #driver.find_element_by_id("field-title")
    thread_title.send_keys('PRC {0}'.format(self.current_round))
    thread_text = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "field-post")))     #driver.find_element_by_id("field-post")
    thread_text.send_keys(post_text)
    
    #Submit the new post
    thread_submit_button = driver.find_element_by_id("field-submit")
    thread_submit_button.click()
    
    
  def get_post_text(self):
    """
    open file 'PRC_Post.txt', which contains the text to post (created by prc_script.py).
    returns the text to write.
    """
    handle = open('PRC_Post.txt', 'r')
    return handle.read()