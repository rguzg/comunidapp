from django.forms import ModelForm
from Apps.Users.models import User

class UserForm(ModelForm):
    def __init__(self, *args, **kargs):
        super(UserForm, self).__init__(*args, **kargs)

    class Meta:
         model = User
         fields = '__all__'