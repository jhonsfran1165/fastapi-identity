from sqlmodel import SQLModel
from fastapi_permissions import Allow, Authenticated


# Shared properties
class PlaceBase(SQLModel):
    id: int
    place_id: str
    place_type: str
    name: str
    full_name: str
    country_code: str
    country: str
    bounding_box: str

    def __acl__(self):
        return [
            (Allow, Authenticated, "view", "edit", "share", "create", "delete", "list"),
            # (Allow, "role:admin", "edit"),
            # (Allow, f"user:{self.owner}", "delete"),
            # (Allow, Authenticated, "view"),
            # (Allow, "role:admin", "edit"),
            # (Allow, f"user:{self.owner}", "delete"),
        ]


# Additional properties to return via API
class Place(PlaceBase):
    pass
