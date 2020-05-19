from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
#from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from .models import Category, Post

list_display = ('title', 'category', 'cover_data', 'is_recommend', 'add_time', 'update_time')
    search_fields = ('title', 'desc', 'content')
    list_filter = ('category', 'tag', 'add_time')
    list_editable = ('category', 'is_recommend')
    date_hierarchy = 'created_date'
    readonly_fields = ('cover_admin', )
    list_display_links = ["title","created_date"]
    raw_id_fields = ('author',)
    list_per_page = 15

    fieldsets = (
        ('Article', {
            'fields': ('title', 'content')
        }),
        ('Admin Articles', {
            'classes': ('collapse', ),
            'fields': ('cover', 'cover_admin', 'desc', 'is_recommend', 'click_count', 'tag', 'category', 'add_time'),
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '59'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 59})},
    }
    """
    form = PostAdminForm
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        if (obj.published_date is None
                and obj.status in [Post.STATUS_PUBLISHED, Post.STATUS_ARCHIVED]):
            obj.published_date = timezone.now()
        if change:
            obj.updated_date = timezone.now()
        super(PostAdmin, self).save_model(request, obj, form, change)
    """
    #class Meta:
    #    model = Article


# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
