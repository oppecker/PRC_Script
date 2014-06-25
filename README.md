PRC_Script
==========

Created by: Daniel Oppecker

Create and post the text for the weekly PRC (poetry running contest) on mtgsalvation.

Files:
PRC_New_Round_Post.py:        script to create and post the text for the weekly PRC (poetry running contest) on mtgsalvation.
PRC_Next_Round_Post.py:       script to post the alert that the submission time for one round is over, and the next is starting.
PRC_Submission_Time_Extended: script to post the alert that not enough poems were submitted so submission period is extended.

PRC_Forum_Tools.py: contains PRCForumTools class with useful methods to use in the script files.
prc_script_vars.py: contains 

account_info.txt:   holds the login information to use. (This file contains fake place-holder values, add real ones to run script)
PRC_Post.txt:       The text created by PRC_New_Round_Post.py and used by mtg_login.py. Included here to show example post text.

Running the scripts:
Run PRC_New_Round_Post.py to create and post the text for a new round.