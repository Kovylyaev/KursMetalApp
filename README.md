# KursMetalApp

## Курсовой проект Metals
Проект по анализу микроструктур сталей с применением машинного обучения для предсказания процентного содержаний желеаза Fe в сплаве на снимке с микроскопа. И интеграция модели на сайт.

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

3. Инициализируйте DVC и получите данные:
   ```bash
   dvc pull
   ```

4. Запустите эксперименты в `notebooks/metals-demo.ipynb`

## Зависимости
- Python 3.9+
- остальные в requirements.txt

## Лицензия
Проект распространяется под лицензией X11 (MIT).
