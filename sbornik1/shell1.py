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
