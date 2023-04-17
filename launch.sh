#!/bin/zsh

pip install virtualenv
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

python3 main.py --help

# пример команды
# python3 main.py <path to the file to be encrypted/decrypted> <path to the file with the result> -m encrypt -c vigener -k что