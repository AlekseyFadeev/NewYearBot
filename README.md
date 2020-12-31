# New Year Bot
Сгенерированные GPT-2 поздравления с Новым 2021 годом.
Используется предобученная модель GPT-2: https://huggingface.co/gpt2, с fine-tune'ом на новогодних и рождественских поздравлениях.
Перевод на русский язык осуществляется посредством второй модели: https://huggingface.co/Helsinki-NLP/opus-mt-en-ru

Сервис в виде интерактивного jupyter notebook'а на основе виджетов может быть развёрнут по следующей ссылке:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GordonShedds/NewYearBot/master?urlpath=%2Fvoila%2Frender%2Fcongratulate.ipynb)

Для ускорения развёртывания сервис выбирает одно поздравление из базы заранее сгенерированных.
