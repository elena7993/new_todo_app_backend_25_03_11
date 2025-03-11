from django.contrib import admin
from .models import Img

# Register your models here.


@admin.register(Img)
class ImgAdmin(admin.ModelAdmin):
    list_display = (
        "img_url",
        "user",
        "created_at",
        "updated_at",
    )
