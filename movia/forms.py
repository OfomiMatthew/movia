from django import forms 
from .models import Review, RATE_CHOICES, Comment

class RateForm(forms.ModelForm):
  text = forms.CharField(widget=forms.Textarea(),required=False)
  rate = forms.ChoiceField(choices=RATE_CHOICES,widget=forms.Select(),required=True)
  
  
  class Meta:
    model = Review
    fields = ['text','rate']
    
class CommentForm(forms.ModelForm):
  body = forms.CharField(widget=forms.Textarea(),required=False)
  
  class Meta:
    model = Comment 
    fields = ['body']
    