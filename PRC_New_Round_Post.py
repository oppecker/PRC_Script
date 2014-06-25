# Script to automatically create the text of the weekly post for the "poetry running contest" on the mtgsalvation forums.

# using beautifulsoup4 (4.3.2) for this script
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import urllib2
import argparse
import sys
import re
from PRC_Forum_Tools import PRCForumTools

class PRCNewRoundPost(PRCForumTools):
  def __init__(self):
    self.days, self.pages, self.output = self.parse_parameters()
    super(PRCNewRoundPost, self).__init__()
    print "Gathering Posts from up to < " + str(self.days.days) + " > days ago."
    print "Searching through last < " + str(self.pages) + " > pages of thread."
    print "Outputting post text to file: < " + self.output + " >"
    
  def parse_parameters(self):
    """
    Script can accept the parameters:
    -w <num>   --weeks <num>   posts less then <num> weeks old will be used
    -p <num>   --pages <num>   posts from <num> thread pages back will be considered
    -o <str>   --output <str>  post text output will be written to file <str>
    
    number of weeks is returned as number of days by multiplying it by 7
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--weeks", type=int, default=1, choices=[1,2,3], help="Pull posts from <num> weeks back")
    parser.add_argument("-p", "--pages", type=int, default=2, choices=[1,2,3], help="Search <num> pages back in the thread for valid posts")
    parser.add_argument("-o", "--output", type=str, default="PRC_Post.txt", help="Write post output to <file> indicated here")
    args = parser.parse_args()
    return timedelta(days=args.weeks * 7), args.pages, args.output
    
  def get_thread_pages(self):
    """
    Extracts the page link numbers from the thread.
    Use the page link numbers to determine the page number of the final thread page.
    If the user has requested searching more pages then the thread is long (through the -p or -pages parameter) then self.pages is just set to the length of the thread.
    Returns array of links to the thread pages that to search though.
    """
    soup = self.get_url_contents(self.submission_thread_url)
    page_links = soup.find('ul', 'b-pagination-list').findAll('a', 'b-pagination-item')
    final_page_number = int(page_links[-1].contents[0])
    if self.pages >= final_page_number:
      print "Thread does not contain " + str(pages) + " pages. Will perform search on all " + str(final_page_number) + " pages of the thread instead."
      self.pages = final_page_number
    return [(self.submission_thread_url + '?page=' + str(index)) for index in range(final_page_number + 1 - self.pages, final_page_number + 1)]
    
  def get_and_format_post_links(self, thread_pages):
    """
    post_links is the array that will hold the links to posts (formatted as: '[URL="' + post_link + '"]' + post_title + '[/URL] by ' + poster_name + '\n') to be used for the new round post.
    present is a datetime object representing the current time. This will be compared with posts dates to determine whether to add a formatted link to that post to post_links.
    thread_pages is an array of links to the thread pages to search for posts.
    
    Search through each page in thread_pages for potential posts to add to post_links. For post on each page, attempt to get the posts date, this step might fail due to the issue described here:
    
    Site recently changed something... now there is some extra html for adds or something which are collected along with the valid posts.
    without the try except statement these cause error messages such as: "TypeError: 'NoneType' object has no attribute '__getitem__'"
    when it's failing this is the contents of post:
    <li class="p-comments p-comments-b"><section class="ad-container"><div class="ad-bin"><div class="ad-placement"></div></div></section></li>
    need to change the "thread_comments = soup.findAll('li', 'p-comments', 'p-comments-b')" line to somehow not grab those lines as posts
    
    If the post date is figured out successfully, make sure the post is recent enough to use, then get all the parts necessary for creating the formatted post link, then append to post_links.
    
    Returns post_links array.
    """
    post_links = []
    present = datetime.now()
    for page in thread_pages:
      soup = self.get_url_contents(page)
      thread_posts = soup.findAll('li', 'p-comments', 'p-comments-b')

      for post in thread_posts:
        try:
          post_date = self.get_post_date(post)
        except:
          continue
        if post_date >= (present - self.days):
          post_link = self.get_post_link(post)
          poster_name = self.get_poster_name(post)
          post_title = self.get_post_title(post)
          post_links.append('[URL="' + post_link + '"]' + post_title + '[/URL] by ' + poster_name + '\n')
    return post_links
    
  def write_post_to_file(self, post_links):
    """
    Writing post to text file is for debugging purposes.
    Import the strings first_post_section, and final_post_section from prc_post_vars.py. These are in a separate file because they are ugly and should be kept hidden.
    post_links is an array of all the formatted links to the submitted poems.
    The the text to post will be written out to file self.output (defaults to "PRC_Post.txt").
    The text written to the output file in this order: first_post_section, post_links, final_post_section.
    If some I/O error happens, it is written to std output.
    """
    from prc_script_vars import first_post_section, final_post_section
    post_text = first_post_section + "".join(post_links).encode('utf8') + final_post_section
    post_text = unicode(post_text, errors="ignore")
    self.write_post_to_output(post_text)
    return post_text
    
  def main(self):
    """
    Runs PrcScript class functions to create text to post for new PRC round.
    """
    thread_pages = self.get_thread_pages()
    post_links = self.get_and_format_post_links(thread_pages)
    post_text = self.write_post_to_file(post_links)
    #print post_text
    #post_text = self.get_post_text()
    #post_text = unicode(post_text, errors="ignore")
    #print post_text
    self.create_and_submit_new_round_post(post_text)
    
if __name__ == "__main__":
  run_script = PRCNewRoundPost()
  run_script.main()