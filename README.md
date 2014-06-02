PRC_Script
==========

Create the text for the weekly poetry running contest on mtgsalvation

Functions in prc_script:

get_last_pages():
Uses urllib2 and beautifulsoup4 to get the html of 'http://www.mtgsalvation.com/forums/creativity/personal-writing/494511-poetry-running-contest-submission-thread'
Then use the page navigation links from the top of the page to determine the links to the final two pages of the thread.
Only the final two pages are needed because of relatively low number of weekly submissions, and the limit of 12 poems per round.
Function returns an array of size 2 containing the two links. (should return a tuple)

get_posted_poems(final_pages, time_frame):
Takes final_pages (the links to the final two pages),and time_frame (num weeks back get poems from).
For each of the final two pages, we get the pages html and parse through it using beautifulsoup4.
Gets all the posts to the thread from each page, (checking for a TypeError exception to be thrown, the site recently changed and caused this step to be necessary...)
For each post, collect: The posts date, text, poster name, and title of the poem (just grabbing the first line of the post for the poem title, this part isn't an exact science as a title is not required and sometimes weird formatting of the title causes this value to be None, in which case the script sets the value to the string "None" and I deal with it manually)
Next the script uses the posts date to determine if the post should be added to the array of posts to be used. (should check for this before collecting everything else...)
Finally the array of formatted links, titles and authors is returned.

write_post_to_file(poem_comment_links):
***Since User can now specify, need to make sure the file can be made and is made correctly (try statement)
Accepts the array of formatted links, titles and authors returned by get_posted_poems.
Then opens up file "PRC_Post.txt" and writes the contents of the post to that file.

arg_parse():
***Script should have parameter for choosing your own name for "PRC_Post.txt" (default to PRC_Post.txt)
***Script should have parameter to choose how many of the final pages to read. (default to two) (maybe limit size too?)
Uses argparse to parse the parameters sent to the function.
If no parameters are used, the default of one week is used.
Function returns the timedelta of the number for weeks times 7 to set the correct amount of days.
