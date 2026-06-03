from pydantic import BaseModel

class RepoRequest(BaseModel):

    owner: str

    repo_name: str