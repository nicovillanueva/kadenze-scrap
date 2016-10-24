#!/usr/bin/env python3

import time
import re
import argparse
import requests
from selenium import webdriver

vids = {}
mail = ''
pwd = ''
default = 'https://www.kadenze.com/courses/'

parser = argparse.ArgumentParser()
parser.add_argument('--browser', type=str, default='chrome', help='Browser to use. "firefox", "chrome". Defaults to "chrome"')
parser.add_argument('--progress', type=bool, default=False, help='Show download speed or not. "true", "false". Defaults to "false"')
args = parser.parse_args()

# -----------

def save_and_next():
	e = d.find_elements_by_tag_name("video")[0]
	url = e.get_attribute("src")
	fname = re.search("file/(.+)\?", url).groups()[0]
	print("Found {}".format(fname))
	vids[fname] = url
	d.execute_script("document.getElementsByClassName(\"vjs-skip-forward\")[0].style.display='block'")
	d.find_element_by_class_name("vjs-skip-forward").click()
	time.sleep(1)

def scrape_session(s):
	print("Scrapping {}".format(s))
	d.get(s)
	vid_amount = len(d.find_element_by_class_name("video-queue__content").find_elements_by_tag_name("li"))
	for i in range(vid_amount):
		save_and_next()

def download_all():
	for k, v in vids.items():
		cont = requests.get(v, stream=True)
		with open(k, "wb") as f:
			if args.progress:
				from tqdm import tqdm
				for data in tqdm(cont.iter_content(chunk_size=1024), desc=k, unit="bytes", unit_scale=False):
					f.write(data)
			else:
				print("Downloading: {}".format(k))
				for data in cont.iter_content(chunk_size=1024):
					f.write(data)


# -----------

if mail == "" or pwd == "":
	print("Mail or password not found in source. Set them now:")
	mail = input("E-Mail address: ")
	pwd = input("Password: ")

if args.browser == "chrome":
	d = webdriver.Chrome()
elif args.browser == "firefox":
	d = webdriver.Firefox()
#elif args.browser == "phantomjs":  # not working :(
#	d = webdriver.PhantomJS()
else:
	print("What the fuck was that? Defaulting to Chrome")
	d = webdriver.Chrome()

d.get("https://www.kadenze.com/sign_in")
print("Logging in as {}".format(mail))
d.find_element_by_id("login_user_email").send_keys(mail)
d.find_element_by_id("login_user_password").send_keys(pwd)
d.find_element_by_id("login_user_password").submit()

d.get(default)

print("""Enter a session URL, and press ENTER. Keep adding to enqueue. Blank line to finalize input.
Ctrl+C to abort.
""")

targets = []
target = input()
while target != "":
	targets.append(target)
	target = input()
if len(targets) == 0:
	print("Aborting")
	exit(0)

for sess in targets:
	scrape_session(sess)
	d.get(default)
	download_all()
	vids.clear()

d.quit()
print("All done.")
