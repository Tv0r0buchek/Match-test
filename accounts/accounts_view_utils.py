import logging

from django.contrib.auth import get_user_model

logger = logging.getLogger('django')

User = get_user_model()


def get_full_role(role: str, full_role=str) -> str:
    if role and isinstance(role, str):
        if role == "ST":
            full_role = "участник"
        elif role == "AD":
            full_role = "администратор"
        elif role == "WK":
            full_role = "модератор"
        elif role == "IA":
            full_role = "inactive"
    else:
        logger.error("get_full_role, role пуста или некорректен тип данных ")
        full_role = ""
    return full_role


