from django.contrib import admin
from .models import Product , Comment

admin.site.register(Product)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user' , 'product','body' , 'created' , 'is_reply' ,'status')
    list_editable = ['status']
    raw_id_fields = ('user','product' , 'reply' )

    @admin.action(description='تایید کامنت‌های انتخاب‌شده')
    def approve_comments(self, request, queryset):
        queryset.update(status=Comment.Status.APPROVED)

    @admin.action(description='رد کامنت‌های انتخاب‌شده')
    def reject_comments(self, request, queryset):
        queryset.update(status=Comment.Status.REJECTED)
# Register your models here.
