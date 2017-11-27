from peewee import *

db = SqliteDatabase('lit.db')


class BaseModel(Model):
    class Meta:
        database = db  # model uses database 'lit.db'


class StagingArea(BaseModel):
    file = CharField(unique=True, primary_key=True)


class Commit(BaseModel):
    hash = CharField(unique=True)
    user_name = CharField()
    datetime = DateTimeField()
    comment = CharField()


class Branch(BaseModel):
    name = CharField(unique=True)


class CommitBranch(BaseModel):
    commit = ForeignKeyField(Commit)
    branch = ForeignKeyField(Branch)


class Head(BaseModel):
    active_branch = ForeignKeyField(Branch)
    # we have no last_commit_id if there are no commits
    last_commit = ForeignKeyField(Commit, null=True)


def create_tables():
    db.connect()
    # db.drop_tables([StagingArea, Commit, Branch, CommitBranch, Head])
    db.create_tables([StagingArea, Commit, Branch, CommitBranch, Head])


create_tables()
