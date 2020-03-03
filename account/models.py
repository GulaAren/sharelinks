from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


def user_dir_path(instance, filename):
    # TODO: enc url
    #       better url
    return '{}/{}'.format(instance.user.id, filename)


class Profile(models.Model):
    GENDERS = (('W', 'Wanita'), ('P', 'Pria'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo_profile = models.ImageField(upload_to=user_dir_path)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
