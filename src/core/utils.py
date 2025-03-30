from datetime import datetime
from uuid import UUID


def convert_data_to_str(data):
    """
      Recursively convert all boolean values, datetime objects, and UUID objects in a dictionary to their string representation.

    Args:
    data (dict): The input dictionary with potentially boolean values, datetime objects, and UUID objects.

    Returns:
    dict: A new dictionary with boolean values, datetime objects, and UUID objects converted to strings.
    """
    if isinstance(data, dict):
        return {k: convert_data_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_data_to_str(element) for element in data]
    elif isinstance(data, bool):
        return str(data).lower()
    elif isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, UUID):
        return str(data)
    else:
        return data


def convert_data_to_dict(data):
    """
    Recursively convert all string representations of boolean values in a dictionary back to booleans.

    Args:
    data (dict): The input dictionary with potentially string representations of boolean values.

    Returns:
    dict: A new dictionary with string representations of boolean values converted back to booleans.
    """
    if isinstance(data, dict):
        return {k: convert_data_to_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_data_to_dict(element) for element in data]
    elif isinstance(data, str):
        if data.lower() == "true":
            return True
        elif data.lower() == "false":
            return False
        # try:
        #     return datetime.fromisoformat(data)
        # except ValueError:
        try:
            return UUID(data)
        except ValueError:
            return data
    else:
        return data
