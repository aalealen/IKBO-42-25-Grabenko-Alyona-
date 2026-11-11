"""Read a simple test dependency graph from JSON."""

import json
from pathlib import Path


def load_test_graph(file_path):
    """Load graph JSON: package names should be uppercase Latin letters."""
    path = Path(file_path)
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Некорректный JSON в {file_path}: {error}") from error
    except OSError as error:
        raise OSError(f"Не удалось прочитать тестовый файл: {error}") from error

    if not isinstance(content, dict):
        raise ValueError("Тестовый граф должен быть JSON-объектом.")

    graph = {}
    for package, dependencies in content.items():
        if not isinstance(package, str) or not package.isalpha() or not package.isupper():
            raise ValueError(
                f"Название пакета '{package}' должно состоять из заглавных латинских букв."
            )
        if not isinstance(dependencies, list):
            raise ValueError(f"Зависимости пакета {package} должны быть списком.")

        normalized_dependencies = []
        for dependency in dependencies:
            if (
                not isinstance(dependency, str)
                or not dependency.isalpha()
                or not dependency.isupper()
            ):
                raise ValueError(
                    f"Название зависимости '{dependency}' должно состоять "
                    "из заглавных латинских букв."
                )
            normalized_dependencies.append(dependency)

        graph[package] = normalized_dependencies

    return graph
