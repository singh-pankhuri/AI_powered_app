from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, declarative_base
from sqlalchemy.engine import URL
from datetime import datetime

# Specify DB connection parameters
db_user="myuser"
db_password='password'
db_host="localhost"
db_port="5432"
db_name="todo_app"

conn_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(conn_url)

# Create Table Schemas
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    first_name = Column(String(80),nullable=False)
    last_name = Column(String(80),nullable=False)
    password = Column(String(80),nullable=False)
    access_token = Column(String(200))
    tasks = relationship('Task', backref='user')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80))
    due_date = Column(DateTime())
    priority = Column(Integer())
    user_id = Column(Integer(), ForeignKey('users.id'))
    access_token = Column(String(200))

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Connect to the database
    connection = engine.connect()
    print("Connection to PostgreSQL DB successful")

    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # if not engine.dialect.has_table(engine, "users"):
    # # If the table does not exist, create it
    #     Base.metadata.create_all(engine)

    print("Table Creation Complete")

    connection = session.connection()
    print("PostgreSQL session is started")

    test1 = User(email = 'test@gmail.com', first_name = "Test", last_name = "User", password = "pwd")
    task1 = Task(name = "Test Task for test user 1", due_date = datetime(2022, 8, 29), priority = 1, user = test1)

    session.add(task1)
    session.commit()

    # print(task1.title)
    # print(task1.id)

except Exception as e:
    print(f"The error '{e}' occurred")

finally:
    session.close()
    print("PostgreSQL session is closed")