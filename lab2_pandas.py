"""Лабораторная работа 2. Pandas: Series, DataFrame и основные операции.

Шесть задач по конспекту: создание объектов, индексация и фильтрация,
пропуски, группировка, объединение таблиц и мини-анализ.
Таблица сотрудников задаётся прямо в скрипте.

Запуск:
    pip install -r requirements.txt
    python lab2_pandas.py
"""

import sys

import pandas as pd

LINE = "=" * 70

# если вывод перенаправляют в файл, Windows подставляет кодировку из локали
# и русский текст падает с UnicodeEncodeError
if (sys.stdout.encoding or "").lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def section(title):
    print()
    print(LINE)
    print(title)
    print(LINE)


# ---------------------------------------------------------------------------
# Задача 1. Создание Series и DataFrame, базовый осмотр
# ---------------------------------------------------------------------------
def task1():
    section("Задача 1. Создание Series и DataFrame, базовый осмотр")

    print("1.1 Series из списка чисел с произвольным индексом:")
    salaries = pd.Series(
        [120000, 72000, 99000, 85000],
        index=["Иванов", "Петрова", "Зайцев", "Кузнецов"],
        name="salary",
    )
    print(salaries.to_string())
    print(f"\nсредняя зарплата в ряду: {salaries.mean():.0f}")

    print("\n1.2 DataFrame из словаря:")
    df = pd.DataFrame(
        {
            "name": [
                "Иванов Алексей",
                "Петрова Мария",
                "Смирнов Дмитрий",
                "Кузнецов Игорь",
                "Соколова Анна",
                "Попов Сергей",
                "Лебедева Ольга",
                "Козлов Артём",
                "Новикова Екатерина",
                "Морозов Павел",
                "Волкова Ирина",
                "Зайцев Никита",
            ],
            "department": [
                "IT", "IT", "IT", "Аналитика", "Аналитика", "HR",
                "Продажи", "Продажи", "Продажи", "Финансы", "Финансы", "IT",
            ],
            "salary": [
                120000, 72000, None, 85000, 78000, None,
                70000, 64000, 61000, 99000, 74000, 105000,
            ],
            "bonus": [
                20000, None, 15000, 12000, None, 8000,
                25000, None, 9000, 18000, 11000, 30000,
            ],
            "hire_date": [
                "2019-03-12", "2020-07-01", "2018-11-23", "2021-02-15",
                "2022-09-05", "2023-01-16", "2019-06-10", "2020-12-01",
                "2021-04-20", "2017-08-14", "2022-03-28", "2016-05-30",
            ],
        }
    )
    print(f"таблица создана, строк: {df.shape[0]}, столбцов: {df.shape[1]}")

    print("\n1.3 Первые три строки:")
    print(df.head(3).to_string())

    print("\nПоследние три строки:")
    print(df.tail(3).to_string())

    print("\nТипы столбцов:")
    print(df.dtypes.to_string())
    print()
    df.info()

    print("\nСтатистика по числовым столбцам:")
    print(df.describe().round(1).to_string())

    return df


# ---------------------------------------------------------------------------
# Задача 2. Индексация, выборка, фильтрация
# ---------------------------------------------------------------------------
def task2(df):
    section("Задача 2. Индексация, выборка, фильтрация")

    print("2.1 Имя и зарплата сотрудников из IT:")
    print(df.loc[df["department"] == "IT", ["name", "salary"]].to_string())

    print("\n2.2 Первые 3 строки и первые 2 столбца через iloc:")
    print(df.iloc[:3, :2].to_string())

    print("\n2.3 Сотрудники с зарплатой выше 70000:")
    rich = df[df["salary"] > 70000]
    print(rich[["name", "department", "salary"]].to_string())
    print(f"всего таких сотрудников: {len(rich)}")

    print("\n2.4 Общая компенсация (пропуски в bonus считаются нулём):")
    df["total_comp"] = df["salary"].fillna(0) + df["bonus"].fillna(0)
    print(df[["name", "salary", "bonus", "total_comp"]].to_string())

    print("\n2.5 Удаляю столбец hire_date:")
    df.drop(columns=["hire_date"], inplace=True)
    print("остались столбцы:", ", ".join(df.columns))

    return df


# ---------------------------------------------------------------------------
# Задача 3. Обработка пропущенных значений
# ---------------------------------------------------------------------------
def task3(df):
    section("Задача 3. Обработка пропущенных значений")

    print("3.1 Пропуски в каждом столбце:")
    print(df.isna().sum().to_string())

    print("\n3.2 Заполняю пропуски в salary средним значением по отделу:")
    df["salary"] = df["salary"].fillna(df.groupby("department")["salary"].transform("mean"))
    print(f"осталось пропусков в salary: {int(df['salary'].isna().sum())}")
    left = df[df["salary"].isna()]
    if not left.empty:
        print("в отделах, где все зарплаты пропущены, среднее не посчитать:")
        print(left[["name", "department"]].to_string())

    print("\n3.3 Заполняю пропуски в bonus нулём:")
    df["bonus"] = df["bonus"].fillna(0)
    print(f"осталось пропусков в bonus: {int(df['bonus'].isna().sum())}")

    # зарплата изменилась, поэтому компенсацию считаю заново
    df["total_comp"] = df["salary"].fillna(0) + df["bonus"].fillna(0)

    print("\n3.4 Удаляю строки, где salary так и остался пропущен:")
    before = len(df)
    df.dropna(subset=["salary"], inplace=True)
    print(f"было строк: {before}, стало: {len(df)}")

    return df


# ---------------------------------------------------------------------------
# Задача 4. Группировка и агрегация
# ---------------------------------------------------------------------------
def task4(df):
    section("Задача 4. Группировка и агрегация")

    print("4.1 Средняя зарплата по отделам:")
    print(df.groupby("department")["salary"].mean().round(1).to_string())

    print("\n4.2 Средняя зарплата, максимальный бонус и число сотрудников:")
    summary = df.groupby("department").agg(
        avg_salary=("salary", "mean"),
        max_bonus=("bonus", "max"),
        employees=("name", "count"),
    )
    print(summary.round(1).to_string())

    print("\n4.3 Сводная таблица: отдел и средняя зарплата:")
    pivot = df.pivot_table(index="department", values="salary", aggfunc="mean")
    print(pivot.round(1).to_string())

    print("\n4.4 Отделы по убыванию средней зарплаты:")
    print(summary.sort_values("avg_salary", ascending=False).round(1).to_string())


# ---------------------------------------------------------------------------
# Задача 5. Объединение данных
# ---------------------------------------------------------------------------
def task5(df):
    section("Задача 5. Объединение данных")

    print("5.1 Таблица руководителей отделов:")
    managers = pd.DataFrame(
        {
            "department": ["IT", "Аналитика", "Продажи", "Финансы", "HR"],
            "manager": [
                "Иванов Алексей",
                "Кузнецов Игорь",
                "Лебедева Ольга",
                "Морозов Павел",
                "Попов Сергей",
            ],
        }
    )
    print(managers.to_string(index=False))

    print("\n5.2 Объединяю с сотрудниками по отделу (left join):")
    df = df.merge(managers, on="department", how="left")
    print(df[["name", "department", "manager"]].to_string())

    print("\n5.3 Добавляю нового сотрудника через concat:")
    new_row = pd.DataFrame(
        [
            {
                "name": "Орлов Пётр",
                "department": "Продажи",
                "salary": 68000.0,
                "bonus": 7000.0,
                "total_comp": 75000.0,
                "manager": "Лебедева Ольга",
            }
        ]
    )
    df = pd.concat([df, new_row])
    print(df.tail(2).to_string())

    print("\n5.4 Индекс после concat повторяется, сбрасываю его:")
    df.reset_index(drop=True, inplace=True)
    print(df.tail(2).to_string())

    return df


# ---------------------------------------------------------------------------
# Задача 6. Комплексный мини-анализ
# ---------------------------------------------------------------------------
def task6(df):
    section("Задача 6. Комплексный мини-анализ")

    print("6.1 Топ-3 сотрудника по общей компенсации:")
    print(df.nlargest(3, "total_comp")[["name", "department", "total_comp"]].to_string(index=False))

    print("\n6.2 Средняя зарплата и средний бонус по отделам:")
    print(df.groupby("department")[["salary", "bonus"]].mean().round(1).to_string())

    print("\n6.3 Доля сотрудников с зарплатой выше 75000:")
    high = (df["salary"] > 75000).groupby(df["department"]).mean()
    print(high.map("{:.0%}".format).to_string())


def main():
    df = task1()
    df = task2(df)
    df = task3(df)
    task4(df)
    df = task5(df)
    task6(df)


if __name__ == "__main__":
    main()
