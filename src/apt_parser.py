
"""Download and parse apt Packages or Packages.gz
using Python standard library."""

import gzip
import urllib.error
import urllib.request


def _read_repository(url):
    """Download repository metadata and return its decoded text."""

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "variant8-dependency-graph/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw_data = response.read()

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise RuntimeError(
            f"Не удалось загрузить репозиторий: {error}"
        ) from error

    # Распаковка архива Packages.gz.
    if url.lower().split("?")[0].endswith(".gz"):
        try:
            raw_data = gzip.decompress(raw_data)
        except (OSError, EOFError) as error:
            raise RuntimeError(
                "Не удалось распаковать Packages.gz."
            ) from error

    return raw_data.decode("utf-8", errors="replace")


def _parse_package_records(text):
    """Yield apt package records separated by blank lines."""

    # Нормализация переносов строк.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    for record in text.split("\n\n"):
        fields = {}
        current_field = None

        for line in record.splitlines():

            if not line:
                continue

            # Обработка многострочных полей.
            if line[0].isspace() and current_field:
                fields[current_field] += " " + line.strip()
                continue

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            current_field = key.strip()
            fields[current_field] = value.strip()

        if fields.get("Package"):
            yield fields


def _dependency_names(dependency_field):
    """Extract package names from Depends and Pre-Depends fields."""

    names = []

    # Запятые разделяют группы обязательных зависимостей.
    for dependency_group in dependency_field.split(","):

        # Вертикальная черта разделяет альтернативные пакеты.
        alternatives = dependency_group.split("|")

        if not alternatives:
            continue

        # Для упрощённого графа выбираем первую альтернативу.
        token = alternatives[0].strip().split()

        if not token:
            continue

        # Убираем архитектурный квалификатор :any или :native.
        name = token[0].split(":")[0]

        if name and name not in names:
            names.append(name)

    return names


def get_dependency_map(repository_url):
    """Return {package: [direct dependencies]} from apt metadata."""

    metadata = _read_repository(repository_url)

    dependency_map = {}

    for record in _parse_package_records(metadata):

        package_name = record["Package"]

        # Учитываем оба типа обязательных зависимостей.
        dependency_field = ", ".join(
            field
            for field in (
                record.get("Depends", ""),
                record.get("Pre-Depends", "")
            )
            if field
        )

        dependency_map[package_name] = _dependency_names(
            dependency_field
        )

    if not dependency_map:
        raise RuntimeError(
            "В репозитории не найдены записи пакетов apt."
        )

    return dependency_map


def get_direct_dependencies(package_name, repository_url):
    """Return direct dependencies for one package."""

    if not package_name.strip():
        raise ValueError(
            "Имя пакета не должно быть пустым."
        )

    dependency_map = get_dependency_map(repository_url)

    if package_name not in dependency_map:
        raise RuntimeError(
            f"Пакет '{package_name}' не найден "
            "в указанном Packages-репозитории."
        )

    return dependency_map[package_name]
