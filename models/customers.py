from typing import Optional

from pydantic import BaseModel


class Customer(BaseModel):
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postalcode: Optional[str] = None
    fax: Optional[str] = None
