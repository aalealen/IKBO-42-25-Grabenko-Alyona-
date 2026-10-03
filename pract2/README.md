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
cat matplotlib_deps.dot
dot -Tpng matplotlib_deps.dot -o matplotlib_deps.png
```
**Вывод cat matplotlib_deps.dot:**

<img width="1117" height="715" alt="image" src="https://github.com/user-attachments/assets/84df1cb5-c0d4-4784-b043-75fb3861ae7c" />

**Граф зависимостей matplotlib:**

<img width="1314" height="383" alt="image" src="https://github.com/user-attachments/assets/0a640035-b2ad-4314-95bc-349af3954886" />

### express
Для получения графа зависимостей создан Graphviz-код вручную на основе данных из `npm view express`.
```bash
nano express_deps.dot
dot -Tpng express_deps.dot -o express_deps.png
xdg-open express_deps.png
```
**Терминал с созданием и рендерингом express-графа:**

<img width="1175" height="247" alt="image" src="https://github.com/user-attachments/assets/43799258-ea69-4c15-a177-0063c62ef737" />

**Граф зависимостей express:**

<img width="2492" height="155" alt="image" src="https://github.com/user-attachments/assets/9b43750b-9c83-4045-8b9a-a32cb6143e91" />

## Задача 4. Счастливые билеты на MiniZinc

**Условие:**  
Изучить основы программирования в ограничениях. Установить MiniZinc, разобраться с основами его синтаксиса и работы в IDE. Решить на MiniZinc задачу о счастливых билетах. Добавить ограничение на то, что все цифры билета должны быть различными (подсказка: используйте `all_different`). Найти минимальное решение для суммы 3 цифр.

**Решение (файл `lucky_ticket.mzn`):**

```minizinc
include "alldifferent.mzn";

array[1..6] of var 0..9: digits;

constraint alldifferent(digits);

constraint digits[1] + digits[2] + digits[3] = digits[4] + digits[5] + digits[6];

var 0..27: sum3 = digits[1] + digits[2] + digits[3];

solve minimize sum3;

output [
    "Билет: \(digits[1])\(digits[2])\(digits[3])\(digits[4])\(digits[5])\(digits[6])\n",
    "Сумма первых трёх: \(sum3)\n",
    "Сумма последних трёх: \(digits[4] + digits[5] + digits[6])\n"
];
```
**Установка MiniZinc:**
На скриншоте показан процесс скачивания и распаковки MiniZinc IDE:
<img width="1476" height="709" alt="image" src="https://github.com/user-attachments/assets/f9968745-121d-4fc6-a24c-6ea0fd195b28" />

**Результат работы:**
На скриншоте показано минимальное решение задачи: билет 620431, у которого сумма первых трёх цифр (6+2+0 = 8) равна сумме последних трёх (4+3+1 = 8). Все цифры различны.

<img width="850" height="902" alt="image" src="https://github.com/user-attachments/assets/9aa31e21-8e2f-4619-9724-270787d5e482" />

## Задача 5. Зависимости пакетов на MiniZinc (по картинке)

**Условие:**  
Решить на MiniZinc задачу о зависимостях пакетов для рисунка.

**Решение (файл `packages.mzn`):**

```minizinc
var {100,110,120,130,140,150}: menu;
var {180,200,210,220,230}: dropdown;
var {100,200}: icons;

constraint icons = 100;

constraint (menu >= 110) -> (dropdown >= 200);
constraint (menu = 100)  -> (dropdown = 180);

constraint (dropdown >= 200) -> (icons = 200);

solve satisfy;

output [
    "menu     = \(menu div 100).\((menu mod 100) div 10).\(menu mod 10)\n",
    "dropdown = \(dropdown div 100).\((dropdown mod 100) div 10).\(dropdown mod 10)\n",
    "icons    = \(icons div 100).\((icons mod 100) div 10).\(icons mod 10)\n"
];
```
**Результат работы:**

На скриншоте показано решение: `menu = 1.0.0, dropdown = 1.8.0, icons = 1.0.0`. Это единственное решение, удовлетворяющее всем зависимостям.

<img width="850" height="902" alt="image" src="https://github.com/user-attachments/assets/b20c9357-7f23-4114-ab74-6a2ae9a95e60" />

## Задача 6. Зависимости пакетов на MiniZinc (по данным)

**Условие:**  
Решить на MiniZinc задачу о зависимостях пакетов для следующих данных:  
root 1.0.0 зависит от foo ^1.0.0 и target ^2.0.0. foo 1.1.0 зависит от left ^1.0.0 и right ^1.0.0. foo 1.0.0 не имеет зависимостей. left 1.0.0 зависит от shared >=1.0.0. right 1.0.0 зависит от shared <2.0.0. shared 2.0.0 не имеет зависимостей. shared 1.0.0 зависит от target ^1.0.0. target 2.0.0 и 1.0.0 не имеют зависимостей.

**Решение (файл `packages2.mzn`):**

```minizinc
var {0,100,110}: foo;
var {0,100,200}: target;
var {0,100}: left;
var {0,100}: right;
var {0,100,200}: shared;

constraint foo >= 100;
constraint target = 200;

constraint (foo = 110) -> (left = 100 /\ right = 100);
constraint (left = 100) -> (shared >= 100);
constraint (right = 100) -> (shared < 200);
constraint (shared = 100) -> (target < 200);

solve satisfy;

output [
    "foo    = \(foo)\n",
    "target = \(target)\n",
    "left   = \(left)\n",
    "right  = \(right)\n",
    "shared = \(shared)\n"
];
```
Обозначения в выводе: 100 = 1.0.0, 110 = 1.1.0, 200 = 2.0.0, 0 = не установлен.
**Результат работы:**

<img width="850" height="902" alt="image" src="https://github.com/user-attachments/assets/4e545cee-fb83-4ee0-a6d1-b56e922c4e09" />

Решение единственное: устанавливается `foo 1.0.0` (без зависимостей) и `target 2.0.0`. Пакеты `left`, `right`, `shared` не устанавливаются, потому что `foo 1.0.0` их не требует. Если бы был выбран `foo 1.1.0`, то потребовались бы `left` и `right`, которые через `shared` создали бы конфликт с `target`.


