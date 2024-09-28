#!/bin/bash

# Обновление базы данных пакетов
sudo dnf -y update  # Используйте 'yum' вместо 'dnf' для старых версий

# Установка RPM-пакетированных библиотек Python, если они еще не установлены
sudo dnf install -y python3-requests python3-pillow  # Используйте 'yum' для старых версий

# Установка pipx, если он еще не установлен
if ! command -v pipx &> /dev/null; then
    sudo dnf install -y python3-pipx  # Используйте 'yum' для старых версий
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
