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

curs = metadata.tables["curators"]
deps = metadata.tables["departments"]
facs = metadata.tables["faculties"]
g_curs = metadata.tables["group_curators"]
groups = metadata.tables["groups"]
g_lecs = metadata.tables["groups_lectures"]
lecs = metadata.tables["lectures"]
subj = metadata.tables["subjects"]
teach = metadata.tables["teachers"]
users = metadata.tables["users"]


def all_groups_info():
    results = session.query(groups).all()

    if results:
        for result in results:
            print(result)

def all_teach_info():
    results = session.query(teach).all()

    if results:
        for result in results:
            print(result)



def deps_names():
    results = session.query(deps.c.name)

    if results:
        for result in results:
            print(result)


def teach_names_per_group():
    results = (session.query(teach.c.name,
                            teach.c.surname, groups.c.name_group).join(lecs, lecs.c.teacher_id == teach.c.id)
               .join(g_lecs, g_lecs.c.id_lecture == lecs.c.id)
               .join(groups, groups.c.id == g_lecs.c.id_group))

    if results:
        for result in results:
            print(f"{result.name} {result.surname} teaches group: {result.name_group}")


def groups_of_deps():
    results = session.query(groups.c.name_group, deps.c.name).join(groups, groups.c.department_id == deps.c.id)
    if results:
        for result in results:
            print(f"{result.name_group} group belongs to {result.name} department")


def subj_per_teach():
    results = (session.query(teach.c.name,
                             teach.c.surname, subj.c.subject_name)
               .join(lecs, lecs.c.teacher_id == teach.c.id)
               .join(subj, subj.c.id == lecs.c.subject_id))

    if results:
        for result in results:
            print(f"{result.name} {result.surname} teaches: {result.subject_name}")




def deps_of_subj():
    results = (session.query(subj.c.subject_name, deps.c.name)
               .join(lecs, lecs.c.subject_id == subj.c.id)
               .join(g_lecs, g_lecs.c.id_lecture == lecs.c.id)
               .join(groups, groups.c.id == g_lecs.c.id_group)
               .join(deps, deps.c.id == groups.c.department_id))

    if results:
        for result in results:
            print(f"You may study {result.subject_name} on {result.name}")

def groups_of_facs():
    results = (session.query(groups.c.name_group, facs.c.facult_name)
               .join(deps, deps.c.id == groups.c.department_id)
               .join(facs, facs.c.id == deps.c.faculties_id))

    if results:
        for result in results:
            print(f"{result.name_group} studies on {result.facult_name}")


print("What do you want to do?")
print("Press 0 to add exit")
print("Press 1 to output all group info")
print("Press 2 to output all teacher info")
print("Press 3 to output names of departments")
print("Press 4 to output teachers names per group")
print("Press 5 to output ammount of departments per each group")
print("Press 6 to output subject name per each teacher")
print("Press 7 to output departments with theirs subjects")
print("Press 8 to output faculties and their groups")


command = int(input("Input command: "))

while True:
    if command == 1:
        all_groups_info()
        break

    elif command == 2:
        all_teach_info()
        break

    elif command == 3:
        deps_names()
        break

    elif command == 4:
        teach_names_per_group()
        break

    elif command == 5:
        groups_of_deps()
        break

    elif command == 6:
        subj_per_teach()
        break

    elif command == 7:
        deps_of_subj()
        break

    elif command == 8:
        groups_of_facs()
        break

    elif command == 0:
        break

    else:
        raise Exception("Wrong command, try again")


