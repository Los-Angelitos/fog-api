from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    _instance = None
    _meta = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()

        return cls._instance
    
    def _initialize(self):
        username = os.getenv("MSSQL_USERNAME")
        password = os.getenv("MSSQL_PASSWORD")
        database = os.getenv("MSSQL_DATABASE")
        server = os.getenv("MSSQL_SERVER")
        port = os.getenv("MSSQL_PORT", "3306")

        # connection string for development
        # mysql+pymysql://<username>:<password>@<server>/<database>

        # ensure the database is created before running the application
        print(username, password, database, server, port)
        if not all([username, password, database, server]):
            raise ValueError("Database connection parameters are not set in the environment variables.")

        self._engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{server}:{port}/{database}",
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=15
        )

        self.Base = declarative_base()
        self.Base.metadata.bind = self._engine
        
        self._session_factory = sessionmaker(bind=self._engine)
        self._meta = self.Base.metadata
        
        print("Database initialized with engine:", self._engine)

    @property
    def session(self):
        return self._session_factory()
    
    @property
    def meta(self):
        return self._meta
    
    def create_all(self):
        """Create all tables in the database."""
        self._meta.create_all(self._engine)
        print("All tables created in the database.")
    
db = Database()