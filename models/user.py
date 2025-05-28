from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship
from database import Base
from models import *

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    picture = Column(String(255), nullable=True)
    
    status_id = Column(Integer, nullable=False, default=1)
    email_verified_at = Column(DateTime, nullable=True)

    password = Column(String(255), nullable=True)
    remember_token = Column(String(100), nullable=True)

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    role_id = Column(BigInteger, ForeignKey("roles.id"), nullable=True)
    department_id = Column(BigInteger, ForeignKey("departments.id"), nullable=True)    
    company_id = Column(BigInteger, ForeignKey("companies.id"), nullable=True)

    # Relationships
    role = relationship("Role", back_populates="users")
    department = relationship("Department", back_populates="users")
    sla_configurations = relationship("SlaConfiguration", back_populates="escalated")
    agent_purpose_links = relationship("AgentPurpose", back_populates="user")
    purposes = relationship(
        "Purpose",
        secondary="agent_purposes",
        back_populates="users"
    )
    ticket_attachments = relationship("TicketAttachment", back_populates="uploader")
    company = relationship("Company", back_populates="users")

    # department_id = Column(BigInteger, ForeignKey("departments.id"), nullable=True)
    # manager_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)

    # max_ticket_threshold = Column(Integer, nullable=False, default=0)
    # emp_ref_no = Column(String(255), nullable=True, index=True)
    # 
    # designation_id = Column(BigInteger, ForeignKey("designations.id"), nullable=True)
    # project_id = Column(BigInteger, ForeignKey("projects.id"), nullable=True)
    # shift_id = Column(BigInteger, ForeignKey("shifts.id"), nullable=True)
    # coa_no = Column(String(255), nullable=True)
    # emp_no = Column(String(256), nullable=True)
    # user_type_id = Column(BigInteger, ForeignKey("user_types.id"), nullable=True)
    # is_first_time = Column(Boolean, default=True)
    # assigned_to_others = Column(Boolean, default=False)

    # Relationships
    # department = relationship("Department")
    # manager = relationship("User", remote_side=[id], back_populates="agents")
    # agents = relationship("User", back_populates="manager", cascade="all, delete-orphan")
    # designation = relationship("Designation")
    # company = relationship("Company")
    # project = relationship("Project")
    # shift = relationship("Shift")
    # user_type = relationship("UserType", back_populates="users")

    # You can add relationships for status, tickets, comments etc. as needed
