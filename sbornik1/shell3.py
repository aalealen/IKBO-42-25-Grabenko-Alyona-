import os
import shlex
from vfs import VFS


class ShellEmulator:
    """Эмулятор оболочки ОС. Этап 3: VFS."""

    def __init__(self, vfs_path=None, script_path=None):
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.vfs = VFS(vfs_path)
        self.vfs_name = self.vfs.name
        self.current_dir = '/'
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
        path = args[0] if args else self.current_dir
        norm = self.vfs.normalize_path(self.current_dir, path)
        if not self.vfs.exists(norm):
            print(f"ls: {path}: нет такого файла или каталога")
            return
        if self.vfs.is_dir(norm):
            for e in self.vfs.list_dir(norm):
                print(e)
        else:
            print(os.path.basename(norm))

    def cmd_cd(self, args):
        if not args:
            self.current_dir = '/'
            return
        if len(args) > 1:
            print("cd: слишком много аргументов")
            return
        path = args[0]
        norm = self.vfs.normalize_path(self.current_dir, path)
        if not self.vfs.exists(norm):
            print(f"cd: {path}: нет такого файла или каталога")
            return
        if not self.vfs.is_dir(norm):
            print(f"cd: {path}: не является каталогом")
            return
        self.current_dir = norm

    def cmd_conf_dump(self, args):
        if args:
            print("conf-dump: команда не принимает аргументов")
            return
        print(f"vfs_path    = {self.vfs_path}")
        print(f"script_path = {self.script_path}")
        print(f"vfs_name    = {self.vfs_name}")
        print(f"current_dir = {self.current_dir}")

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
        return f"{self.vfs_name}:{self.current_dir}$ "

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
