from pydantic import BaseModel, root_validator, constr
from typing import List, Optional, Literal

class UpdateXpath(BaseModel):
    xpath:constr(min_length=1)
    tlid:constr(min_length=1)
    