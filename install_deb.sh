#!/bin/bash

# Обновление базы данных пакетов
sudo apt update && sudo apt upgrade -y

# Установка необходимых библиотек Python, если они еще не установлены
sudo apt install -y python3-requests python3-pil python3-venv python3-pip

# Установка pipx, если он еще не установлен
if ! command -v pipx &> /dev/null; then
    python3 -m pip install --user pipx
    # Добавление pipx в PATH
    export PATH="$HOME/.local/bin:$PATH"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
fi

# Установка библиотек с помощью pipx
pipx install --force ffmpeg-python
pipx install --force yt-dlp
pipx install --force vosk
pipx install --force tqdm

# Создание виртуального окружения для установки оставшихся библиотек
python3 -m venv myenv  # Создание виртуального окружения с именем "myenv"
source myenv/bin/activate  # Активация виртуального окружения

# Установка библиотек из requirement.txt
pip install -r requirement.txt

# Деактивация виртуального окружения после завершения
deactivate
