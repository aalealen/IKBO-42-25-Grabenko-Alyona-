import argparse
import sys
from shell import ShellEmulator
def main():
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки ОС (Практическая работа №1, Вариант №8)"
    )
    parser.add_argument('--vfs', help='Путь к физическому расположению VFS (ZIP)')
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
