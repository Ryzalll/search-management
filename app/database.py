# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Sesuaikan dengan setingan XAMPP / MySQL kamu
# user: root, password: (kosong), host: 127.0.0.1, port: 3306
DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/lost-and-found-db"

engine = create_engine(
    DATABASE_URL,
    echo=False,              # ubah True kalau mau lihat SQL di console
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency untuk dipakai di FastAPI (get_db)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
