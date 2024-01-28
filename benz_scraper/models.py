
from pydantic import BaseModel


class RestaurantReview(BaseModel):
    id: int
    text: str = None
    stars: str
    date: str

class RestaurantMetadata(BaseModel):
    name: str
    category: str
    nb_reviews: str
    average_rating: str
    # text: str = None
    # stars: str
    # date: str