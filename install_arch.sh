#!/bin/bash

# Обновление базы данных пакетов
sudo pacman -Syu

# Установка Arch-пакетированных библиотек Python, если они еще не установлены
sudo pacman -S --needed python-requests python-pillow

# Установка pipx, если он еще не установлен
if ! command -v pipx &> /dev/null; then
    sudo pacman -S python-pipx
fi

# Установка библиотек с помощью pipx
pipx install --force ffmpeg-python
pipx install --force yt-dlp
pipx install --force vosk
pipx install --force tqdm

# Создание виртуального окружения для установки оставшихся библиотек
python -m venv myenv  # Создание виртуального окружения с именем "myenv"
source myenv/bin/activate  # Активация виртуального окружения

# Установка библиотек из requirement.txt
pip install -r requirement.txt

# Деактивация виртуального окружения после завершения
deactivate
