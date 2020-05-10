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
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=99, verbose_name='分类排序')
    active = models.BooleanField(default=True, verbose_name='是否添加到菜单')
    icon = models.CharField(max_length=30, default='fa-home',verbose_name='菜单图标')

    # 统计文章数 并放入后台
    def get_items(self):
        return len(self.article_set.all())

    def icon_data(self):
        return format_html(
            '<i class="{}"></i>',
            self.icon,
        )

    get_items.short_description = '文章数'
    icon_data.short_description = '图标预览'

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
"""

class PostQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=[Post.STATUS_PUBLISHED, Post.STATUS_ARCHIVED])

    def published(self):
        return self.filter(status=Post.STATUS_PUBLISHED)


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

    category = models.ManyToManyField(Category,_("Category"), blank=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="autors",
        verbose_name=_("Author"),
        on_delete=models.CASCADE
    )
    #author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(_("Title"), max_length=300)
    slug = models.SlugField(max_length=255, unique_for_date="published_date")
    #slug = models.SlugField(max_length=255, unique=True)
    content = MarkdownxField()  # markdownx
    #content = RichTextField()
    #published_date = models.DateTimeField(auto_now=True)
    description = models.TextField(_("Description"), max_length=150, help_text="Enter you description text here.")
    #description = models.TextField(max_length=2000, help_text="Enter you blog text here.")
    #cover = models.CharField(max_length=200, default='https://image.3001.net/images/20200304/15832956271308.jpg', verbose_name='文章封面')
    #content = MDTextField(verbose_name='文章内容')
    created = models.DateTimeField(_("Created"), default=timezone.now, editable=False)  # when first revision was created
    updated = models.DateTimeField(_("Updated"), null=True, blank=True, editable=False)  # when last revision was created (even if not published)
    published = models.DateTimeField(_("Published"), null=True, blank=True)  # when last published
    #click_count = models.IntegerField(default=0, verbose_name='点击次数')
    #is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    allow_comments = models.BooleanField(default=True)
    #status = models.CharField(default="DRAFT", choices=STATUS, max_length=10)
    status = models.SmallIntegerField(_("State"), choices=STATUS)
    #state = models.IntegerField(_("State"), choices=STATE_CHOICES, default=STATE_CHOICES[0][0])
    views_count = models.IntegerField(_("View count"), default=0, editable=False)
    #category = models.ForeignKey(Category, blank=True, null=True, verbose_name='文章分类', on_delete=models.CASCADE)
    #tag = models.ManyToManyField(Tag, verbose_name='文章标签')

    # tags mechanism
    tags = TaggableManager(blank=True)
    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ("-published",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:details_post", kwargs={"slug": self.slug})

    @property
    def formatted_markdown(self):
        """
        To properly display markdowned content field
        """
        return markdownify(self.content)

    def is_draft(self):
        return self.status == "DRAFT"

    def viewed(self):
        self.view_count += 1
        self.save()
        self.current().viewed()

        """
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

    def viewed(self):
        """
        #Viewed
        """
        self.click_count += 1
        self.save(update_fields=['click_count'])

    cover_data.short_description = '文章封面'
    cover_admin.short_description = '文章封面'

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
    """
        """
    class Meta:
        ordering = ["-post_date"]
    
    def get_absolute_url(self):
        """
        #Returns the url to access a particular blog instance.
        """
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        """
        #String for representing the Model object.
        """
        return self.name
    """
