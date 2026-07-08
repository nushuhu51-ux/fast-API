from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    title: set = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)
    
    
    
class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    #post.title
    
    id: int
    date_posted: str
    
    