from . import Tools
from .SQLMethod import SQLMethod
from .SQLQuery import SQLQuery


def initDatabase():
    from .. import database
    database.create_table(SQLQuery.createTable)
