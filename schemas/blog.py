from datetime import date
from pydantic import BaseModel, root_validator
from typing import Optional


class CreateBlog(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None

    @root_validator(pre=True)
    def generate_slug(cls, values):
        """
        Generate a slug based on the provided title.

        Parameters:
            cls (type): The class of the instance.
            values (dict): The values to generate the slug from.

        Returns:
            dict: The updated values with the generated slug.
        """
        title = values.get("title")
        if title is not None:
            values["slug"] = title.replace(" ", "-").lower()
        return values




# kind of implemented
class UpdateBlog(CreateBlog):
    pass
