
"""CLI entry point for the dependency graph tool."""

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse

from apt_parser import get_direct_dependencies, get_dependency_map
from graph import (
    build_graph_bfs_recursive,
    build_reverse_dependency_map,
    print_ascii_tree,
)from test_graph import load_test_graph

DEFAULT_REPOSITORY = (
    "https://archive.ubuntu.com/ubuntu/dists/noble/"
    "main/binary-amd64/Packages.gz"
)

def parse_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Инструмент анализа графа зависимостей пакетов Ubuntu (apt)."
    )

    parser.add_argument(
        "--package",
        required=True,
        help="Имя анализируемого пакета."
    )

    parser.add_argument(
        "--repository",
        default=DEFAULT_REPOSITORY,
        help="URL файла Packages/Packages.gz (Ubuntu apt)."
    )

    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Использовать тестовый граф вместо apt-репозитория."
    )

    parser.add_argument(
        "--test-file",
        default="tests/test_graph.json",
        help="Путь к JSON-файлу тестового графа."
    )

    parser.add_argument(
        "--output",
        default="dependency_graph.mmd",
        help="Имя выходного файла графа."
    )

    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        help="Вывести зависимости в виде ASCII-дерева."
    )

    parser.add_argument(
        "--stage",
        type=int,
        choices=(1, 2, 3, 4),
        default=1,
        help="Этап запуска: 1 — CLI, 2 — прямые зависимости, 3 — граф."
    )

    return parser.parse_args()


def validate_args(args):
    """Validate user-supplied CLI settings."""

    # Проверка имени пакета.
    if not args.package.strip():
        raise ValueError("Имя пакета не должно быть пустым.")

    args.package = args.package.strip()

    # Проверка URL репозитория.
    args.repository = args.repository.strip()

    if not args.repository:
        if not args.test_mode:
            raise ValueError("URL репозитория не должен быть пустым.")
    elif not args.test_mode:
        try:
            parsed_url = urlparse(args.repository)

            # Проверка корректности порта, если он указан.
            _ = parsed_url.port

        except ValueError as error:
            raise ValueError(
                "Некорректный URL репозитория."
            ) from error

        if (
            parsed_url.scheme not in ("http", "https")
            or not parsed_url.netloc
            or not parsed_url.hostname
        ):
            raise ValueError(
                "Некорректный URL репозитория. "
                "Используйте адрес с http:// или https://."
            )

    # Проверка пути к тестовому файлу.
    args.test_file = args.test_file.strip()

    if not args.test_file:
        raise ValueError(
            "Путь к тестовому файлу не должен быть пустым."
        )

    if args.test_mode:
        test_path = Path(args.test_file)

        if not test_path.is_file():
            raise FileNotFoundError(
                f"Тестовый файл не найден: {args.test_file}"
            )

    # Проверка выходного файла.
    args.output = args.output.strip()

    if not args.output:
        raise ValueError(
            "Имя выходного файла не должно быть пустым."
        )

    output_path = Path(args.output)

    if output_path.name in ("", ".", ".."):
        raise ValueError(
            "Указано некорректное имя выходного файла."
        )

    if not output_path.parent.exists():
        raise ValueError(
            f"Каталог для выходного файла не существует: "
            f"{output_path.parent}"
        )

    if not output_path.parent.is_dir():
        raise ValueError(
            f"Указанный родительский путь не является каталогом: "
            f"{output_path.parent}"
        )

    if output_path.exists() and output_path.is_dir():
        raise ValueError(
            "Вместо имени выходного файла указан каталог."
        )


def print_configuration(args):
    """Print configuration as key-value pairs (stage 1 requirement)."""

    print("Параметры запуска:")
    print(f"package = {args.package}")
    print(f"repository = {args.repository}")
    print(f"test_mode = {args.test_mode}")
    print(f"test_file = {args.test_file}")
    print(f"output = {args.output}")
    print(f"ascii_tree = {args.ascii_tree}")
    print(f"stage = {args.stage}")


def main():
    """Run the selected project stage."""

    args = parse_args()

    # Проверка конфигурации.
    try:
        validate_args(args)

    except (ValueError, FileNotFoundError) as error:
        print(
            f"Ошибка конфигурации: {error}",
            file=sys.stderr
        )
        return 2

    # Этап 1: минимальный CLI-прототип.
    if args.stage == 1:
        print_configuration(args)
        print("\nЭтап 1 завершён: параметры проверены.")
        return 0

    try:

        # Этап 2: получение прямых зависимостей.
        if args.stage == 2:

            if args.test_mode:
                dependency_map = load_test_graph(args.test_file)

                if args.package not in dependency_map:
                    raise ValueError(
                        f"Пакет '{args.package}' отсутствует "
                        "в тестовом графе."
                    )

                dependencies = dependency_map[args.package]

            else:
                dependencies = get_direct_dependencies(
                    args.package,
                    args.repository
                )

            print(
                f"\nПрямые зависимости пакета {args.package}:"
            )

            if dependencies:
                for dependency in dependencies:
                    print(f"- {dependency}")
            else:
                print("(прямые зависимости не найдены)")

            return 0

        # Этап 3: построение транзитивного графа зависимостей.
        if args.test_mode:
            dependency_map = load_test_graph(args.test_file)

        else:
            dependency_map = get_dependency_map(args.repository)

        # Проверяем наличие пакета в репозитории.
        if args.package not in dependency_map:

            # Пакет может встречаться как зависимость другого пакета,
            # даже если у него самого нет зависимостей.
            known_as_dependency = any(
                args.package in dependencies
                for dependencies in dependency_map.values()
            )

            if not known_as_dependency:
                raise ValueError(
                    f"Пакет '{args.package}' не найден "
                    "в репозитории/тестовом графе."
                )

            dependency_map[args.package] = []

        # Построение графа алгоритмом BFS с рекурсией.
        graph = build_graph_bfs_recursive(
            args.package,
            dependency_map
        )

        print(
            f"\nТранзитивный граф зависимостей "
            f"для пакета {args.package}:"
        )

        for package, dependencies in graph.items():
            dependencies_text = (
                ", ".join(dependencies)
                if dependencies
                else "(нет зависимостей)"
            )

            print(f"{package}: {dependencies_text}")

        # Дополнительный вывод ASCII-дерева.
        if args.ascii_tree:
            print("\nASCII-дерево:")
            print_ascii_tree(args.package, graph)

    except (ValueError, OSError, RuntimeError, KeyError) as error:
        print(
            f"Ошибка выполнения: {error}",
            file=sys.stderr
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
