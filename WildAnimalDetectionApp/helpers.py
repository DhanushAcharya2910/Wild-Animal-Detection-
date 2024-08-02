from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from WildAnimalDetectionApp.models import User

def send_email_to_user(user_id):
    users = User.objects.filter(id=user_id).first()

    # Using list comprehension to create a list of email addresses
    email_list = [users.email]
    subject = "Wild Animal Detection Alert"
    message = f'''Dear {users.name},

We would like to inform you that your request for wild animal detection has been successfully completed and we detect the wild animal.


Best regards,
Wild Animal Detection Community Team
'''
   
    from_email = settings.EMAIL_HOST_USER
    to_email = email_list
    send_mail(subject, message, from_email, to_email)
    print("Email sent successfully...")



def send_email_to_officer(user_id):
    users = User.objects.filter(id=user_id).first()

    # Using list comprehension to create a list of email addresses
    emails = "sahil26faraz@gmail.com"
    email_list = [emails]
    subject = "Wild Animal Detection Alert"
    message = f'''Dear Officer,

We would like to inform you that your request for wild animal detection has been successfully completed and we detect the wild animal.
For location information please contact this person :  Name: {users.name},  Contact: {users.contact} and Address :  {users.address}


Best regards,
Wild Animal Detection Community Team
'''
    from_email = settings.EMAIL_HOST_USER
    to_email = email_list
    send_mail(subject, message, from_email, to_email)
    print(" Officer Email sent successfully...")