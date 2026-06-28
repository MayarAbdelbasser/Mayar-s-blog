from django.contrib import admin
from .models import Post, Author


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "title",
        "date",
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        Author.full_name,
        "email_address",
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
