from rich import print
from rich.traceback import install
from pydantic import BaseModel, ConfigDict

install(show_locals=True)


class incoming_message(BaseModel):
    message: str
