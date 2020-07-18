Test Telegram Bot (TTB)
=======================

TTB - бот, цель которого изучение телеграм ботов на python

Установка
---------
Создайте виртуальное акружение, дале в нём выполните:

.. code-block:: text

	pip install -r requirements.txt

Положите картинки котиков в папку images, название файлов должно начинаться с cat и иметь расширение .jpg или .jpeg

Настройка
---------
Создайте файл settings.py, добавьте туда следующие настройки:

.. code-block:: python

	API_KEY = "API ключ, кторый вы получили у BotFather"
	USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

Запуск
------
В виртуальном окружение выполните:

.. code-block:: text

	python3 bot.py