from django.contrib import admin

from social_media.models import Post, Comment, Like, Follow

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
