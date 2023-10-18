from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from typing_extensions import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now


class Base(DeclarativeBase):
    pass


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(String(250), unique=True)
    password: Mapped[str] = mapped_column(String(200))  # TODO: Encrypt.
    name: Mapped[str] = mapped_column(String(50))

    chat_messages = relationship("ChatMessages", back_populates="user_ref")


class ChatMessages(Base):
    __tablename__ = "chat_messages"

    id: Mapped[intpk]
    user_ref: Mapped[intpk] = mapped_column(ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    chatbot_id: Mapped[str] = mapped_column(String(50), unique=True)
    message: Mapped[str] = mapped_column(Text)
    is_bot_reply: Mapped[bool] = mapped_column(Boolean)
    createdat: Mapped[datetime] = mapped_column(server_default=now(), index=True)