from uuid import UUID


def validate_uuid(uuid_to_test: str, version: int = 4):
    """
    Check if uuid_to_test is a valid UUID. Acknowledgments: https://stackoverflow.com/a/33245493
    :param uuid_to_test: str
    :param version: {1, 2, 3, 4}
    :return: True if uuid_to_test is a valid UUID, otherwise False.

    Examples
    --------
    >>> validate_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> validate_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
