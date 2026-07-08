from django.contrib import admin
from .models import Post, Author, Tag


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "title",
        "date",
        "author",
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        Author.full_name,
        "username",
        "email_address",
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
