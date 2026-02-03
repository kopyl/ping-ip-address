from datetime import datetime


def format_time_delta(td: datetime) -> str:
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return (
        '{:02} годин, '
        '{:02} хвилин '
        'і {:02} секунд'
        .format(int(hours), int(minutes), int(seconds))
    )


def make_status_message(
    
        is_reachable: bool,
        last_status: dict,
        timestamp: datetime,
        status_change_counter: int
    ) -> str:

    """
    Avoid sending info on amount of time without/presence of light
    on the first status change after starting the script, becase
    we don't have enough data to calculate it accurately.
    """

    if last_status["status"] is None:
        if is_reachable:
            return f"Світло в будинку є"
        else:
            return f"Світло в будинку відсутнє"

    if is_reachable and not last_status["status"]:
        message = "Світло в будинку з'явилось."
        if status_change_counter > 1:
            time_with_no_light = timestamp - last_status["timestamp"]
            message += f" Не було світла протягом {format_time_delta(time_with_no_light)}"
        return message
    elif not is_reachable and last_status["status"]:
        message = "Світло в будинку вимкнулось."
        if status_change_counter > 1:
            time_with_light = timestamp - last_status["timestamp"]
            message += f" Світло було присутнє протягом {format_time_delta(time_with_light)}"
        return message
    
    return ""