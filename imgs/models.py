from django.db import models
from common.models import CommonModel

# Create your models here.


class Img(CommonModel):
    img_url = models.URLField()

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
