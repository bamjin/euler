#!/usr/bin/python3

import sys
import os
import time
import telepot
import json
import requests
import atexit
import re
import random
import string
import operator
import urllib.request

from urllib import parse
from apscheduler.schedulers.background import BackgroundScheduler
from telepot.delegate import per_chat_id, create_open, pave_event_space

CONFIG_FILE = 'setting.json'

class euler(telepot.helper.ChatHandler):

	GREETING = "번역해드립니다."
	KOREAN = 'ko'
	JAPANESE = 'ja'
	ENGLISH = 'en'
	CHINESE = 'zh-CN'

	global scheduler

	def __init__(self, *args, **kwargs):
		super(euler, self).__init__(*args, **kwargs)

	def open(self, initial_msg, seed):
		self.sender.sendMessage(self.GREETING)

	def translate(self, sentence):
		output_lang = self.KOREAN
		if re.match(u'[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7A3]+', sentence) is not None:
			input_lang = self.KOREAN
			output_lang = self.ENGLISH
		elif re.match(u'[\u0061-\u007a\u0041-\u005a]+', sentence) is not None:
			input_lang = self.ENGLISH
		elif re.match(u'[\u3040-\u309F\u30A0-\u30FF]+', sentence) is not None or re.match(u'[\u2E80-\u2EFF\u31C0-\u31EF\u3200-\u32FF\u3400-\u4DBF\u4E00-\u9FBF\uF900-\uFAFF\u20000-\u2A6DF\u2F800-\u2FA1F]+', sentence) is not None:
			input_lang = self.JAPANESE
			if re.match(u'[\u2E80-\u2EFF\u31C0-\u31EF\u3200-\u32FF\u3400-\u4DBF\u4E00-\u9FBF\uF900-\uFAFF\u20000-\u2A6DF\u2F800-\u2FA1F]+', sentence) is not None and re.match(u'[\u3040-\u309F\u30A0-\u30FF]+', sentence) is None:
				input_lang = self.CHINESE

		encText = urllib.parse.quote(sentence)
		data = "source=" + input_lang + "&target=" + output_lang + "&text=" + encText
		url = "https://openapi.naver.com/v1/language/translate"
		request = urllib.request.Request(url)
		request.add_header("X-Naver-Client-Id",client_id)
		request.add_header("X-Naver-Client-Secret",client_secret)
		response = urllib.request.urlopen(request, data=data.encode("utf-8"))
		rescode = response.getcode()
		if(rescode==200):
			response_body = response.read().decode('utf-8')
			data = json.loads(response_body)
			self.sender.sendMessage(data['message']['result']['translatedText'])
		else:
		    print("Error Code:" + rescode)

	def on_message(self, msg):
		content_type, chat_type, chat_id= telepot.glance(msg)

		if content_type is 'text':
			self.translate(msg['text'])
			return

	def on_close(self, exception):
		pass

def parseConfig(filename):
	f = open(filename, 'r')
	js = json.loads(f.read())
	f.close()
	return js

def getConfig(config):
	global TOKEN
	global client_id
	global client_secret

	TOKEN = config['common']['token']
	client_id = config['common']['id']
	client_secret = config['common']['key']


config = parseConfig(CONFIG_FILE)

if not bool(config):
	print("Err: Setting file is not found")
	exit()

getConfig(config)
scheduler = BackgroundScheduler()
scheduler.start()
bot = telepot.DelegatorBot(TOKEN, [
	pave_event_space()
	(per_chat_id(), create_open, euler, timeout=120),
])
bot.message_loop(run_forever='Listening...')
