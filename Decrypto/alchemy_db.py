import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
engine = create_engine("sqlite:///{}".format(os.path.join(project_dir, "decrypto.db")))

meta = MetaData()

words = Table(
    'words', meta,
    Column('word', String, primary_key = True)
)
insert_word = words.insert().values(word = "test")
meta.create_all(engine)