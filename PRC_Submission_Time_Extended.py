# Script to automatically create the text of the weekly post for the "poetry running contest" on the mtgsalvation forums.

# using beautifulsoup4 (4.3.2) for this script
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import urllib2
import argparse
import sys
import re
from PRC_Forum_Tools import PRCForumTools

#using selenium (2.42.1)
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PRCSubmissionTimeExtended(PRCForumTools):
  def __init__(self):
    super(PRCSubmissionTimeExtended, self).__init__()
    
  def main(self):
    message = '[b]Submission time for Round {} extended until next Monday to allow for more poems to be submitted![/b]'.format(str(self.current_round))
    print message
    self.post_submission_thread_update(message)
    
if __name__ == "__main__":
  run_script = PRCSubmissionTimeExtended()
  run_script.main()