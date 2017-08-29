#Before running this :
#
#create a praw.ini file with the following format:
#[bot]
#client_id = 
#client_secret = 
#password = 
#username = 

import praw
import re
import pdb
import time
import os

# all the words that you want to check
flagged_words = ["other", "edit", "all"]

# any messages to be put
pre_message = "Please consider removing " 
post_message = "from the flair title"


# to log in
def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit('bot', user_agent = 'RPromoteReddit bot v1.0 by u/mjguru')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit


def main():
	reddit = authenticate()
	while True :
		run_bot(reddit)
		# 30 second break to go easy on the traffic
		time.sleep(30)

def run_bot(reddit):
	# choose any subreddit
	subreddit = reddit.subreddit("PRomoteReddit")

	# commented.txt contains the id of those submissions on which we have already commented
	if not os.path.exists("commented.txt"):
	    posts_replied_to = []
	else :
		with open("commented.txt", "r") as f:
			posts_replied_to = f.read()
			posts_replied_to = posts_replied_to.split("\n")
			posts_replied_to = list(filter(None, posts_replied_to))

	# choose any limit
	for submission in subreddit.new(limit = 30):
		# 2 second break as we are allowed 30 commments per minute
		time.sleep(2)
		flair =  submission.link_flair_text
		if submission.id not in posts_replied_to and isinstance(flair, unicode):
			flair.encode('ascii', 'ignore')
			got_it = 0
			error_entry = "-1" 
			for flagged in flagged_words :
				if re.search(flagged, flair, re.IGNORECASE):
					got_it = 1
					error_entry = flagged
			if got_it == 1:
				submission.reply(pre_message + error_entry + post_message)
				print ("Replied to ", submission.title, " with flair ", flair)

				posts_replied_to.append(submission.id)
				with open("commented.txt", "a+") as f:
					f.write(submission.id + "\n")

if __name__ == '__main__':
	main()



