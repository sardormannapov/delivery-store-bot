include .env
run:
	python3 bot.py

bot:
	 telegram-bot-api   --api-id=${API_ID} --api-hash=${API_HASH} --local

venv:
	python3 -m venv venv

requirements:
	pip3 freeze > requirements.txt

pip:
	pip3 install -r requirements.txt
