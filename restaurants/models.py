from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import confirmation_restaurant_email


class Restaurant(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100, null=False, blank=False)
    restaurant_slug = models.SlugField(max_length=100, blank=True)
    nipt = models.ImageField(upload_to='restaurants/nipt_images')
    is_approved = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            restaurant_status = Restaurant.objects.get(pk=self.pk)
            if restaurant_status.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                        'user': self.user,
                        'is_approved': self.is_approved,
                }
                if self.is_approved:
                    # send email
                    mail_subject = 'Congratulations! The restaurant has been approved'
                    confirmation_restaurant_email(mail_subject, mail_template, context)
                else:
                    # send email
                    mail_subject = 'We are sorry! You are not a restaurant. Please enter \
                        the information required and try again!'
                    mail_template = 'accounts/emails/admin_approval_email.html'
                    confirmation_restaurant_email(mail_subject, mail_template, context)
        return super(Restaurant, self).save(*args, **kwargs)
