from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from posts.models import Post


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin", "admin@domain.com", "admin")
        if not User.objects.filter(username="editor").exists():
            User.objects.create_user(
            	'editor', 'editor@domain.com', 'editor')
        if not User.objects.filter(username="normal").exists():
            User.objects.create_user(
            	'normal', 'normal@domain.com', 'normal')
        from django.contrib.auth.models import Group

		Group.objects.create(name='Name of the group')
		# g1.user_set.add(user1, user2, user5, user7)
		# g1.permissions.add(perm1, perm3, perm4)


		#new_group, created = Group.objects.get_or_create(name='new_group')
		# Code to add permission to group ???
		ct = ContentType.objects.get_for_model(Post)
		# Now what - Say I want to add 'Can add project' permission to new_group?
		#new_group, created = Group.objects.get_or_create(name='new_group')
		proj_add_perm = Permission.objects.get(name='Can add project')
		new_group.permissions.add(proj_add_perm)
            self.stdout.write(self.style.SUCCESS('Users has created'))
        else:
            self.stdout.write(self.style.SUCCESS('Users already exists'))
