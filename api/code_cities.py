
"""
    Конфигурация для получения информации о городах, прогнозе и тп.
"""

cities = {
    "Москва": ["294021", "bot/img/Moskwa.jpg"],
    "Ростов-на-Дону": ["295146", "bot/img/rostov-na-donu.jpg"],
    "Санкт-Петербург": ["295212", "bot/img/sant-petesburg.jpg"],
    "Луганск": ["324763", "bot/img/Lygansk.jpg"],
    "Чертково": ["290065", "bot/img/Chertkovo.jpg"]
}


def convert_fr_to_cl(fr: float):
    """
    Перевод с системы Фаренгейта в Цельсий
    :param fr:
    :return:
    """
    temperature_cl: float = (fr - 32) * (5 / 9)
    return temperature_cl