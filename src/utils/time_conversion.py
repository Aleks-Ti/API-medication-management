from datetime import datetime, time, timedelta

DICT_TIMEZONE = {
    "-1": lambda x: x - 1,
    "МСК": lambda x: x,
    "+1": lambda x: x + 1,
    "+2": lambda x: x + 2,
    "+3": lambda x: x + 3,
    "+4": lambda x: x + 4,
    "+5": lambda x: x + 5,
    "+6": lambda x: x + 6,
    "+7": lambda x: x + 7,
    "+8": lambda x: x + 8,
    "+9": lambda x: x + 9,
}


def conversion_reception_time_to_GMT(reception_time: time, timezone: str) -> time:
    """
    Приводит время полученное от пользователя в Telegram к времени GMT с учетом указанной пользователем TimeZone

    Variables:
        msk_time_zone (int): переменная нужна, для того чтобы привести время к нужному, потому что пользователь
        на стороне Telegram, всегда выбирает TimeZone с учетом от МСК TimeZone (+3 от GMT)
    """
    msk_time_zone = 3  # часовой пояс МСК от гринвича
    time_from_data = datetime.combine(datetime(2024, 1, 1), reception_time)
    result = (time_from_data - timedelta(hours=DICT_TIMEZONE[timezone](msk_time_zone))).time()
    return result


def conversion_GMT_reception_time_to_TZ(reception_time: time, timezone: str) -> time:
    """
    Приводит время GMT из БД для записи, к времени с учетом указанным пользователем TimeZone
    Variables:
        msk_time_zone (int): переменная нужна, для того чтобы привести время к нужному, потому что пользователь
        на стороне Telegram, всегда выбирает TimeZone с учетом от МСК TimeZone (+3 от GMT)
    """
    msk_time_zone = 3  # часовой пояс МСК от гринвича
    time_from_data = datetime.combine(datetime(2024, 1, 1), reception_time)
    result = (time_from_data + timedelta(hours=DICT_TIMEZONE[timezone](msk_time_zone))).time()
    return result
