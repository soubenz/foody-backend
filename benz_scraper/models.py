from tortoise.models import Model
from tortoise import fields



class Restaurant(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    pricing = fields.CharField(max_length=255)
    av_stars = fields.DecimalField(max_digits=2, decimal_places=1, null=True)
    category = fields.CharField(max_length=255)
    url = fields.CharField(max_length=500)
    address= fields.CharField(max_length=500, unique=True)
    description = fields.TextField( null=True)
    cover_img = fields.CharField(max_length=500, null=True)
    added_at = fields.DatetimeField(auto_now_add=True)
    reviews: fields.ReverseRelation["Review"]

    def __str__(self):
        return self.name
    
    class Meta:
        table = "restuarants"
        unique_together=(("name", "address"), )
        indexes =(("name", "address"), )

class Review(Model):
    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=255)
    stars = fields.FloatField()
    date: fields.DatetimeField()
    # reviewer_stats = fields.CharField(max_length=255)
    reviewer = fields.CharField(max_length=255)
    added_at = fields.DatetimeField(auto_now_add=True)
    restaurant: fields.ForeignKeyRelation[Restaurant] = fields.ForeignKeyField(
        "models.Restaurant", related_name="reviews"
    )


    class Meta:
        table = "reviews"
        # unique_together=(("name", "address"), )
        # indexes =(("name", "address"), )
