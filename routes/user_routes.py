from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from utils.user import get_current_user , get_dropdown_options
from utils.user import verify_password, create_access_token
from sqlalchemy.orm import Session, joinedload
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import List, Optional
from database import get_db
from schemas import *
from models import *
import shutil
import json
import uuid
import os
router = APIRouter(prefix="/user", tags=["user"])

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/login", response_model=dict)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .options(joinedload(User.role))
        .filter(User.email == login_data.email)
        .first()
    )

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.email})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Login successful",
            "status_code": status.HTTP_200_OK,
            "access_token": token,
            "token_type": "bearer",
            "data": {
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "picture": user.picture,
                    "role_id": user.role.id if user.role else None,
                    # "department_id": user.department.id if user.department else None,
                    # "company_id": user.company.id if user.company else None,
                    # "project_id": user.project.id if user.project else None,
                    # "designation_id": user.designation.id if user.designation else None,
                    # "user_type_id": user.user_type.id if user.user_type else None,
                    # "manager_id": user.manager.id if user.manager else None,
                    # "status_id": user.status.id if user.status else None,
                    # "shift_id": user.shift.id if user.shift else None,
                },
                # "role": {
                #     "id": user.role.id if user.role else None,
                #     "name": user.role.name if user.role else None,
                #     "status": user.role.status if user.role else None,
                # },
                # "department": {
                #     "id": user.department.id if user.department else None,
                #     "name": user.department.name if user.department else None,
                #     "status": user.department.status if user.department else None,
                # },
                # "company": {
                #     "id": user.company.id if user.company else None,
                #     "name": user.company.name if user.company else None,
                #     "status": user.company.status if user.company else None,
                # },
                # "project": {
                #     "id": user.project.id if user.project else None,
                #     "name": user.project.name if user.project else None,
                #     "status": user.project.status if user.project else None,
                # },
                # "designation": {
                #     "id": user.designation.id if user.designation else None,
                #     "name": user.designation.name if user.designation else None,
                #     "status": user.designation.status if user.designation else None,
                # },
                # "user_type": {
                #     "id": user.user_type.id if user.user_type else None,
                #     "name": user.user_type.name if user.user_type else None,
                # },
                # "manager": {
                #     "id": user.manager.id if user.manager else None,
                #     "name": user.manager.name if user.manager else None,
                #     "email": user.manager.email if user.manager else None,
                # },
                # "status": {
                #     "id": user.status.id if user.status else None,
                #     "name": user.status.name if user.status else None,
                # },
                # "shift": {
                #     "id": user.shift.id if user.shift else None,
                #     "name": user.shift.name if user.shift else None,
                #     "status": user.shift.status if user.shift else None,
                # }
            }
        }
    )

@router.get("/get-roles")
def get_roles_menus(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    roles_menus = db.query(RolesMenu).all()
    all_menu_ids = set()

    parsed_roles = []

    for rm in roles_menus:
        try:
            raw_ids = json.loads(rm.menu_id)
            if isinstance(raw_ids, str):
                menu_ids = json.loads(raw_ids)
            else:
                menu_ids = raw_ids

            if not isinstance(menu_ids, list):
                menu_ids = []
        except Exception as e:
            print("JSON parse error:", e)
            menu_ids = []

        all_menu_ids.update(menu_ids)

        parsed_roles.append({
            "id": rm.id,
            "role_id": rm.role_id,
            "menu_ids": menu_ids,
            "status": rm.status
        })

    # ✅ Bulk fetch all Meneus at once
    menus = db.query(Meneus).filter(Meneus.id.in_(all_menu_ids)).all()
    menu_map = {menu.id: menu for menu in menus}

    result = []
    for role in parsed_roles:
        serialized_menus = []

        for menu_id in role["menu_ids"]:
            menu = menu_map.get(menu_id)
            if menu:
                serialized_menus.append({
                    "id": menu.id,
                    "name": menu.name,
                    "parent_id": menu.parent_id,
                    "status": menu.status,
                    "page_path": menu.page_path,
                    "created_at": menu.created_at.isoformat() if menu.created_at else None,
                    "updated_at": menu.updated_at.isoformat() if menu.updated_at else None,
                    "encryption_salt": menu.encryption_salt
                })
            else:
                print(f"Menu ID {menu_id} not found.")

        result.append({
            "id": role["id"],
            "role_id": role["role_id"],
            "status": role["status"],
            "menu_id": serialized_menus,
        })


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Roles menus fetched successfully",
            "status_code": status.HTTP_200_OK,
            "data": result
        }
    )

@router.get("/dropdown-options")
async def get_dropdown_options_endpoint(current_user=Depends(get_current_user),db: Session = Depends(get_db)):
    result = get_dropdown_options(db)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Dropdown options fetched successfully",
            "status_code": status.HTTP_200_OK,
            "data": result
        }
    )

@router.post("/tickets/create")
async def create_ticket(
    title: str = Form(...),
    message: str = Form(...),  # will contain HTML
    purpose_ids: List[int] = Form(...),
    ticket_status_id: int = Form(...),
    ticket_source_id: int = Form(...),
    priority_id: int = Form(...),
    assigned_to_id: int = Form(...),
    notification_type_ids: List[int] = Form(...),
    contact_id: int = Form(...),
    sla_id: int = Form(...),
    contact_ref_no: Optional[str] = Form(None),
    to_recipients: Optional[List[str]] = Form(None),
    cc_recipients: Optional[List[str]] = Form(None),
    reminder_datetime: Optional[str] = Form(None),  # e.g., "2025-05-15 06:37:02"
    attachments: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # if using auth
):
    try:
        ticket_id = f"TCKT-{uuid.uuid4().hex[:12].upper()}"
        
        # Fetch SLA times
        sla_obj = db.query(SlaConfiguration).filter_by(id=sla_id).first()
        if not sla_obj:
            raise HTTPException(status_code=400, detail="Invalid SLA")

        # Store Ticket
        ticket = Tickets(
            ticket_id=ticket_id,
            title=title,
            message=message,
            contact_ref_no=contact_ref_no,
            reminder_datetime=datetime.strptime(reminder_datetime, "%Y-%m-%d %H:%M:%S") if reminder_datetime else None,
            ticket_status_id=ticket_status_id,
            ticket_source_id=ticket_source_id,
            priority_id=priority_id,
            assigned_to_id=assigned_to_id,
            created_by_id=current_user.id,
            contact_id=contact_id,
            company_id=current_user.company_id,
            SLA=sla_id,
            purpose_type_id=json.dumps([str(pid) for pid in purpose_ids]),  # JSON stringified list of IDs
            notification_type_id=json.dumps([str(nt) for nt in notification_type_ids]),
            response_time=sla_obj.response_time,
            resolution_time=sla_obj.resolution_time,
            to_recipients=to_recipients,
            cc_recipients=cc_recipients,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        # Save attachments to TicketAttachment table
        if attachments:
            os.makedirs("uploads", exist_ok=True)
            for file in attachments:
                filename = f"{uuid.uuid4().hex}_{file.filename}"
                file_path = os.path.join("uploads", filename)
                with open(file_path, "wb") as f:
                    shutil.copyfileobj(file.file, f)

                attachment = TicketAttachment(
                    ticket_id=ticket.id,
                    file_url=file_path,
                    uploaded_by=current_user.id
                )
                db.add(attachment)
            db.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Ticket created successfully",
                "status_code": 201,
                "data": {
                    "id": ticket.id,
                    "ticket_id": ticket.ticket_id,
                    "title": ticket.title,
                    "status": ticket_status_id,
                    "assigned_to": assigned_to_id
                }
            }
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": f"Failed to create ticket: {str(e)}",
                "status_code": 500
            }
        )

@router.get("/tickets/get-all-tickets", response_model=TicketListResponse)
async def get_all_tickets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        tickets = db.query(Tickets).all()
        result = []

        for ticket in tickets:
            # Decode JSON string fields
            purpose_ids = json.loads(ticket.purpose_type_id or "[]")
            notification_type_ids = json.loads(ticket.notification_type_id or "[]")

            # Use JSON fields directly for these, no need to json.loads()
            to_recipients = ticket.to_recipients or []
            cc_recipients = ticket.cc_recipients or []

            # Fetch related entities
            ticket_status = db.query(TicketStatus).filter_by(id=ticket.ticket_status_id).first()
            priority = db.query(Priority).filter_by(id=ticket.priority_id).first()
            assigned_to = db.query(User).filter_by(id=ticket.assigned_to_id).first()
            source = db.query(TicketSource).filter_by(id=ticket.ticket_source_id).first()
            contact = db.query(Contact).filter_by(id=ticket.contact_id).first()
            sla = db.query(SlaConfiguration).filter_by(id=ticket.SLA).first()

            notification_types = db.query(NotificationType).filter(NotificationType.id.in_(notification_type_ids)).all()
            purpose_types = db.query(Purpose).filter(Purpose.id.in_(purpose_ids)).all()

            attachments = db.query(TicketAttachment).filter_by(ticket_id=ticket.id).all()
            attachment_urls = [a.file_url for a in attachments]

            result.append({
                "id": ticket.id,
                "ticket_id": ticket.ticket_id,
                "title": ticket.title,
                "message": ticket.message,
                "contact_ref_no": ticket.contact_ref_no,
                "ticket_status": ticket_status.name if ticket_status else None,
                "priority": priority.name if priority else None,
                "assigned_to": assigned_to.name if assigned_to else None,
                "created_by": ticket.createdBy.name if ticket.createdBy else None,
                "ticket_source": source.name if source else None,
                "contact": contact.name if contact else None,
                "sla": {
                    "name": sla.name if sla else None,
                    "response_time": sla.response_time if sla else None,
                    "resolution_time": sla.resolution_time if sla else None
                },
                "notification_types": [nt.name for nt in notification_types],
                "purposes": [pt.name for pt in purpose_types],
                "to_recipients": to_recipients,
                "cc_recipients": cc_recipients,
                "reminder_datetime": ticket.reminder_datetime.strftime("%Y-%m-%d %H:%M:%S") if ticket.reminder_datetime else None,
                "attachments": attachment_urls,
                "created_at": ticket.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": ticket.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Tickets fetched successfully",
                "status_code": status.HTTP_200_OK,
                "data": result
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tickets: {str(e)}")

@router.get("/tickets/get-ticket-byId/{id}", response_model=SingleTicketListResponse)  
def get_ticket(id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        ticket = db.query(Tickets).filter_by(id=id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")       

        # Decode JSON string fields
        purpose_ids = json.loads(ticket.purpose_type_id or "[]")
        notification_type_ids = json.loads(ticket.notification_type_id or "[]")

        # Use JSON fields directly as lists (already stored as list or null)
        to_recipients = ticket.to_recipients or []
        cc_recipients = ticket.cc_recipients or []

        # Fetch related entities
        ticket_status = db.query(TicketStatus).filter_by(id=ticket.ticket_status_id).first()
        priority = db.query(Priority).filter_by(id=ticket.priority_id).first()
        assigned_to = db.query(User).filter_by(id=ticket.assigned_to_id).first()
        source = db.query(TicketSource).filter_by(id=ticket.ticket_source_id).first()
        contact = db.query(Contact).filter_by(id=ticket.contact_id).first()
        sla = db.query(SlaConfiguration).filter_by(id=ticket.SLA).first()

        notification_types = db.query(NotificationType).filter(NotificationType.id.in_(notification_type_ids)).all()
        purpose_types = db.query(Purpose).filter(Purpose.id.in_(purpose_ids)).all()

        attachments = db.query(TicketAttachment).filter_by(ticket_id=ticket.id).all()
        attachment_urls = [a.file_url for a in attachments]

        result = {
            "id": ticket.id,
            "ticket_id": ticket.ticket_id,
            "title": ticket.title,
            "message": ticket.message,
            "contact_ref_no": ticket.contact_ref_no,
            "ticket_status": ticket_status.name if ticket_status else None,
            "priority": priority.name if priority else None,
            "assigned_to": assigned_to.name if assigned_to else None,
            "created_by": ticket.createdBy.name if ticket.createdBy else None,
            "ticket_source": source.name if source else None,
            "contact": contact.name if contact else None,
            "sla": {
                "name": sla.name if sla else None,
                "response_time": sla.response_time if sla else None,
                "resolution_time": sla.resolution_time if sla else None
            },
            "notification_types": [nt.name for nt in notification_types],
            "purposes": [pt.name for pt in purpose_types],
            "to_recipients": to_recipients,
            "cc_recipients": cc_recipients,
            "reminder_datetime": ticket.reminder_datetime.strftime("%Y-%m-%d %H:%M:%S") if ticket.reminder_datetime else None,
            "attachments": attachment_urls,
            "created_at": ticket.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": ticket.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Ticket fetched successfully",
                "status_code": status.HTTP_200_OK,
                "data": result
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch ticket: {str(e)}")

@router.put("/tickets/update-ticket/{id}", response_model=SingleTicketListResponse)
async def update_ticket(
    id: int,
    title: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    purpose_ids: Optional[List[int]] = Form(None),
    ticket_status_id: Optional[int] = Form(None),
    ticket_source_id: Optional[int] = Form(None),
    priority_id: Optional[int] = Form(None),
    assigned_to_id: Optional[int] = Form(None),
    notification_type_ids: Optional[List[int]] = Form(None),
    contact_id: Optional[int] = Form(None),
    sla_id: Optional[int] = Form(None),
    contact_ref_no: Optional[str] = Form(None),
    to_recipients: Optional[List[str]] = Form(None),
    cc_recipients: Optional[List[str]] = Form(None),
    reminder_datetime: Optional[str] = Form(None),
    attachments: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        ticket = db.query(Tickets).filter_by(id=id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        def check_and_update(field_name, new_value):
            if new_value is not None and getattr(ticket, field_name) != new_value:
                setattr(ticket, field_name, new_value)

        # Basic fields
        check_and_update("title", title)
        check_and_update("message", message)
        check_and_update("contact_ref_no", contact_ref_no)
        check_and_update("ticket_status_id", ticket_status_id)
        check_and_update("ticket_source_id", ticket_source_id)
        check_and_update("priority_id", priority_id)
        check_and_update("assigned_to_id", assigned_to_id)
        check_and_update("contact_id", contact_id)

        # SLA update
        if sla_id is not None and sla_id != ticket.SLA:
            sla_obj = db.query(SlaConfiguration).filter_by(id=sla_id).first()
            if not sla_obj:
                raise HTTPException(status_code=400, detail="Invalid SLA configuration")
            ticket.SLA = sla_id
            ticket.response_time = sla_obj.response_time
            ticket.resolution_time = sla_obj.resolution_time

        # Purpose IDs
        if purpose_ids is not None:
            new_purpose_set = set(map(str, purpose_ids))
            current_purpose_set = set(json.loads(ticket.purpose_type_id or "[]"))
            if new_purpose_set != current_purpose_set:
                ticket.purpose_type_id = json.dumps(list(new_purpose_set))

        # Notification type IDs
        if notification_type_ids is not None:
            new_notification_set = set(map(str, notification_type_ids))
            current_notification_set = set(json.loads(ticket.notification_type_id or "[]"))
            if new_notification_set != current_notification_set:
                ticket.notification_type_id = json.dumps(list(new_notification_set))

        # Recipients
        if to_recipients is not None and ticket.to_recipients != to_recipients:
            ticket.to_recipients = to_recipients
        if cc_recipients is not None and ticket.cc_recipients != cc_recipients:
            ticket.cc_recipients = cc_recipients

        # Reminder datetime
        if reminder_datetime is not None:
            new_reminder = datetime.strptime(reminder_datetime, "%Y-%m-%d %H:%M:%S")
            if ticket.reminder_datetime != new_reminder:
                ticket.reminder_datetime = new_reminder

        # Attachments (replace existing)
        if attachments:
            existing_attachments = db.query(TicketAttachment).filter_by(ticket_id=ticket.id).all()
            for att in existing_attachments:
                try:
                    if os.path.exists(att.file_url):
                        os.remove(att.file_url)
                except Exception:
                    pass
                db.delete(att)

            for file in attachments:
                filename = f"{uuid.uuid4().hex}_{file.filename}"
                file_path = os.path.join("uploads", filename)
                os.makedirs("uploads", exist_ok=True)
                with open(file_path, "wb") as f:
                    shutil.copyfileobj(file.file, f)

                attachment = TicketAttachment(
                    ticket_id=ticket.id,
                    file_url=file_path,
                    uploaded_by=current_user.id
                )
                db.add(attachment)

        ticket.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(ticket)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Ticket updated successfully",
                "status": status.HTTP_200_OK,
                "ticket_id": ticket.ticket_id,
                "id": ticket.id
            }
        )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update ticket: {str(e)}")

@router.delete("/tickets/delete-ticket/{id}")
def delete_ticket(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Fetch ticket by primary key
        ticket = db.query(Tickets).filter_by(id=id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found.")

        # Ensure only tickets with status 'new' can be deleted
        ticket_status = db.query(TicketStatus).filter_by(id=ticket.ticket_status_id).first()
        if not ticket_status or ticket_status.name.strip().lower() != "new":
            raise HTTPException(status_code=403, detail="Only tickets with status 'new' can be deleted.")

        # Delete all attachments (if any)
        attachments = db.query(TicketAttachment).filter_by(ticket_id=ticket.id).all()
        for attachment in attachments:
            try:
                os.remove(attachment.file_url)
            except FileNotFoundError:
                pass  # Ignore missing files
            db.delete(attachment)

        # Delete the ticket
        db.delete(ticket)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Ticket '{id}' with issue_ticket_id '{ticket.ticket_id}' deleted successfully",
                "status_code": status.HTTP_200_OK
            }
        )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete ticket: {str(e)}")










