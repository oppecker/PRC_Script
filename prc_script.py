# Script to automatically create the text of the weekly post for the "poetry running contest" on the mtgsalvation forums.

# using beautifulsoup4 (4.3.2) for this script
from bs4 import BeautifulSoup
import urllib2
from datetime import date, timedelta, datetime
import argparse

def get_last_pages(pages):
  """
  Return array of urls for the last two pages of thread pointed to by url
  """
  url = 'http://www.mtgsalvation.com/forums/creativity/personal-writing/494511-poetry-running-contest-submission-thread'
  content = urllib2.urlopen(url).read()
  soup = BeautifulSoup(content)
  navigation_page_links = soup.find('ul', 'b-pagination-list')
  final_page_links = navigation_page_links.findAll('a', 'b-pagination-item')
  final_page_number = int(final_page_links[-1].contents[0])
  if pages >= final_page_number:
    print "Thread does not contain " + str(pages) + " pages. Will perfrom search on all " + str(final_page_number) + " pages of the thread instead."
    pages = final_page_number
  final_pages = [(url + '?page=' + str(index)) for index in range(final_page_number + 1 - pages, final_page_number + 1)]
  #print final_pages
  #return url + '?page=' + str(final_page_number - 1), url + '?page=' + str(final_page_number)
  return final_pages

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
        comment_link = get_post_link(comment)
      except TypeError:
        continue
        
      commenter_name = get_poster_name(comment)
      
      post_date = get_post_date(comment)
      
      poem_title = get_poem_title(comment)
      
      # if the 'post_date' is from within the time frame given, append the post to "poem_comment_links" array
      if post_date >= (present - time_frame):
        poem_comment_links.append('[URL="' + comment_link + '"]' + poem_title + '[/URL] by ' + commenter_name + '\n')
  return poem_comment_links
  
def get_post_link(comment):
  comment_link = comment.find('a', 'j-comment-link')['href']
  return comment_link

def get_post_date(comment):
  post_date = comment.find('span', {'itemprop' : 'dateCreated'}).string
  post_date = post_date.split(" ")[0]
  post_date = datetime.strptime(post_date, "%m/%d/%Y")
  return post_date
  
def get_poster_name(comment):
  commenter_name = comment.find('span', {'itemprop' : 'name'}).string
  return commenter_name
  
def get_poem_title(comment):
  poem_title = comment.find('div', {'itemprop' : 'text'}).contents[0].string
  if poem_title == None:
    poem_title = comment.find('div', {'itemprop' : 'text'}).contents[0].text
    if poem_title == None:
      poem_title = "None"
  poem_title = poem_title.strip()
  return poem_title

def write_post_to_file(poem_comment_links, output_file_name):
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
  
  try:
    with open(output_file_name, 'w') as output_file:
      output_file.write(first_part + "".join(poem_comment_links).encode('utf8') + last_part)
      output_file.close()
  except IOError as e:
      print "I/O error({0}): {1}".format(e.errno, e.strerror)

def arg_parse():
  """
  Parse the arguments sent to script
  currently returning a timedelta of 1 to 3 weeks for use returning the right amount posts
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("-w", "--weeks", type=int, default=1, choices=[1,2,3], help="Pull posts from X num weeks back")
  parser.add_argument("-p", "--pages", type=int, default=2, choices=[1,2,3], help="Search X pages back for valid posts")
  parser.add_argument("-o", "--output", type=str, default="PRC_Post.txt", help="Write post text to file indicated here")
  args = parser.parse_args()
  return timedelta(days=args.weeks * 7), args.pages, args.output

def print_parameters(parameters):
  print "Gathering Posts from " + str(parameters[0].days) + " days ago."
  print "Searching last " + str(parameters[1]) + " pages of thread."
  print "Outputting to file: " + parameters[2]
  
if __name__ == "__main__":
  # Parse Parameters
  parameters = arg_parse()
  print_parameters(parameters)
  # Get the final two pages of script
  final_pages = get_last_pages(parameters[1])
  # store each posts link, poem_title, and commenters name in array poem_comment_links
  poem_comment_links = get_posted_poems(final_pages, parameters[0])
  # write posts from poem_comment_links and other needed text for post to "PRC_Post.txt"
  write_post_to_file(poem_comment_links, parameters[2])