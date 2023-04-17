# encryption

(функционал еще будет добавляться)


Консольное приложение, с помощью которого можно расшифровать/зашифровать текстовый файл (на русском языке)

Запуск bash-скрипта launch.sh вызывает команду --help, и в консоль выводится документация к использованию приложения.

Чтобы запустить проект, можно запустить скрипт launch.sh, но так как это консольное приложение, командной строке нужно подавать разные аргументы для разных сценариев работы.
Cкрипт только устанавливает все необходимые библиотеки и запускает программу с флагом --help. После чего в терминале появляется описание работы всех флагов и аргументов. 


Чтобы запустить приложение, нужно из папки, в которой находится проект запустить команду python3 main.py со следующими аргументами:

Первыми двумя аргументами вводятся пути к текстовым файлам:  
    1. Файл с текстом для шифровки/расфивровки/взлома шифра input_file (для стеганографии это текст)  
    2. Файл, в который будет записан результат шифровки/расшифровки/взлома шифра output_file (для стеганографии это путь для картинки, которую зашнуруется текст)  

Второй аргумент (необязательный, если input_file имеет кодировку utf-8) -e (--encoding) ENCODING - кодировка файла input_file  

Третий аргумент -m (--mode) MODE: MODE – выбор одного из действий:  
(для стеганографии пока что доступно только шифрование, расшифровка в процессе)  
    - зашифровать: encrypt  
    - расшифровать: decrypt  
    - взломать: hack (только для текстов зашифрованный с помощью шифра Цезаря)  

Если выбрано действие hack, больше аргументы не вводятся. 

Четвертый аргумент -c (--cipher) CIPHER: CIPHER – выбор одного из действий:  
    - шифр Цезаря: caesar  
    - шифр Виженера: vigener  

Пятый аргумент -k (--key) KEY:  
    - для шифра Цезаря: key это shift (число на которое сдвинут текст)  
    - для шифра Виженера: key это строка (последовательность русских букв)  

Также для стеганографии есть аргумент --bmp: файл bmp, который используется, чтобы зашифровать текст (он не меняется, информация шифруется в другой файл bmp)
