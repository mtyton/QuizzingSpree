from typing import List


class DataEntriesRequiredValidator(object):

    @staticmethod
    def validate(required_keys: List[str], data: dict) -> List[dict]:
        _errors = []
        for key in required_keys:
            if not data.get(key, None):
                _errors.append({
                    'message': f"missing data for key: {key}"
                })
        return _errors
