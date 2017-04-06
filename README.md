# **Euler** [![einstein](https://img.shields.io/badge/telegram-euler-blue.svg)](https://telegram.me/euler_translate_bot)

This is Telegram messenger BOT translate the text which are extracted 4 language which are Korean, English, Japanese, Chinese from the message that user sent.

## **Installation**

+ install python packages
```bash
$ pip3 install telepot
```
 and, it will be needed to add your bot token in *settings.json* file
 You should create your bot with @Botfather in telgram.
 Then, you can get your token using  */token*  message.
 *For more details: http://telepot.readthedocs.io/en/latest/*

+ Edit setting.json
```json
{
  "common": {
    "token": "123456789:blahblahblahYourBotToken",
    "id": "API_ID",
    "key": "API_SECRET_KEY"
    }
}
```
**YOU SHOULD CHANGE THE NAME setting_example.json FILE TO setting.json**

**token** is your bot token which you got when you make a new bot using *@Botfather*

**id** should be your Naver API id which you can get from  https://developers.naver.com/products/translator/

**key** should be your Naver API secrete key which you can get from  https://developers.naver.com/products/translator/

## **Run**
```bash
$ python3 euler.py
``` 
