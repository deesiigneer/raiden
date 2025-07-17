# ⚡ Raiden

Raiden — это асинхронный Discord-бот на базе [nextcord](https://github.com/nextcord/nextcord) с интеграцией библиотеки [pyspapi](https://github.com/deesiigneer/pyspapi), разработанный для расширенного взаимодействия с API и удобной архитектуры через Cogs.

## 📦 Зависимости

- [`nextcord`](https://pypi.org/project/nextcord/)
- [`pyspapi`](https://pypi.org/project/pyspapi/)
- `aiohttp`

Установка зависимостей:

```bash
pip install -r requirements.txt
```

## 🚀 Быстрый старт

```bash
python main.py
```

### Не забудьте настроить переменные окружения

Добавьте необходимые токены и ключи в `.env` файл или переменные среды:

- `DISCORD_TOKEN` — токен вашего бота
- другие переменные API (если используются)

## 🧠 Основные возможности

- Асинхронный запуск и управление ботом
- Загрузка `cogs` на старте
- Поддержка команд и событий
- Расширяемость через отдельные модули

## 📝 Лицензия

Проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

---

Разработка: [deesiigneer](https://github.com/deesiigneer)
