# Script to automatically create the text of the weekly post for the "poetry running contest" on the mtgsalvation forums.

# using beautifulsoup4 (4.3.2) for this script
from bs4 import BeautifulSoup
import urllib2
from datetime import date, timedelta, datetime
import argparse

def get_last_pages():
  """
  Return array of urls for the last two pages of thread pointed to by url
  """
  url = 'http://www.mtgsalvation.com/forums/creativity/personal-writing/494511-poetry-running-contest-submission-thread'
  content = urllib2.urlopen(url).read()
  soup = BeautifulSoup(content)
  navigation_page_links = soup.find('ul', 'b-pagination-list')
  final_page_links = navigation_page_links.findAll('a', 'b-pagination-item')
  final_page_number = int(final_page_links[-1].contents[0])
  return [url + '?page=' + str(final_page_number - 1), url + '?page=' + str(final_page_number)]

def get_posted_poems(final_pages, time_frame):
  """
  Return the link, poem title, and commenters name for each post
  """
  # poem_comment_links will contain an array with each element having the form: '[URL="' + comment_link + '"]' + poem_title + '[/URL] by ' + commenter_name + '\n'
  poem_comment_links = []
  present = datetime.now()
  for page in final_pages:
    content = urllib2.urlopen(page).read()
    soup = BeautifulSoup(content)
    thread_comments = soup.findAll('li', 'p-comments', 'p-comments-b')
    

    for comment in thread_comments:
      # Site recently changed something... now there is some extra html for adds or something that breaks this
      # without the try except statement the script now fails with "TypeError: 'NoneType' object has no attribute '__getitem__'"
      # when it's failing this is the contents of comment:
      # <li class="p-comments p-comments-b"><section class="ad-container"><div class="ad-bin"><div class="ad-placement"></div></div></section></li>
      # need to change the "thread_comments = soup.findAll('li', 'p-comments', 'p-comments-b')" line to only grab the correct info to fix this
      try:
        comment_link = comment.find('a', 'j-comment-link')['href']
      except TypeError:
        continue
        
      commenter_name = comment.find('span', {'itemprop' : 'name'}).string
      #post date stuff
      post_date = comment.find('span', {'itemprop' : 'dateCreated'}).string
      post_date = post_date.split(" ")[0]
      post_date = datetime.strptime(post_date, "%m/%d/%Y")
      
      poem_title = comment.find('div', {'itemprop' : 'text'}).contents[0].string
      if poem_title == None:
        poem_title = "None"
      # if the 'post_date' is from within the time frame given, append the post to "poem_comment_links" array
      if post_date >= (present - time_frame):
        poem_comment_links.append('[URL="' + comment_link + '"]' + poem_title + '[/URL] by ' + commenter_name + '\n')
  return poem_comment_links

def write_post_to_file(poem_comment_links):
  """
  Write first_part, poem_comment_links, then last part to "PRC_Post.txt"
  """
  first_part = """Welcome to the [i][COLOR="DarkSlateGray"]Poetry Running Contest![/color][/i]

  Here are the Poetry submissions for this week:\n\n"""
  last_part = """\nVote for the poem(s) you feel is the best (up to two). Remember to adhere to the "Honor Code" when voting.
  [spoiler=Honor Code:]
  While it is understood there is no absolute means to monitor the intent of a vote, we ask each PRC participant to exercise integrity when voting out of respect for the contest:

  - Please give each poetry submission an equal opportunity in attaining your vote.
  - Please read, or at least skim, all the entries before voting.
  - Please do not vote for your friends just because they're your friends.

  The Poetry Running Contest puts good faith in its participants to act in an honorable manner.[/spoiler]

  Contestants, remember, you are [b]required[/b] to vote (and you can't vote for yourself)!
  Also, please leave a comment on this thread telling who you voted for as currently the polling system does not currently have the option to display that information.

  [b]Please Note, Voting Is To Be Done Via The Comments On The Thread. This Way We Can Track Who Has Voted, Foster Discussion, And Avoid Using The Currently Horrendous Poll System This Site Has.[/b] 

  Thank you and Happy voting!"""
  
  output_file = open('PRC_Post.txt', 'w')
  output_file.write(first_part + "".join(poem_comment_links).encode('utf8') + last_part)
  output_file.close()

def arg_parse():
  """
  Parse the arguments sent to script
  currently returning a timedelta of 1 to 3 weeks for use returning the right amount posts
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("-w", "--weeks", type=int, choices=[1,2,3], default=1, help="Pull posts from X num weeks back")
  args = parser.parse_args()
  return timedelta(days=args.weeks * 7)
  
if __name__ == "__main__":
  # Parse Parameters
  time_frame = arg_parse()
  print "Gathering Posts from " + str(time_frame.days) + " days ago."
  # Get the final two pages of script
  final_pages = get_last_pages()
  # store each posts link, poem_title, and commenters name in array poem_comment_links
  poem_comment_links = get_posted_poems(final_pages, time_frame)
  # write posts from poem_comment_links and other needed text for post to "PRC_Post.txt"
  write_post_to_file(poem_comment_links)