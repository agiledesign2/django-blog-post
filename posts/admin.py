from django.contrib import admin
from django.utils import timezone
from django.db import models
from django.forms import TextInput, Textarea
#from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from .models import Category, Post

#@admin.register(Article)
class PostAdmin(admin.ModelAdmin):	#(ImportExportModelAdmin):
    list_display = (
        'title', 'author', 'content', 'description', 'allow_comments', 
        'tags', 'status', 'views_count', 'created', 'updated', 'published'
    )
    search_fields = ('title', 'author', 'description', 'content', 'published')
    list_filter = ('category', 'author', 'tags', 'published')
    list_editable = ('allow_comments',)
    date_hierarchy = 'published'
    #readonly_fields = ('cover_admin', )
    list_display_links = ["title","published"]
    raw_id_fields = ('author',)
    list_per_page = 15

    fieldsets = (
        ('Post', {
            'fields': ('title', 'category', 'content', 'description', 'allow_comments', 'tags', 'status')
        }),
        ('Admin Posts', {
            'classes': ('collapse', ),
            'fields': ( 
            	'published',
            ),
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '59'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 59})},
    }
    """
    form = PostAdminForm
    prepopulated_fields = {'slug': ('title',)}
    """

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        if (obj.published is None
                and obj.status in [Post.STATUS_PUBLISHED]):
            obj.published = timezone.now()
        if change:
            obj.updated = timezone.now()
        super(PostAdmin, self).save_model(request, obj, form, change)

    #class Meta:
    #    model = Article


# Register your models here.
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
