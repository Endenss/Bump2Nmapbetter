# 🖼️ Texture Converter Pro | Конвертер текстур для S.T.A.L.K.E.R

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-%233776AB?logo=python)](https://python.org)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-%2341CD52?logo=qt)](https://pypi.org/project/PyQt5/)
[![License MIT](https://img.shields.io/badge/License-MIT-%23green)](LICENSE)
[![Version 1.0](https://img.shields.io/badge/Version-1.0-%23blueviolet)](CHANGELOG.md)

**Профессиональный инструмент** для конвертации и обработки игровых текстур (DDS/PNG) с удобным графическим интерфейсом.

---

## 🌟 Основные возможности

### 🔄 Конвертация форматов
- DDS ↔ PNG взаимное преобразование
- Пакетная обработка файлов
- Сохранение альфа-канала

### 🛠️ Специализированные функции
| Функция | Описание |
|---------|----------|
| **Bump → Normal** | Генерация normal-карт из bump-текстур |
| **Извлечение Roughness** | Автоматическое получение карт шероховатости |
| **Создание Specular** | Генерация specular-карт |
| **Пакетная обработка** | Массовая конвертация по шаблонам |

### 🖥️ Интерфейс
- Темная тема с анимированными элементами
- Вкладки для разных форматов (DDS/PNG)
- Гибкие настройки конвертации
- Визуализация прогресса

---

## 📦 Установка

1. Убедитесь, что установлен [Python 3.10+](https://python.org)
2. Установите зависимости:
```bash
pip install PyQt5 numpy imageio
Скачайте последнюю версию программы

🚀 Использование
bash
Copy
python texture_converter.py
Примеры работы:
Массовая конвертация DDS → PNG

Выберите режим "Глобальная обработка"

Укажите папку с текстурами

Нажмите "Конвертировать"

Создание normal-карты

Включите режим "Конвертация bump в normal"

Выберите файлы *_bump.dds

Укажите выходную папку

Извлечение roughness

Активируйте режим "Извлечение roughness"

Выберите файлы *bump#.png

Настройте параметры сохранения

📂 Поддерживаемые форматы
Тип	Входные форматы	Выходные форматы
Текстуры	.dds, .png	.dds, .png
Bump-карты	*_bump.*	*_nmap.*
Roughness	*bump#.*	*roughness.*
🛠 Технические детали
Алгоритм преобразований
python
Copy
def convert_bump_to_normal(img):
    height_data = img[:,:,1].astype(np.float32) / 255.0
    normal_map = np.zeros_like(img)
    normal_map[:,:,2] = (height_data * 255).astype(np.uint8)  # Синий канал
    normal_map[:,:,0] = 128  # Красный (нейтральный)
    normal_map[:,:,1] = 128  # Зеленый (нейтральный)
    return normal_map
Структура проекта
Copy
texture_converter/
├── icons/          # Графические ресурсы
├── presets/        # Шаблоны настроек
└── texture_converter.py  # Основной код
📜 Лицензия
MIT License © 2023 [Ваше имя/компания]

🤝 Участие в разработке
Форкните репозиторий

Создайте ветку для новой фичи (git checkout -b feature/AmazingFeature)

Сделайте коммит (git commit -m 'Add amazing feature')

Запушьте изменения (git push origin feature/AmazingFeature)

Откройте Pull Request

Open in GitHub
