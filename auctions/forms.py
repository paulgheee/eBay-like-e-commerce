from django import forms

class CreateListing(forms.Form):
    title = forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control", "id":"exampleFormControlInput1", "placeholder":"Title"}))
    textDescription = forms.CharField(label="",widget=forms.Textarea(attrs={"class":"form-control", "id":"exampleFormControlTextarea1", "placeholder":"Text Description"}))
    startingBid = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", "id":"exampleFormControlInput1", "placeholder":"Starting Bid"}))
    imageURL =  forms.URLField(label='', required=False, widget=forms.URLInput(attrs={"class":"form-control", "id":"exampleFormControlInput1", "placeholder":"URL Image"}))
    OPTIONS = (
        ('','Select category'),
        ('fashion','Fashion'),
        ('toys','Toys'),
        ('electronics','Electronics'), 
        ('home','Home'), 
        ('other','Other')
        )
    category = forms.ChoiceField(label='', required=False, choices=OPTIONS, widget=forms.Select(attrs={"class":"form-control form-select"}))

class Comment(forms.Form):
    comment = forms.CharField(label="", max_length=300, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Write a comment"}))

class Bid(forms.Form):
    bid = forms.FloatField(label="", widget=forms.TextInput(attrs={"class":"form-control", "id":"exampleFormControlInput1", "placeholder":"Bid"}))

class Category(forms.Form):
    OPTIONS = (
        ('','Select category'),
        ('fashion','Fashion'),
        ('toys','Toys'),
        ('electronics','Electronics'), 
        ('home','Home'), 
        ('other','Other')
        )
    category = forms.ChoiceField(label="", choices=OPTIONS, widget=forms.Select(attrs={"class":"form-control form-select"}))