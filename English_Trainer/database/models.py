import datetime

from typing import Annotated

from sqlalchemy import UniqueConstraint, Integer, DateTime, Boolean, Table, MetaData, Column, String, ForeignKey

from database.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


intpk = Annotated[int,mapped_column(primary_key=True)]

class Table_Users(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    name: Mapped[str]
    chat_id: Mapped[str]
    new_word_table: Mapped["Table_New_Word"] = relationship(back_populates='user')
    learned_word_table: Mapped["Table_Learned_Word"] = relationship(back_populates='user')

    __table_args__ = (UniqueConstraint('chat_id',name='unique_chat_id'),)

class Table_All_Word(Base):
    __tablename__ = 'all_dict'

    id: Mapped[intpk]
    word_en: Mapped[str]
    word_ru: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    __table_args__ = (UniqueConstraint('word_en',name='unique_word'),)


class Table_New_Word(Base):
    __tablename__ = 'new_dict'

    id: Mapped[intpk]
    word_en: Mapped[str]
    word_ru: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[list["Table_Users"]] = relationship(back_populates='new_word_table')
    count_answer: Mapped[int] = mapped_column(Integer,default=0)

class Table_Learned_Word(Base):
    __tablename__ = 'learned_dict'

    id: Mapped[intpk]
    word_en: Mapped[str]
    word_ru: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[list["Table_Users"]] = relationship(back_populates='learned_word_table')
    count_answer: Mapped[int] = mapped_column(Integer,default=0)

