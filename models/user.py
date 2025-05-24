from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from .role import *
from .departement import *

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    picture = Column(String, nullable=True)
    password= Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))

    role = relationship("Role", back_populates="users")  # Use string, not actual class
    department = relationship("Department",back_populates="users")
