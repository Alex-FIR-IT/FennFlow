from dataclasses import dataclass


@dataclass
class UserPath:
    user_id: int

    def render(self) -> str:
        return f"users/user_{self.user_id}"


@dataclass
class UserPathWithTrailingSlash:
    user_id: int

    def render(self) -> str:
        return f"users/user_{self.user_id}/"


@dataclass
class MonthPath:
    year: int
    month: int

    def render(self) -> str:
        return f"{self.year}/{self.month:02d}"


@dataclass
class MonthPathWithTrailingSlash:
    year: int
    month: int

    def render(self) -> str:
        return f"{self.year}/{self.month:02d}/"
