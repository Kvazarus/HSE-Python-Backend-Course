import uuid


class User:
    def __init__(self, name: str):
        self.id = uuid.uuid4()
        self.name = name
        self.comments_count = 0
        self.rate = 0
        self.is_banned = False

    def edit_name(self, new_name: str):
        self.name = new_name

    def increment_rate(self):
        self.rate = self.rate + 1

    def ban_user(self):
        self.is_banned = True

    def unban_user(self):
        self.is_banned = False

    def __repr__(self) -> str:
        return f'User: {self.name} (ID: {self.id})'
