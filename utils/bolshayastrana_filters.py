from datetime import date
from typing import Dict, Any, List

def transform_filter_values(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms filter values for the following keys:
      'regions', 'restKinds', 'collections', 'comfort', 'difficulty', 'accommodation'
    by replacing display names with corresponding codes from the mapping dictionaries.

    The mapping dictionaries (regions, restKinds, etc.) must be defined in the environment,
    each of which has the structure:
        'Name': 'Code'
    or for filters with additional info (like comfort, difficulty):
        'Name': {'value': 'Code', 'description': '...'}
    
    Args:
        filters (Dict[str, Any]): Input filters with possible multiple values (list) for the keys.
    
    Returns:
        Dict[str, Any]: The filters dictionary with transformed values for the specified keys.
    """

    mappings = {
        'regions': regions, 
        'cities': cities,
        'restKinds': restKinds,
        'collections': collections,
        'comfort': comfort,
        'difficulty': difficulty,
        'accommodation': accommodation,
    }
    
    new_filters = dict(filters)
    
    for key, mapping_dict in mappings.items():
        if key in filters:
            original_value = filters[key]
            if not isinstance(original_value, list):
                original_value = [original_value]
            transformed_values: List[str] = []
            for item in original_value:
                if item in mapping_dict:
                    code = mapping_dict[item]
                    if isinstance(code, dict):
                        transformed_values.append(code.get('value', item))
                    else:
                        transformed_values.append(code)
                else:
                    transformed_values.append(item)
            new_filters[key] = transformed_values
    return new_filters



def build_filter_descriptions(filter_definitions: Dict[str, Any]) -> str:
    """
    Builds a multi-line string describing the filters based on their definitions.

    Args:
        filter_definitions (Dict[str, Any]): Dictionary containing filter names as keys and their
            corresponding values which can be either dictionaries with 'value' or 'description'
            fields or simple lists of strings representing available options.

    Returns:
        str: A multi-line string where each line describes a filter option. For filters that have
            additional descriptions, the description is included in parentheses after the filter name.
            Special cases like dateFrom and dateTo are handled with specific descriptions.
    """
    descriptions = []
    for name, values in filter_definitions.items():
        if isinstance(values, dict) and all(isinstance(v, dict) and 'description' in v for v in values.values()):
            # Filters with additional description
            if name == "comfort":
                desc = ("comfort: Specifies the level of comfort provided by the tour. "
                        "Options: " + ", ".join([f'''"{k}" - {v['description']}''' for k, v in values.items()]))
            elif name == "difficulty":
                desc = ("difficulty: Specifies the physical difficulty of the tour. "
                        "Options: " + ", ".join([f'''"{k}" - {v['description']}''' for k, v in values.items()]))
            else:
                desc = f"{name}: " + ", ".join([f'''"{k}" - {v['description']}''' for k, v in values.items()])
        elif isinstance(values, dict):
            if name == "regions":
                desc = ("regions: Specifies the Russian region where the tour is available. "
                        "Options: " + ", ".join(values.keys()))
            if name == "cities":
                desc = ("cities: Specifies the Russian city where the tour is available. "
                        "When using region filter, city filter should not be used. "
                        "Options: " + ", ".join(values.keys()))
            elif name == "restKinds":
                desc = ("restKinds: Specifies the type of tour or activity. "
                        "Options: " + ", ".join(values.keys()))
            elif name == "collections":
                desc = ("collections: Specifies the tour collection or theme. "
                        "Options: " + ", ".join(values.keys()))
            elif name == "accommodation":
                desc = ("accommodation: Specifies the lodging type provided during the tour. "
                        "Options: " + ", ".join(values.keys()))
            else:
                desc = f"{name}: " + ", ".join(values.keys())
        else:
            if name == "dateFrom":
                desc = (f"dateFrom: Tour start date; cannot be before today ({date.today()}). "
                        "If a past season or month is requested, the date is auto-adjusted to the next valid period "
                        "(e.g., in April 2025, an autumn request becomes Sept–Nov 2025, and a February request becomes February 2026).")
            elif name == "dateTo":
                desc = ("dateTo: Tour end date; must be later than dateFrom and match the adjusted seasonal period.")
            elif name == "sort":
                desc = ("sort: Defines the sorting order of tour results. "
                        "Possible values include 'default' (by popularity), 'price' (ascending), and '-price' (descending).")
            elif name == "priceMin":
                desc = "priceMin: Specifies the minimum total price for the tour in rubles."
            elif name == "priceMax":
                desc = ("priceMax: Specifies the maximum total price for the tour in rubles. "
                        "When using total price filters (priceMin, priceMax), per-day filters (pricePerDayMin, pricePerDayMax) should not be used.")
            elif name == "pricePerDayMin":
                desc = "pricePerDayMin: Specifies the minimum price per day for the tour in rubles."
            elif name == "pricePerDayMax":
                desc = ("pricePerDayMax: Specifies the maximum price per day for the tour in rubles. "
                        "When using per-day price filters (pricePerDayMin, pricePerDayMax), total price filters (priceMin, priceMax) should not be used.")
            elif name == "daysMin":
                desc = "daysMin: Defines the minimum duration of the tour in days."
            elif name == "daysMax":
                desc = "daysMax: Defines the maximum duration of the tour in days."
            elif name == "minAge":
                desc = ("minAge: Specifies the minimum allowed participant age. "
                        "This filter ensures that the tour is appropriate for the intended age group (from 0 to 18, where 18 means no age filter).")
            elif name == "maxGroupSize":
                desc = ("maxGroupSize: Specifies the maximum number of participants allowed in the tour group. "
                        "This filter is used to maintain an optimal group size for the tour experience.")
            else:
                desc = f"{name}: {values}"
        descriptions.append(desc)

    descriptions_str = "\n".join(descriptions)
    return descriptions_str



# Dicts of filters for https://bolshayastrana.com
regions = {
    "Алтай": "1",
    "Адыгея": "3",
    "Карелия": "14",
    "Калмыкия": "19",
    "Хакасия": "24",
    "Дагестан": "26",
    "Ингушетия": "29",
    "Калужская область": "33",
    "Орловская область": "34",
    "Рязанская область": "35",
    "Белгородская область": "36",
    "Воронежская область": "37",
    "Тверская область": "38",
    "Псковская область": "39",
    "Ярославская область": "40",
    "Магаданская область": "41",
    "Ленинградская область": "42",
    "Тульская область": "43",
    "Костромская область": "44",
    "Липецкая область": "45",
    "Владимирская область": "46",
    "Калининградская область": "48",
    "Ивановская область": "49",
    "Хабаровский край": "52",
    "Нижегородская область": "53",
    "Красноярский край": "55",
    "Коми": "56",
    "Бурятия": "57",
    "Пермский край": "64",
    "Астраханская область": "68",
    "Ростовская область": "69",
    "Амурская область": "70",
    "Вологодская область": "74",
    "Московская область": "75",
    "Кировская область": "77",
    "Челябинская область": "83",
    "Мурманская область": "85",
    "Краснодарский край": "94",
    "Татарстан": "95",
    "Ульяновская область": "96",
    "Свердловская область": "98",
    "Тамбовская область": "100",
    "Волгоградская область": "101",
    "Новгородская область": "102",
    "Ставропольский край": "103",
    "Марий Эл": "133",
    "Смоленская область": "155",
    "Курская область": "156",
    "Самарская область": "157",
    "Саратовская область": "166",
    "Забайкальский край": "173"
}

cities = {
    "Абакан": "1",
    "Архангельск": "6",
    "Астрахань": "7",
    "Балаково": "9",
    "Барнаул": "10",
    "Белгород": "14",
    "Благовещенск": "18",
    "Братск": "21",
    "Брянск": "22",
    "Владивосток": "28",
    "Владикавказ": "29",
    "Волгоград": "30",
    "Волгодонск": "31",
    "Вологда": "32",
    "Воронеж": "34",
    "Грозный": "37",
    "Екатеринбург": "41",
    "Иваново": "46",
    "Ижевск": "49",
    "Иркутск": "51",
    "Йошкар-Ола": "54",
    "Казань": "56",
    "Калининград": "57",
    "Калуга": "58",
    "Кемерово": "59",
    "Киров": "62",
    "Комсомольск-на-Амуре": "65",
    "Кострома": "66",
    "Краснодар": "68",
    "Красноярск": "69",
    "Курган": "70",
    "Курск": "71",
    "Липецк": "75",
    "Магнитогорск": "78",
    "Махачкала": "79",
    "Москва": "82",
    "Мурманск": "83",
    "Набережные Челны": "85",
    "Нальчик": "88",
    "Нижневартовск": "93",
    "Нижний Новгород": "94",
    "Новокузнецк": "97",
    "Новосибирск": "99",
    "Норильск": "102",
    "Омск": "109",
    "Орёл": "110",
    "Оренбург": "111",
    "Орск": "112",
    "Пенза": "116",
    "Пермь": "117",
    "Петрозаводск": "118",
    "Петропавловск-Камчатский": "119",
    "Псков": "124",
    "Ростов-на-Дону": "126",
    "Рыбинск": "127",
    "Рязань": "128",
    "Самара": "131",
    "Санкт-Петербург": "132",
    "Саранск": "133",
    "Саратов": "134",
    "Смоленск": "135",
    "Сочи": "139",
    "Ставрополь": "141",
    "Сургут": "144",
    "Сыктывкар": "145",
    "Таганрог": "146",
    "Тамбов": "148",
    "Тверь": "150",
    "Томск": "153",
    "Тула": "154",
    "Тюмень": "157",
    "Улан-Удэ": "158",
    "Ульяновск": "159",
    "Уфа": "168",
    "Хабаровск": "170",
    "Чебоксары": "174",
    "Челябинск": "175",
    "Череповец": "176",
    "Чита": "178",
    "Южно-Сахалинск": "185",
    "Якутск": "186",
    "Ярославль": "187",
    "Бийск": "189",
    "Сызрань": "192",
    "Ангарск": "196",
    "Армавир": "198",
    "Балашиха": "200",
    "Великий Новгород": "204",
    "Волжский": "205",
    "Дзержинск": "207",
    "Домодедово": "210",
    "Златоуст": "217",
    "Каменск-Уральский": "218",
    "Королёв": "226",
    "Красногорск": "227",
    "Люберцы": "228",
    "Мытищи": "232",
    "Нижний Тагил": "235",
    "Новороссийск": "238",
    "Новочеркасск": "240",
    "Одинцово": "244",
    "Подольск": "247",
    "Прокопьевск": "248",
    "Северодвинск": "256",
    "Старый Оскол": "260",
    "Стерлитамак": "261",
    "Тольятти": "262",
    "Уссурийск": "263",
    "Хасавюрт": "264",
    "Химки": "265",
    "Шахты": "267",
    "Энгельс": "270"
}

restKinds = {
    "Велотуры": "9",
    "Вертолетные туры": "20",
    "Восхождения": "10",
    "Горнолыжные туры": "11",
    "Дайвинг и снорклинг": "12",
    "Джип-туры": "13",
    "ЖД туры": "31",
    "Каньонинг": "23",
    "Комбинированные туры": "15",
    "Конные туры": "16",
    "Лыжные походы": "19",
    "Пешие туры": "7",
    "Рыболовные туры": "21",
    "Серфинг и SUP-туры": "14",
    "Сплавы": "8",
    "Туры на квадроциклах": "6",
    "Туры на снегоходах": "5",
    "Туры на собачьих упряжках": "4",
    "Фитнес и йога-туры": "22",
    "Экскурсионные туры": "18",
    "Экспедиции": "3",
    "Яхтинг": "1"
}

collections = {
    "Автобусные туры": "105",
    "Айс-флоатинг": "156",
    "Бесплатная отмена бронирования": "15",
    "Винные туры": "33",
    "Гастрономические туры": "35",
    "Избинг": "154",
    "Исторические туры": "91",
    "Корпоративные туры": "23",
    "Литературные туры": "87",
    "Мистические туры": "90",
    "На рафтах": "67",
    "Национальные туристические маршруты России": "123",
    "Необычные туры": "80",
    "Обзорные туры": "79",
    "Оздоровительные туры": "61",
    "Отдых с детьми": "6",
    "Познавательные туры": "89",
    "Популярные туры": "86",
    "Походы без рюкзаков": "118",
    "Проживание в глэмпинге": "19",
    "Промышленные туры": "155",
    "Событийные туры": "88",
    "Спа-туры": "111",
    "Спелеотуры": "108",
    "Туры для пенсионеров": "75",
    "Туры к Деду Морозу": "78",
    "Туры к петроглифам": "85",
    "Туры на байдарках": "63",
    "Туры на каяках": "110",
    "Туры на термальные источники": "20",
    "Туры на хивусах": "106",
    "Туры на Черную пятницу": "141",
    "Туры с наблюдением за дикими животными": "103",
    "Туры с северным сиянием": "24",
    "Туры, в которые можно с собакой": "59",
    "Фототуры": "52",
    "Экологические туры": "38",
    "Этнотуры": "57"
}

accommodation = {
    "Палатка": "tent",
    "Гостиница": "hotel",
    "Каюта": "cabin",
    "Квартира": "flat",
    "Поезд": "train",
    "Турбаза": "camp-site",
    "Гостевой дом": "guest-house",
    "Без проживания": "not-set"
}

comfort = {
    "Базовый": {
        "value": "base",
        "description": "Туристы живут в палатках, кемпингах или хижинах. Удобств нет или они находятся на улице"
    },
    "Простой": {
        "value": "base_plus",
        "description": "Гостевые дома или гостиницы 1* (одна звезда). Удобства могут быть в каждом номере или на этаже"
    },
    "Средний": {
        "value": "medium",
        "description": "Апартаменты, коттеджи или гостиницы 2* (две звезды). Обычно есть удобства: питание и уборка"
    },
    "Выше среднего": {
        "value": "improved",
        "description": "Гостиницы 3* (три звезды) или виллы. Обычно удобства в каждом номере, на территории могут быть спа-зона, бассейн и тренажерный зал"
    },
    "Высокий": {
        "value": "premium",
        "description": "Гостиницы 4 и 5* (четыре и пять звёзд), бутик-отели или глэмпинги. Часто включает в себя эксклюзивные услуги вроде собственного бассейна"
    }
}

difficulty = {
    "Легкий": {
        "value": "1",
        "description": "Физическая нагрузка минимальна. Подходит для всех, вне зависимости от физической подготовки и возраста"
    },
    "Средний": {
        "value": "2",
        "description": "Не требует физической подготовки, но предполагает умеренную физическую нагрузку"
    },
    "Интенсивный": {
        "value": "3",
        "description": "Не требует специальных навыков, но туристы должны быть в хорошей физической форме"
    },
    "Экстремальный": {
        "value": "4",
        "description": "Только для опытных и физически подготовленных туристов. Нужны специальные навыки и снаряжение"
    }
}
