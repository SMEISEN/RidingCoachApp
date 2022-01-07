from datetime import datetime, timezone


def query_intervals(filter_keys, query, request, model):

    filter_data = {}
    for key in filter_keys:
        if request.get(key, 'ParameterNotInPayload') != 'ParameterNotInPayload':
            if "datetime" in key:
                filter_data[key] = {
                    'values': [
                        datetime.fromtimestamp(ts, tz=timezone.utc).replace(tzinfo=None) for ts in request.get(
                            key)['values']
                    ],
                    'operators': request.get(key)['operators'],
                }
            else:
                filter_data[key] = {
                    'values': request.get(key)['values'],
                    'operators': request.get(key)['operators'],
                }

    for attr, item in filter_data.items():
        for operator, value in zip(item['operators'], item['values']):
            if operator == '==':
                query = query.filter(getattr(model, attr) == value)
            elif operator == '<=':
                query = query.filter(getattr(model, attr) <= value)
            elif operator == '>=':
                query = query.filter(getattr(model, attr) >= value)
            elif operator == '<':
                query = query.filter(getattr(model, attr) < value)
            elif operator == '>':
                query = query.filter(getattr(model, attr) > value)
            elif operator == '!=':
                query = query.filter(getattr(model, attr) != value)
            else:
                raise ValueError('Given operator does not match available operators!')

    return query, filter_data
