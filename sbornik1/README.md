# Практическая работа №1 из сборника (Вариант №8)
## Эмулятор оболочки ОС
**Выполнила:** Грабенко Алёна Андреевна, ИКБО-42-25
**Цель:** разработать эмулятор для языка оболочки ОС, работающий по принципу командной строки UNIX-подобной ОС.
## Этап 1. REPL
**Цель этапа:** создать минимальный прототип. Большинство функций пока представляют собой заглушки, но диалог с пользователем уже поддерживается.
**Реализовано:**
- Консольное приложение (CLI)
- Приглашение к вводу содержит имя VFS: `default_vfs:~$`
- Парсер с раскрытием переменных окружения реальной ОС (`$HOME`, `$USER` и др.)
- Команды-заглушки `ls` и `cd` выводят своё имя и аргументы
- Команда `exit` для выхода
- Обработка ошибок: неизвестная команда, неверное число аргументов

**Структура:**
- **`main.py`** - точка входа
```python
from shell import ShellEmulator
def main():
    shell = ShellEmulator()
    shell.run()
if __name__ == '__main__':
    main()
```
- **`shell.py`** - REPL и обработка команд
```python
import os
import shlex
class ShellEmulator:
    """Эмулятор оболочки ОС. Этап 1: базовый REPL."""
    def __init__(self):
        self.vfs_name = "default_vfs"
        self.running = True
    def expand_env(self, text):
        return os.path.expandvars(text)
    def parse_command(self, line):
        line = self.expand_env(line)
        try:
            return shlex.split(line)
        except ValueError as e:
            raise ValueError(f"Ошибка парсинга: {e}")
    def cmd_ls(self, args):
        print(f"[ls] имя команды: ls")
        print(f"[ls] аргументы: {args}")

    def cmd_cd(self, args):
        print(f"[cd] имя команды: cd")
        print(f"[cd] аргументы: {args}")
    def cmd_exit(self, args):
        if args:
            print("exit: команда не принимает аргументов")
            return
        self.running = False
    def execute(self, line):
        line = line.strip()
        if not line or line.startswith('#'):
            return

        try:
            tokens = self.parse_command(line)
        except ValueError as e:
            print(f"Ошибка: {e}")
            return

        if not tokens:
            return

        cmd, args = tokens[0], tokens[1:]

        if cmd == 'ls':
            self.cmd_ls(args)
        elif cmd == 'cd':
            self.cmd_cd(args)
        elif cmd == 'exit':
            self.cmd_exit(args)
        else:
            print(f"{cmd}: команда не найдена")

    def get_prompt(self):
        return f"{self.vfs_name}:~$ "

    def run(self):
        while self.running:
            try:
                line = input(self.get_prompt())
            except (EOFError, KeyboardInterrupt):
                print()
                break
            self.execute(line)
```
**Запуск**
Создание файлов и переход в папку:
```bash
cd ~
mkdir -p sbornik1/scripts sbornik1/vfs_samples
cd sbornik1
nano shell.py
nano main.py
ls -l
```
Запуск эмулятора:
```bash
python3 main.py
```
**Результат работы:**
<img width="1078" height="742" alt="image" src="https://github.com/user-attachments/assets/57a341b2-e0fd-40c7-9349-6d078bbb1901" />

## Этап 2. Конфигурация
**Цель этапа:** сделать эмулятор настраиваемым - поддержать параметры командной строки, стартовый скрипт и отладочный вывод.
**Реализовано:**
- Параметры командной строки `--vfs` (путь к VFS) и `--script` (путь к стартовому скрипту)
- Отладочный вывод всех заданных параметров при запуске
- Стартовый скрипт с поддержкой комментариев (`#`)
- При выполнении скрипта на экран выводится и ввод, и вывод - имитация диалога
- Обработка ошибок в скрипте (не прерывает работу)
- Служебная команда `conf-dump` - вывод параметров в формате ключ-значение
- Bash-скрипты для тестирования запуска с разными параметрами

**Обновлённый `main.py`**
```python
import argparse
import sys
from shell import ShellEmulator
def main():
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки ОС (Практическая работа №1, Вариант №8)"
    )
    parser.add_argument('--vfs', help='Путь к физическому расположению VFS')
    parser.add_argument('--script', help='Путь к стартовому скрипту')
    args = parser.parse_args()
    try:
        shell = ShellEmulator(vfs_path=args.vfs, script_path=args.script)
        shell.run()
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        sys.exit(1)
if __name__ == '__main__':
    main()
```
**Обновлённый shell.py**
```python
import os
import shlex
class ShellEmulator:
    """Эмулятор оболочки ОС. Этап 2: конфигурация."""
    def __init__(self, vfs_path=None, script_path=None):
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.vfs_name = os.path.basename(vfs_path).rsplit('.', 1)[0] if vfs_path else "default_vfs"
        self.running = True
    def expand_env(self, text):
        return os.path.expandvars(text)

    def parse_command(self, line):
        line = self.expand_env(line)
        try:
            return shlex.split(line)
        except ValueError as e:
            raise ValueError(f"Ошибка парсинга: {e}")

    def cmd_ls(self, args):
        print(f"[ls] имя команды: ls")
        print(f"[ls] аргументы: {args}")

    def cmd_cd(self, args):
        print(f"[cd] имя команды: cd")
        print(f"[cd] аргументы: {args}")

    def cmd_conf_dump(self, args):
        if args:
            print("conf-dump: команда не принимает аргументов")
            return
        print(f"vfs_path    = {self.vfs_path}")
        print(f"script_path = {self.script_path}")
        print(f"vfs_name    = {self.vfs_name}")

    def cmd_exit(self, args):
        if args:
            print("exit: команда не принимает аргументов")
            return
        self.running = False

    def execute(self, line):
        line = line.strip()
        if not line or line.startswith('#'):
            return

        try:
            tokens = self.parse_command(line)
        except ValueError as e:
            print(f"Ошибка: {e}")
            return

        if not tokens:
            return

        cmd, args = tokens[0], tokens[1:]

        if cmd == 'ls':
            self.cmd_ls(args)
        elif cmd == 'cd':
            self.cmd_cd(args)
        elif cmd == 'conf-dump':
            self.cmd_conf_dump(args)
        elif cmd == 'exit':
            self.cmd_exit(args)
        else:
            print(f"{cmd}: команда не найдена")

    def get_prompt(self):
        return f"{self.vfs_name}:~$ "

    def run_script(self, path):
        if not os.path.exists(path):
            print(f"Ошибка: стартовый скрипт не найден: {path}")
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for lineno, line in enumerate(f, 1):
                    raw = line.rstrip('\n')
                    print(f"{self.get_prompt()}{raw}")
                    try:
                        self.execute(raw)
                    except Exception as e:
                        print(f"Ошибка в строке {lineno}: {e}")
                    if not self.running:
                        break
        except Exception as e:
            print(f"Ошибка чтения скрипта: {e}")

    def run(self):
        print(f"[debug] vfs_path    = {self.vfs_path}")
        print(f"[debug] script_path = {self.script_path}")
        print(f"[debug] vfs_name    = {self.vfs_name}")
        print()

        if self.script_path:
            self.run_script(self.script_path)
        else:
            while self.running:
                try:
                    line = input(self.get_prompt())
                except (EOFError, KeyboardInterrupt):
                    print()
                    break
                self.execute(line)
```
**Стартовые скрипты**
`scripts/basic.txt:`
```bash
ls
ls -l /home
cd /tmp
cd $HOME
conf-dump
exit
```

`scripts/errors.txt`:
```bash
ls
unknowncommand
exit extra_arg
cd
conf-dump extra_arg
exit
```
`scripts/full.txt:`
```bash
# Полный скрипт: все команды и $HOME
ls
ls -l /home
ls dir1 dir2
cd /tmp
cd $HOME
cd
conf-dump
unknowncommand arg1 arg2
exit
```
**Bash-скрипты для тестирования**
`scripts/run_no_args.sh:`
```bash
#!/bin/bash
cd "$(dirname "$0")/.."
python3 main.py
```
`scripts/run_script.sh:`
```bash
#!/bin/bash
cd "$(dirname "$0")/.."
python3 main.py --script scripts/basic.txt
```
`scripts/run_vfs.sh:`
```bash
#!/bin/bash
cd "$(dirname "$0")/.."
python3 main.py --vfs sample.zip --script scripts/basic.txt
```
**Запуск**
Без параметров:
```bash
python3 main.py
```
Со стартовым скриптом:
```bash
python3 main.py --script scripts/basic.txt
```
С VFS и скриптом:
```bash
python3 main.py --vfs myvfs.zip --script scripts/basic.txt
```
Через bash-скрипт:
```bash
./scripts/run_script.sh
```
**Результаты работы:**
Запуск без параметров и `conf-dump`:
<img width="799" height="466" alt="image" src="https://github.com/user-attachments/assets/2d4b0237-b56e-4b80-b275-e4719c3ed9d1" />

Запуск со стартовым скриптом `scripts/basic.txt`:
<img width="823" height="537" alt="image" src="https://github.com/user-attachments/assets/aef0912d-358f-42f8-8ad3-8d9e5dfdf7ed" />

Запуск с VFS `myvfs.zip` — имя VFS в приглашении изменилось на `myvfs`:
<img width="936" height="540" alt="image" src="https://github.com/user-attachments/assets/fd74bb3d-4311-4bad-b6fe-616bbea86a9d" />

Запуск со скриптом ошибок `scripts/errors.txt`:
<img width="823" height="440" alt="image" src="https://github.com/user-attachments/assets/35185a33-6bd6-4311-b5eb-17dfcc0b8ac4" />

Запуск через bash-обёртку `./scripts/run_script.sh`:
<img width="777" height="565" alt="image" src="https://github.com/user-attachments/assets/0d66b358-d4f1-4393-92af-da4427616ec5" />



