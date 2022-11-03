from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    print(created)
    if created:
        print('create the user profile')
        UserProfile.objects.create(user=instance)
        print('User profile is created!')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            #  create userprofile if not exist
            UserProfile.objects.create(user=instance)
            print('profile did not exist but, I created one')
        print('user is updated')


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):  # will trigger just before user is created
    print(instance.username, 'we are saving this user')
#  post_save.connect(post_save_create_profile, sender=User)