from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()
# 数据库
class FatigueRecord(Base):
    __tablename__ = 'fatigue_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now)
    epoch = Column(Integer)
    perclos_score = Column(Float)
    status = Column(String(10))  # 清醒 / 疲劳

class SpeedRecord(Base):
    __tablename__ = 'speed_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now)
    speed = Column(Float)

#  MySQL 配置
DATABASE_URL = "mysql+pymysql://driving_user:123456@localhost:3306/driving_detection?charset=utf8mb4"

# 连接和会话
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# 初始化建表（只需一次）
def init_db():

    Base.metadata.create_all(engine)

# 初始化数据库
# if __name__ == '__main__':
#     init_db()
#     print("数据库已初始化。")
#     # 查询测试
#     session = SessionLocal()
#     records = session.query(FatigueRecord).all()
#     for record in records:
#         print(f"ID: {record.id}, 时间: {record.timestamp}, 轮次: {record.epoch}, Perclos值: {record.perclos_score}, 状态: {record.status}")
