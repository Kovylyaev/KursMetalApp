# KursMetalApp

## Курсовой проект Metals
Проект по анализу микроструктур сталей с применением машинного обучения для предсказания процентного содержаний желеаза Fe в сплаве по снимку с микроскопа. И интеграция модели на сайт.

## Полезные ссылки
- [Отчёт Wandb по проведённым экспериментам](https://api.wandb.ai/links/sasha_kovylyaev-hse/vflkfsup)
- [Главный GitHub репозиторий с экспериментов](https://github.com/Kovylyaev/Metals/)
- TODO [Ссылка на сам сайт] <!--(https://example.com) -->

## Проект включает:
- Простой Django проект с сайтом, загруженной моделью и возможностью получить её предсказание.

## Структура репозитория
- `DL/` — файлы модели и scaler'а
- `media/` — сохранённые изображения, которые моделе через сайт
- `templates/` — html-страницы
- `home/` и `KursMetalApp/` — папки Django проекта
- `db.sqlite3` — база данных сайта
- `requirements.txt` - зависимости проекта

 ## Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Kovylyaev/KursMetalApp.git
   cd KursMetalApp
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите сайт:
   ```bash
   python manage.pu runserver
   ```

## TODO выложить сайт в публичный доступ

   
## Зависимости
- Python 3.12.4+
- остальные в requirements.txt

## Лицензия
Проект распространяется под лицензией X11 (MIT).
