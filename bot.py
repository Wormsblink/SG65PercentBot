from datetime import datetime
import time
import pandas as pd

import config
import getlists

def run_bot(r):

	prefix_list = getlists.prefix_list(config.prefixlist)

	for comment in r.subreddit(config.subreddit).comments(limit = config.searchlimit):

		replied_database = getlists.replied_list(config.repliedlist)
		replies_id = replied_database["id"].tolist()
		
		if (check_comment(r, comment, replies_id, prefix_list) == True):
			if (update_database(comment, replied_database) == True):
				
				reply_comment(r, comment, replied_database)

		time.sleep(10)

def check_comment(r, comment, replies_id, prefix_list):
	if any(word in comment.body.lower() for word in prefix_list):

		if comment.id not in replies_id or len(replies_id)==0:
			if comment.author != r.user.me():
				if "bot" not in comment.author.name:
					return True
	else:
		return False

def update_database(comment, replied_database):
	try:
		add_to_database(comment, replied_database)
		return True
	except:
		print("error replying comment id " + comment.id)
		return False

def reply_comment(r, comment, replied_database):
	reply_text = "🎉 **RESET THE COUNTER!!!** 🎉"

	if(replied_database.empty):
		reply_text = add_to_reply(reply_text, "First Mention of the 65%!")
	else:
		reply_text = add_to_reply(reply_text, "it has been " + get_last_time(replied_database) + " since we've had an intellectual discussion about the 65%!")
		reply_text = add_to_reply(reply_text, "Last mention by: " + get_last_user(replied_database) + ":")
		reply_text = add_to_reply(reply_text, "[" + get_last_comment(replied_database) + "](" + get_last_permalink(r, replied_database) + ")")

	if (config.replymode == True):
		comment.reply(reply_text)
	else:
		print(reply_text)
		pass

def add_to_reply(reply_text, new_text):
	reply_text = reply_text + "\n\n" + new_text

	return reply_text

def get_last_time(replied_database):
	last_entry_time = int(replied_database.iloc[-1]["time"])
	current_time = int(time.time())
	time_difference = current_time - last_entry_time

	if (time_difference > 24*3600*2):
		return (str(int(time_difference/24/3600)) + " days")

	elif(time_difference > 3600*2):
		return(str(int(time_difference/3600)) + " hours")

	elif(time_difference>60*2):
		return(str(int(time_difference/60)) + " minutes")
	else:
		return (str(time_difference) + " seconds")

def get_last_user(replied_database):
	last_user = "u/" + replied_database.iloc[-1]["user"]

	return last_user

def get_last_comment(replied_database):
	last_comment = replied_database.iloc[-1]["text"]

	return last_comment

def get_last_permalink(r, replied_database):
	last_permalink = r.comment(replied_database.iloc[-1]["id"]).permalink
	return last_permalink

def add_to_database(comment, replied_database):
	append_to_database = pd.DataFrame({"id": [comment.id], "text": [comment.body], "user": [comment.author.name], "time": [comment.created_utc]})
	
	if replied_database.empty:
		new_database = append_to_database
	else:
		new_database = pd.concat([replied_database, append_to_database])
	
	new_database.to_csv(config.repliedlist)

	return True