from django import forms

class SearchForm(forms.Form):
    criteria = forms.CharField(label='Criteria', max_length=100, required=False)