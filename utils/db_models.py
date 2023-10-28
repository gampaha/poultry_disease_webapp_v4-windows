from sqlalchemy import Column, Integer, String, ForeignKey
from utils.database import Base
class Cases(Base):
    __tablename__ = 'Cases'
    Case_Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Address = Column(String)
    Farm_Type = Column(Integer)
    Animal_Cat = Column(Integer)
class Images(Base):    
    __tablename__ = 'Images'
    Image_Id = Column(Integer, primary_key=True, index=True)
    Image_Name = Column(String)
    Image_Loc = Column(String)
class Predictions(Base):
    __tablename__ = 'Predictions'
    Pred_Id = Column(Integer, primary_key=True, index=True)
    Prediction = Column(String)
    Confidence_Score = Column(String)
    Image_Id = Column(Integer, ForeignKey('Images.Image_Id'), nullable=False)
    Case_Id = Column(Integer, ForeignKey("Cases.Case_Id"), nullable=False) 
class Feedbacks(Base):
    __tablename__ = 'Feedbacks'
    Feed_Id = Column(Integer, primary_key=True, index=True)
    Feedback = Column(String)
    Case_Id = Column(Integer, ForeignKey("Cases.Case_Id"), nullable=False) 


