from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime, time

#schema for all the tickets details
class SLAInfo(BaseModel):
    name: Optional[str]
    response_time: Optional[str]
    resolution_time: Optional[str]

class TicketResponse(BaseModel):
    ticket_id: str
    title: str
    message: str
    contact_ref_no: Optional[str]
    ticket_status: Optional[str]
    priority: Optional[str]
    assigned_to: Optional[str]
    created_by: Optional[str]
    ticket_source: Optional[str]
    contact: Optional[str]
    sla: SLAInfo
    notification_types: List[str]
    purposes: List[str]
    to_recipients: List[str]
    cc_recipients: List[str]
    reminder_datetime: Optional[str]
    attachments: List[str]
    created_at: str
    updated_at: str

class TicketListResponse(BaseModel):
    message: str
    status_code: int
    data: List[TicketResponse]

class SingleTicketListResponse(BaseModel):
    message: str
    status_code: int
    data: TicketResponse

    

# class TicketStatusOut(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True


# class UserOut(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True


# class PriorityOut(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True


# class TicketOut(BaseModel):
#     id: int
#     ticket_id: Optional[str]
#     title: str
#     ticket_status: Optional[TicketStatusOut]
#     createdBy: Optional[UserOut]
#     assignedTo: Optional[UserOut]
#     priorities: Optional[PriorityOut]
#     company_id: Optional[int]
#     contact_id: Optional[int]
#     contact_ref_no: Optional[str]
#     message: Optional[str]
#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]

#     class Config:
#         from_attributes = True

