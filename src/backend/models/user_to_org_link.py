from uuid import UUID

from sqlmodel import SQLModel, Field


class UserToOrgLink(SQLModel, table=True):
    __tablename__ = "user_to_org_link"

    user_id: UUID = Field(default=None, foreign_key="users.user_id", primary_key=True)
    org_id: UUID = Field(default=None, foreign_key="organisations.org_id", primary_key=True)
