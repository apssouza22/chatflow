from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from typing_extensions import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from sqlalchemy import UniqueConstraint

class Base(DeclarativeBase):
    pass


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(String(250), unique=True)
    password: Mapped[str] = mapped_column(String(200))  # TODO: Encrypt.
    name: Mapped[str] = mapped_column(String(50))

    chat_messages = relationship("ChatMessages", back_populates="user_ref")
    apps = relationship("App", back_populates="apps")


class ChatMessages(Base):
    __tablename__ = "chat_messages"

    id: Mapped[intpk]
    user_ref: Mapped[int] = mapped_column(ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    chatbot_id: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
    is_bot_reply: Mapped[bool] = mapped_column(Boolean)
    createdat: Mapped[datetime] = mapped_column(server_default=now(), index=True)

    # TODO: Possibly a unique constraint should not be missing?
    #__table_args__ = (UniqueConstraint('user_ref', 'chatbot_id', name='_chatbot_id_unique'),)

class App(Base):
    __tablename__ = "apps"

    id: Mapped[intpk]
    user_ref: Mapped[int] = mapped_column(ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    app_name: Mapped[str] = mapped_column(String(100))
    app_description: Mapped[str] = mapped_column(Text)
    app_key: Mapped[str] = mapped_column(String(50))
    app_model: Mapped[str] = mapped_column(String(50))
    app_temperature: Mapped[float] = mapped_column(default=0.1)

    __table_args__ = (UniqueConstraint('user_ref', 'app_key', name='_app_key_unique'),
                      UniqueConstraint('user_ref', 'app_name', name='_app_name_unique'))