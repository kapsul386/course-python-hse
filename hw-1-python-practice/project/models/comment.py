from __future__ import annotations

from datetime import datetime
from typing import Any


class Comment:
    def __init__(self, author_id: Any, text: str) -> None:
        self.author_id: Any = author_id
        self.text: str = text
        self.create_data: datetime = datetime.now()
        self.update_data: datetime = self.create_data
        self.like_count: int = 0

    def edit_comment(self, new_text: str) -> None:
        self.text = new_text
        self.update_data = datetime.now()

    def like(self) -> None:
        self.like_count += 1

    def dislike(self) -> None:
        self.like_count -= 1

    def __repr__(self) -> str:
        return f"Comment(author_id={self.author_id!r}, text={self.text!r}, like_count={self.like_count})"
