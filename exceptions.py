class EmptyResponseException(Exception):
    """Исключение, возникающее при получении пустого ответа от API."""
    pass


class NotGettingListException(Exception):
    """Исключение, возникающее при получении домашки не в виде списка."""
    pass
