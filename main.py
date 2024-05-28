from sqlalchemy import (create_engine, Column, Integer, String,
                        insert, update, Sequence, Date, MetaData, delete, Table)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text


username = 'postgres'
db_password = 134472

db_url = f'postgresql+psycopg2://{username}:{db_password}@localhost:5432/academy'
engine = create_engine(db_url)

metadata = MetaData()
metadata.reflect(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

tables = {
    "curators": metadata.tables["curators"],
    "departments": metadata.tables["departments"],
    "faculties": metadata.tables["faculties"],
    "group_curators": metadata.tables["group_curators"],
    "groups": metadata.tables["groups"],
    "groups_lectures": metadata.tables["groups_lectures"],
    "lectures": metadata.tables["lectures"],
    "subjects": metadata.tables["subjects"],
    "teachers": metadata.tables["teachers"],
    "users": metadata.tables["users"]
}



print("What do you want to do?")
print("Press 0 to add exit")
print("Press 1 to add row")
print("Press 2 to delete row")

command = int(input("Input command: "))

if command == 1:
    table_name = input("Input table name to insert data: ")

    if table_name in tables:
        users_table = metadata.tables[table_name]
        columns = users_table.columns.keys()
        new_record = {}

        for column in columns:
            new_value = input(f"Input new value for {column}: ")
            new_record[column] = new_value

        inserted_values = insert(users_table).values(new_record)

        session.execute(inserted_values)
        session.commit()

elif command == 2:
    table_name = input("Input table name to delete data: ")

    if table_name in tables:
        users_table = metadata.tables[table_name]
        index_column = input("Input index column name: ")
        index_value = input("Input index value to delete: ")

        delete_query = delete(users_table).where(users_table.columns[index_column] == index_value)

        session.execute(delete_query)
        session.commit()

    ...





