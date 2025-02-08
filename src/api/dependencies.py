from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends, Query

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=None, ge=1)]
    per_page: Annotated[int | None, Query(default=None, ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]