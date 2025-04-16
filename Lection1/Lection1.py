# # Шпаргалки по типам, классам, функциям

# ТИПЫ
# 5 - тип int (целое число)
# 5.86 - тип float (дробное число)
# Привет - тип str (строка)
# 1 или 0 (True или False) - тип bool (булевое, единица или ноль, правда или ложь)
#
# АРИФМЕТИЧЕСКИЕ ОПЕРАЦИИ
#
# + сложение
# - вычитание
# * умножение
# / деление
# % остаток от деления (проверка на кратность)
# // целочисленное деление
# ** возведение в степень

import json
import os

# Файл для хранения данных о героях
data_file = 'heroes_data.json'

# Создание/чтение базы данных героев
def load_heroes_data():
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}

def save_heroes_data(data):
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Инициализация базы данных
heroes_data = load_heroes_data()

def get_hero_recommendations(hero_name):
    hero_info = heroes_data.get(hero_name)
    if hero_info:
        parameters = hero_info["parameters"]
        sets = hero_info["sets"]
        synergies = {
            "PvP": hero_info["synergy"]["PvP"],
            "PvE": hero_info["synergy"]["PvE"],
            "Hydra/Chimera": hero_info["synergy"]["Hydra/Chimera"],
            "Ваша коллекция": get_collection_synergy(hero_name)
        }
        return parameters, sets, synergies
    else:
        return None, None, None

def get_collection_synergy(hero_name):
    # Возвращает список героев, уже добавленных в базу, которые могут синергировать с данным героем
    collection_synergy = []
    for hero, info in heroes_data.items():
        if hero != hero_name:  # Исключаем текущего героя из списка
            collection_synergy.append(hero)
    return collection_synergy

def main():
    while True:
        user_input = input("Введите имя героя (или 'выход' для завершения): ").strip()
        if user_input.lower() == 'выход':
            break

        parameters, sets, synergies = get_hero_recommendations(user_input)

        if parameters:
            print(f"\nИнформация о герое {user_input}:")
            print(f"Класс: {heroes_data[user_input]['class']}")
            print(f"Параметры: {parameters}")
            print(f"Рекомендуемые сеты: {', '.join(sets)}")
            print("\nЭффективные команды:")
            for content_type, synergy_list in synergies.items():
                print(f"{content_type}: {', '.join(synergy_list)}")
        else:
            print(f"Герой '{user_input}' не найден в базе данных.")
            add_hero = input("Хотите добавить нового героя? (Да/Нет): ").strip().lower()
            if add_hero == 'да':
                class_name = input("Введите класс героя: ")
                parameters_input = {}
                parameters_input['attack'] = input("Укажите уровень атаки (высокий/средний/низкий): ")
                parameters_input['defense'] = input("Укажите уровень защиты (высокий/средний/низкий): ")
                parameters_input['speed'] = input("Укажите уровень скорости (высокий/средний/низкий): ")
                sets_input = input("Укажите рекомендуемые сеты, разделенные запятой: ").split(',')
                synergy_pvp = input("Введите синергию для PvP, разделенную запятой: ").split(',')
                synergy_pve = input("Введите синергию для PvE, разделенную запятой: ").split(',')
                synergy_hydra = input("Введите синергию для Hydra/Chimera, разделенную запятой: ").split(',')

                # Добавление нового героя в базу данных
                heroes_data[user_input] = {
                    "class": class_name,
                    "parameters": parameters_input,
                    "sets": [s.strip() for s in sets_input],
                    "synergy": {
                        "PvP": [s.strip() for s in synergy_pvp],
                        "PvE": [s.strip() for s in synergy_pve],
                        "Hydra/Chimera": [s.strip() for s in synergy_hydra],
                        "Ваша коллекция": []  # Для нового героя начально пустой
                    }
                }
                # Сохранение обновленных данных в файл
                save_heroes_data(heroes_data)
                print(f"Герой {user_input} успешно добавлен!")
            elif add_hero == 'нет':
                print("Попробуйте ввести другое имя героя.")
            else:
                print("Неправильный ввод. Пожалуйста, введите 'Да' или 'Нет'.")

if __name__ == "__main__":
    main()