from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{os.getenv('USER_DB')}:{os.getenv('PASS_DB')}@{os.getenv('SERVER_DB_URI')}/{os.getenv('NAME_DB')}?driver=ODBC+Driver+18+for+SQL+Server"
    SQLALCHEMY_TRACK_MODIFICATIONS = False