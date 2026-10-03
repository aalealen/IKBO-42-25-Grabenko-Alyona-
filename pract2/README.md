# Практическое занятие №2. Менеджеры пакетов

**Выполнила:** Грабенко Алёна Андреевна, ИКБО-42-25

## Задача 1. Служебная информация о пакете matplotlib
**Условие:**  
Вывести служебную информацию о пакете `matplotlib` (Python). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

**Решение:**

Команда для вывода служебной информации:

```bash
python3 -m pip show matplotlib
```
Основные элементы:
- **Name** — имя пакета (`matplotlib`).
- **Version** — версия в формате semver `3.11.2` (MAJOR.MINOR.PATCH).
- **Summary** — краткое описание.
- **Home-page** — сайт проекта.
- **Author** — авторы пакета.
- **License** — лицензия.
- **Location** — путь установки.
- **Requires** — зависимости.
- **Required-by** — кто зависит от этого пакета.

**Как получить пакет без менеджера пакетов:**
- Скачать `.whl` файл напрямую с PyPI: https://pypi.org/project/matplotlib/#files
- Распаковать (это zip-архив): `unzip matplotlib-*.whl -d matplotlib_pkg`
- Служебная информация лежит в `matplotlib-*.dist-info/METADATA`.
- Либо клонировать репозиторий с GitHub и изучить `pyproject.toml`.

**Результат работы:**
На скриншоте показан вывод команды `pip show matplotlib` — служебная информация о пакете: имя, версия, зависимости, лицензия.
<img width="1087" height="319" alt="image" src="https://github.com/user-attachments/assets/74880c3f-f804-4700-aa2e-798f31dada25" />

## Задача 2. Служебная информация о пакете express
**Условие:**  
Вывести служебную информацию о пакете `express` (JavaScript). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

**Решение:**
Команда для вывода служебной информации:

```bash
npm view express
```
**Основные элементы:**
- **name** — имя пакета (`express`).
- **version** — версия в формате semver (`5.2.1`).
- **description** — краткое описание.
- **license** — лицензия (MIT).
- **dependencies** — зависимости пакета (28 штук).
- **maintainers** — сопровождающие пакета.
- **dist.tarball** — ссылка на архив пакета.
- **dist-tags** — теги версий (`latest: 5.2.1`).

**Как получить пакет без менеджера пакетов:**
- Скачать `.tgz` архив напрямую из реестра npm: https://registry.npmjs.org/express/-/express-5.2.1.tgz
- Распаковать: `tar -xzf express-5.2.1.tgz`
- Служебная информация лежит в `package/package.json`.
- Либо клонировать репозиторий с GitHub: https://github.com/expressjs/express

**Результат работы:**
На скриншоте показан вывод команды npm `view express` - служебная информация о пакете: имя, версия, зависимости, лицензия, сопровождающие.
<img width="1476" height="709" alt="image" src="https://github.com/user-attachments/assets/1b6e0d50-a5b3-468e-9cd2-ef8a0c5604e4" />

## Задача 3. Граф зависимостей matplotlib и express

**Условие:**  
Сформировать graphviz-код и получить изображения зависимостей matplotlib и express.

**Решение:**
### matplotlib
Для получения дерева зависимостей использована утилита `pipdeptree`:
```bash
pipdeptree --packages matplotlib --graph-output dot > matplotlib_deps.dot
```
Рендеринг изображения:
```bash
dot -Tpng matplotlib_deps.dot -o matplotlib_deps.png
```
### express
Для получения графа зависимостей создан Graphviz-код вручную на основе данных из `npm view express`.
```bash
nano express_deps.dot
dot -Tpng express_deps.dot -o express_deps.png
xdg-open express_deps.png
```

<img width="980" height="625" alt="image" src="https://github.com/user-attachments/assets/666b17f3-e243-4751-b89e-09f5bd766507" />

<img width="1314" height="383" alt="image" src="https://github.com/user-attachments/assets/0a640035-b2ad-4314-95bc-349af3954886" />

**Результат работы:**

Граф зависимостей matplotlib:
<img width="1314" height="383" alt="image" src="https://github.com/user-attachments/assets/0a640035-b2ad-4314-95bc-349af3954886" />

Граф зависимостей express:
<img width="2492" height="155" alt="image" src="https://github.com/user-attachments/assets/9b43750b-9c83-4045-8b9a-a32cb6143e91" />

