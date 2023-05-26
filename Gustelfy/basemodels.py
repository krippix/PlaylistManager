import pydantic

class Diff(pydantic.BaseModel):
    tracks: list[list,list]