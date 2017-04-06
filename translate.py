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
	CHOICE = "번역할 언어를 선택해주세요."
	KOREAN = 'ko'
	JAPANESE = 'ja'
	ENGLISH = 'en'
	CHINESE = 'zh-CN'
	MENU0 = '언어'
	MENU1 = '영어'
	MENU2 = '일본어'
	MENU3 = '중국어(간체)'
	MENU4 = '다시 입력'
	context = ''
	mode = ''
	command = ''

	global scheduler

	def __init__(self, *args, **kwargs):
		super(euler, self).__init__(*args, **kwargs)

	def open(self, initial_msg, seed):
		self.sender.sendMessage(self.GREETING)

	def menu(self):
		self.mode = ''

	def language(self):
		self.mode = self.MENU0
		self.input_lang = self.KOREAN
		show_keyboard = {'keyboard': [[self.MENU1],  [self.MENU2], [self.MENU3]]}
		self.sender.sendMessage(self.CHOICE, reply_markup=show_keyboard)

	def translate(self, sentence):
		self.mode = ''
		hide_keyboard = {'hide_keyboard': True}
		encText = urllib.parse.quote(sentence)
		data = "source=" + self.input_lang + "&target=" + self.output_lang + "&text=" + encText
		url = "https://openapi.naver.com/v1/language/translate"
		request = urllib.request.Request(url)
		request.add_header("X-Naver-Client-Id",client_id)
		request.add_header("X-Naver-Client-Secret",client_secret)
		response = urllib.request.urlopen(request, data=data.encode("utf-8"))
		rescode = response.getcode()
		if(rescode==200):
			response_body = response.read().decode('utf-8')
			data = json.loads(response_body)
			self.sender.sendMessage(data['message']['result']['translatedText'], reply_markup=hide_keyboard)
			self.menu()
		else:
		    print("Error Code:" + rescode)
	def handle_command(self, command):
		if self.mode == self.MENU0:
			if command == self.MENU1:
				self.output_lang = self.ENGLISH
				self.translate(self.context)
			elif command == self.MENU2:
				self.output_lang = self.JAPANESE
				self.translate(self.context)
			elif command == self.MENU3:
				self.output_lang = self.CHINESE
				self.translate(self.context)
		else:
			if re.match(u'[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7A3]+', command) is not None:
				self.context = command
				self.input_lang = self.KOREAN
				self.language()
			else:
				self.output_lang = self.KOREAN
				if re.match(u'[\u0061-\u007a\u0041-\u005a]+', command) is not None:
					self.input_lang = self.ENGLISH
				elif re.search(u'[\u2E80-\u2EFF\u31C0-\u31EF\u3200-\u32FF\u3400-\u4DBF\u4E00-\u9FBF\uF900-\uFAFF\u20000-\u2A6DF\u2F800-\u2FA1F]+', command) is not None:
					if re.search(u'[\u3040-\u309F\u30A0-\u30FF]+', command) is not None:
						self.input_lang = self.JAPANESE
					else:
						self.input_lang = self.CHINESE
				self.translate(command)

	def on_message(self, msg):
		content_type, chat_type, chat_id= telepot.glance(msg)

		if content_type is 'text':
			self.handle_command(msg['text'])
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
