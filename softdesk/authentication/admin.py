from django.contrib import admin

# Register your models here.


from authentication.models import User

admin.site.register(User)