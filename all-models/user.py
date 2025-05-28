from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from database import Base  # your Base from SQLAlchemy setup
from .user_type import UserType

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    picture = Column(String, nullable=True)
    status_id = Column(Integer, ForeignKey("user_statuses.id"))
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    # department_id = Column(Integer, ForeignKey("departments.id"))
    # manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # max_ticket_threshold = Column(Integer, nullable=True)
    # emp_no = Column(String, nullable=True)
    # emp_ref_no = Column(String, nullable=True)
    # company_id = Column(Integer, ForeignKey("companies.id"))
    # designation_id = Column(Integer, ForeignKey("designations.id"))
    # user_type_id = Column(Integer, ForeignKey("user_types.id"))
    # is_first_time = Column(Boolean, default=True)
    # assigned_to_others = Column(Boolean, default=False)

    role = relationship("Role")
    # Relationships
    # department = relationship("Department")
    # manager = relationship("User", remote_side=[id], back_populates="agents")
    # agents = relationship("User", back_populates="manager")
    # status = relationship("UserStatus")
    # designation = relationship("Designation")
    # company = relationship("Company")
    # user_type = relationship("UserType",back_populates="users")
    # agent_purpose_links = relationship("AgentPurpose", back_populates="user")
    # purposes = relationship(
    #     "Purpose",
    #     secondary="agent_purposes",
    #     back_populates="users"
    # )
    # comments = relationship("Comment", back_populates="user", foreign_keys="[Comment.user_id]")

    # assigned_tickets = relationship("Tickets", foreign_keys="[Tickets.assigned_to_id]")
    # created_tickets = relationship("Tickets", foreign_keys="[Tickets.created_by_id]")
