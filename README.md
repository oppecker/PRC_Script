PRC_Script
==========

Created by: Daniel Oppecker

Create the text for the weekly poetry running contest on mtgsalvation.

Functions in prc_script:

get_last_pages(pages):
Takes integer variable pages, used to determine the number of page links to return.
Uses urllib2 and beautifulsoup4 to get the html of 'http://www.mtgsalvation.com/forums/creativity/personal-writing/494511-poetry-running-contest-submission-thread'
Then use the page navigation links from the top of the page to determine the links to the final pages of the thread to be used.
Function returns an array containing the links to the pages to be searched through.

get_posted_poems(final_pages, time_frame):
Accepts array final_pages (containing the links of the pages to be searched through),and time_frame (num weeks back to get poems from).
For each page, we get the pages html and parse through it using beautifulsoup4.
Gets all the posts to the thread from each page, (checking for a TypeError exception to be thrown, the site recently changed and caused this step to be necessary...)
For each post, collect: The posts date, posts link, poster name, and title of the poem.
The script uses the posts date to determine if the post should be added to the array of posts to be used.
Finally the array full of formatted links, titles and authors is returned.

write_post_to_file(poem_comment_links, output_file_name):
Accepts the array of links to poems, and name of the file to write the posts text to.
Attempts to open and write to output file, throwing an exception and exiting the script if an error occurs here.

arg_parse():
Uses argparse to parse the parameters sent to the function.
If no parameters are used, the defaults for --weeks, --pages, and --output are used.
Function returns the values of the parameters in a tuple

print_parameters(parameters):
Prints out the values of the parameters that will currently be used.

get_post_link(comment):
Returns string containing the link to the poems post.

get_post_date(comment):
Returns the date the post was posted as a datetime object.

get_poster_name(comment):
Returns the name of the posts author.

get_poem_title(comment):
Returns the title of the poem.
Uses the first line of the post as the poem title, this part isn't an exact science as a title is not required and sometimes weird html tags on the title make this annoying to get. It seems that first checking for .string, then if that returns None, checking for .text instead, I get the first line that I'm looking for. After those two checks I set the poems title to "Error: Could Not Figure Out A Title" to indicate that this should be manually looked at.