#!/usr/bin/python3
from requests import *
from bs4 import BeautifulSoup as BS
from os import mkdir
import re, os.path, json

class PhotoExtractor:
	def __init__(self):
		self.author = "SEKODE"
		self.r = Session()
		self.auth = 0
		self.photo_url = []
	def login(self, email, password):
		if os.path.isfile(email + ".session"):
			with open(email + ".session") as f:
				self.r.cookies.update(json.loads(f.read()))
				self.auth = 1
				return 1
		self.r.get('https://m.facebook.com')
		self.r.post('https://m.facebook.com/login.php', data={
			'email': email,
			'pass': password
		}, allow_redirects=False)
		if 'c_user' in self.r.cookies:
			uid = dict(self.r.cookies)['c_user']
			with open(email + ".session", "w") as f:
				f.write(json.dumps(dict(r.cookies)))
				self.auth = 1
				return True
		print("*Login Failed")
		return 0
	def get_photos(self, user, limit = 12):
		s = self.r.get("https://m.facebook.com/" + user).text
		bs = BS(s, 'html.parser')
		url_photo = [x.get('href') for x in bs.find_all('a') if "photos" in str(x)][0]
		s = self.r.get("https://m.facebook.com/" + url_photo).text
		bs = BS(s, 'html.parser')
		url_photo = [x.get('href') for x in bs.find_all('a') if "photoset" in str(x)][0] + "&offset="
		for i in range(limit // 12):
			s = self.r.get("https://m.facebook.com/" + url_photo + str(i * 12)).text
			bs = BS(s, 'html.parser')
			if len(bs.select('a')) > 0:
				self.photo_url += [x.get('href') for x in bs.find_all('a') if "photo.php" in str(x)]
			else:
				break
		return "*Getting %s Photo " % len(self.photo_url)
	def export(self, folder):
		result = []
		if len(self.photo_url) > 0:
			mkdir(folder) if not os.path.isdir(folder) else None
			for no, photo in enumerate(self.photo_url):
				s = self.r.get("https://m.facebook.com/" + photo).text
				bs = BS(s, 'html.parser')
				link = bs.select('div#root img')[0]		
				fn = '{}/{}.png'.format(folder, no)
				with open(fn,'wb') as f:
					f.write(self.r.get(link['src']).content)
					result.append(fn)
		res = len(result)
		if res:
			print("*Success Export {} Photo to Folder {}".format(res, folder))
		else:
			print("*Error Export Photo")