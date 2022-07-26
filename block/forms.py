from django.forms import ModelForm, widgets
from django.forms.fields import ImageField
from . models import block
from django import forms

class blockForm(forms.ModelForm):
    class Meta:
        model= block
        
        fields = '__all__'
        # widgets ={
        #     'user' = forms.TextInput(attrs={'class':'form-control'}),
        #     'title' = forms.TextInput(attrs={'class':'form-control'}),
        #     'cover_image' = forms.ImageField(attrs={'class':'form-control'}),
        #     'description_block' = forms.TextInput(attrs={'class':'form-control'}),
        #     'developer' = forms.TextInput(attrs={'class':'form-control'}),
        #     'rating' = forms.TextInput(attrs={'class':'form-control'}),

        #     'download' = forms.TextInput(attrs={'class':'form-control'}),
        #     'screenshots' = forms.ImageField(attrs={'class':'form-control'}),
        #     'review' = forms.TextInput(attrs={'class':'form-control'}),
        #     'demo' = forms.ImageField(attrs={'class':'form-control'}),

        # }
