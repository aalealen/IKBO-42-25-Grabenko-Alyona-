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
