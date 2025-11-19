# SmartLocker Control Center

Полноценное приложение PySide6 для управления вендинговым шкафом с контроллером Kerong CU24 и сервоблоком. Поддерживаются выдача/загрузка предметов, журнал в SQLite, экспорт/импорт Excel, автопоиск COM-портов, watchdog.

## Структура проекта
```
vending_app/
├── config.json             # Настройки
├── main.py                 # Точка входа GUI
├── serial/                 # Драйверы Kerong и серводрайвер
├── gui/                    # PySide6 интерфейс
├── services/               # Бизнес-логика, контроллер, watchdog
├── db/                     # Работа с SQLite
├── logs/                   # app.log и device.log
```

## Зависимости
```
pip install -r requirements.txt
```
`requirements.txt` находится рядом и включает PySide6, pyserial, openpyxl и вспомогательные пакеты.

## Запуск в режиме разработки
```
python -m vending_app.main
```

## Сборка Windows .EXE (PyInstaller)
1. Установите PyInstaller: `pip install pyinstaller`
2. Выполните из каталога `backend/vending_app`:
   ```
   pyinstaller --noconsole --onefile --name SmartLocker main.py
   ```
3. Готовый `SmartLocker.exe` будет в `dist/`. Файл `config.json` и каталог `logs/` можно положить рядом либо прописать путь в конфиге.

## Перенос на Raspberry Pi
Код модульный: драйверы и бизнес-логика отделены от GUI. Для headless-режима достаточно заменить PySide6-клиент на CLI/web, переиспользовав `services/` и `serial/`.

## Конфигурация
`config.json` определяет:
- `databasePath` — путь к SQLite
- `kerong` и `servo` — параметры COM-портов и скоростей
- `watchdog` — период проверки и количество попыток

## Логи
`logs/app.log` — общие события. `logs/device.log` — низкоуровневые обмены.
