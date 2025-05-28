from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
from typing import Optional, List

class RoleMenuPermission(Base):
    __tablename__ = "role_menu_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_menu_id = Column(Integer, ForeignKey("roles_menus.id"), nullable=False)
    objects = Column(JSON, nullable=True)
    status = Column(String(50), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    roles_menu = relationship("RolesMenu", back_populates="role_menu_permissions")
    role = relationship("Role", back_populates="role_menu_permissions")
    # menus relationship depends on RolesMenu — typically you'd access menus via roles_menu

    def get_menu_names(self, db) -> Optional[str]:
        """
        Simulates Laravel accessor getMenuNamesAttribute:
        - fetches menu IDs stored as JSON in roles_menu.menu_id
        - queries Meneus for names and joins them
        """
        if not self.roles_menu or not self.roles_menu.menu_id:
            return None

        import json
        try:
            menu_ids = json.loads(self.roles_menu.menu_id)
        except Exception:
            return None
        
        from models.meneus import Meneus
        menus = db.query(Meneus).filter(Meneus.id.in_(menu_ids)).all()
        names = [menu.name for menu in menus]
        return ", ".join(names)

