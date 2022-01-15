from typing import Protocol


class BasePermission(Protocol):

    def check_permission(self) -> bool:
        ...
