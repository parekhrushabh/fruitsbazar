from django import forms
from app_module.admin_app import models

class commentsdata(forms.ModelForm):
    class Meta:
        model = models.comments
        fields = '__all__'

class contectdata(forms.ModelForm):
    class Meta:
        model = models.contect
        fields = '__all__'

class subscribedata(forms.ModelForm):
    class Meta:
        model = models.subscribe
        fields = '__all__'

class categorydata(forms.ModelForm):
    class Meta:
        model = models.category
        fields = '__all__'

# class subcategorydata(forms.ModelForm):
#     class Meta:
#         model = models.subcategory
#         fields = '__all__'

class productdata(forms.ModelForm):
    class Meta:
        model = models.product
        fields = '__all__'

class productimagedata(forms.ModelForm):
    class Meta:
        model = models.productimage
        fields = '__all__'

class UserStatusdata(forms.ModelForm):
    class Meta:
        model = models.UserStatus
        fields = '__all__'