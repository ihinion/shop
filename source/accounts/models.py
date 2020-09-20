from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='User')
    githubprofile = models.URLField(null=True, blank=True, verbose_name='Github profile')
    about = models.TextField(max_length=2000, null=True, blank=True, verbose_name='About')
    profile_pic = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Profile pic')

    class Meta:
        permissions = [
            ("can_view_user_list", "Can view the list of users"),
            ('can_manage_users', 'Can manage users'),
        ]

    def __str__(self):
        return self.user.username + "'s Profile"

