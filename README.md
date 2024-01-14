## Project
<h1>Проект - Телеграм бот для получения погодных данных</h1>

![Иллюстрация к проекту](https://github.com/darkfos/t_wthr/blob/main/Screenshot_1.png)

## About

<p>С помощью данного бота вы сможете</p>
<ul>
  <li>Узнать текущие погодные данные</li>
  <li>Получить данные за 5 дней</li>
  <li>Узнать ближащие города</li>
  <li>Получить уникальные сведения о городе</li>
  <li>Оставить свой отзыв</li>
</ul>

## Documentation

<h4>Имеется следующий перечень команд</h4>
<b>/start</b> - <p>запуск бота, выбор города для показа текущих погодных данных</p>
<b>/help</b> - <p>ознакомление с функционалом бота</p>
<b>/name_city</b> - <p>показ уникальных данных о поселении</p>
<b>/neighbors</b> -<p>вывод ближащих городов к объекту</p>
<b>/weather_5d</b> - <p>прогноз погоды на следующие 5 дней</p>
<b>/review</b> - <p>возможность оставить свой отзыв</p>

## Developers

- [darkfos](https://github.com/darkfos)

## How to install
<p>Создание виртуального окружения</p>
```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```

<p>Установка всех пакетов</p>
```python
pip3 install -r requirements.txt
```

<p>Нужные Api key</p>
- [AccuWeather](https://developer.accuweather.com/)
<p>Так же понадобится API key от Telegram</p>
- [BotFather](https://t.me/BotFather)

