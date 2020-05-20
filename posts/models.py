from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
#from ckeditor.fields import RichTextField
#from django.utils.html import format_html
#from mdeditor.fields import MDTextField

from django.conf import settings


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        # app_label = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("posts:category", kwargs={"name": self.name})
    """
class Category(models.Model):
    """
    #Category
    """
    name = models.CharField(max_length=30, verbose_name='Name')
    index = models.IntegerField(default=99, verbose_name='Index')
    active = models.BooleanField(default=True, verbose_name='Active')
    icon = models.CharField(max_length=30, default='fa-home',verbose_name='Icon')

    # Get all Categorys
    def get_items(self):
        return len(self.article_set.all())

    def icon_data(self):
        return format_html(
            '<i class="{}"></i>',
            self.icon,
        )

    get_items.short_description = 'Categorys'
    icon_data.short_description = 'Icon'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
"""

class PostQuerySet(models.QuerySet):
    def active(self):
        """
        Return all published and archived posts
        """
        return self.filter(status__in=[Post.STATUS_PUBLISHED, Post.STATUS_ARCHIVED])

    def published(self):
        """
        Return all published posts
        """
        return self.filter(status=Post.STATUS_PUBLISHED)

    def draft(self):
        """
        Return all defted posts
        """
        return self.filter(status=Post.STATUS_DRAFT)


class Post(models.Model):
    STATUS_DRAFT = 1
    STATUS_PUBLISHED = 2
    #STATUS_ARCHIVED = 3
    STATUS = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        #(STATUS_ARCHIVED, 'Archived'),
    )
    #STATUS = (("DRAFT", "Draft"), ("PUBLISHED", "Published"))
    #STATE_CHOICES = PINAX_BLOG_STATE_CHOICES
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="autors",
        verbose_name=_("Author"),
        on_delete=models.CASCADE
    )
    #author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(_("Title"), max_length=300)
    category = models.ManyToManyField(Category,_("Category"), blank=False)
    #category = models.ForeignKey(Category, blank=True, null=True, verbose_name='Category', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique_for_date="published")
    #slug = models.SlugField(max_length=255, unique=True)
    content = MarkdownxField()  # markdownx
    #content = RichTextField()
    #content = MDTextField(verbose_name='Content')
    description = models.TextField(_("Description"), max_length=150, help_text="Enter you description text here.")
    #description = models.TextField(max_length=2000, help_text="Enter you blog text here.")
    #cover = models.CharField(max_length=200, default='https://image.3001.net/images/20200304/15832956271308.jpg', verbose_name='Cover')
    created = models.DateTimeField(_("Created"), default=timezone.now, editable=False)  # when first revision was created
    updated = models.DateTimeField(_("Updated"), null=True, blank=True)  # when last revision was created (even if not published)
    #published = models.DateTimeField(_("Published"), auto_now=True)  # when last published
    published = models.DateTimeField(_("Published"), null=True, blank=True)  # when last published
    #published_date = models.DateTimeField(auto_now=True)
    #is_recommend = models.BooleanField(default=False, verbose_name='Is Recommend')
    allow_comments = models.BooleanField(default=True)
    #status = models.CharField(default="DRAFT", choices=STATUS, max_length=10)
    status = models.SmallIntegerField(_("State"), choices=STATUS)
    #status = models.IntegerField(_("State"), choices=STATE_CHOICES, default=STATE_CHOICES[0][0])
    views_count = models.IntegerField(_("View count"), default=0, editable=False)
    #click_count = models.IntegerField(default=0, verbose_name='Click Count')
    #tag = models.ManyToManyField(Tag, verbose_name='Tag')

    # tags mechanism
    tags = TaggableManager(blank=True)
    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ("-published",)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Redirect to post detail view
        """
        return reverse("posts:details_post", kwargs={"slug": self.slug})

    @property
    def formatted_markdown(self):
        """
        To properly display markdowned content field
        """
        return markdownify(self.content)

    def viewed(self):
        """
        Increment post view count
        """
        self.view_count += 1
        self.save(update_fields=['view_count'])
        #self.current().viewed()

        """

    def viewed(self):
        """
        #Viewed
        """
        self.click_count += 1
        self.save(update_fields=['click_count'])

    def cover_data(self):
        return format_html(
            '<img src="{}" width="156px" height="98px"/>',
            self.cover,
        )

    def cover_admin(self):
        return format_html(
            '<img src="{}" width="440px" height="275px"/>',
            self.cover,
        )

    cover_data.short_description = 'Cover'
    cover_admin.short_description = 'Admin Cover'

    """
