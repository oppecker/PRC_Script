PRC_Script
==========

Created by: Daniel Oppecker

Create and post the text for the weekly PRC (poetry running contest) on mtgsalvation.

Files:
prc_script.py:      script to create the text for the weekly PRC (poetry running contest) on mtgsalvation.
mtg_login.py:       script to post the text for the weekly PRC (poetry running contest) on mtgsalvation.
account_info.txt:   holds the login information for mtg_login.py to use. (This file contains fake place-holder values, add real ones to run script)
PRC_Post.txt:       The text created by prc_script.py and used by mtg_login.py. Included here to show example post text.

Running the scripts:
Run prc_script.py to create the text for the post.
Run mtg_login.py to automate posting the new post text to mtgsalvation to create the new round.

Things to note:
Currently mtg_login.py only uses text provided by the default "PRC_Post.txt" location created by prc_script.py. Very soon however mtg_login.py will accept a parameter to select which file to get post text from.

