from django import forms

class SearchForm(forms.Form):
    searchinput = forms.CharField(label=False,max_length=10,
                                            widget=forms.TextInput(attrs={"class":"searchinput","id":"searchinput"}))

class VehicalForm(forms.Form):
    vehicleno = forms.CharField(label=False,max_length=10,
                                widget=forms.TextInput(attrs={"id":"vehicleno"}))
    brand = forms.CharField(label=False,max_length=25,
                            widget=forms.TextInput(attrs={"id":"brand"}))
    model = forms.CharField(label=False,max_length=12,
                            widget=forms.TextInput(attrs={"id":"model"}))

# class ServicesForm(forms.Form):
#     # serviceid = forms.CharField(label=False,max_length=10,
#     #                             widget=forms.TextInput(attrs={"id":"serviceid"}))
#     serviceid = forms.IntegerField(label=False,widget=forms.HiddenInput(attrs={"id":"serviceid"}))
#     servicetype = forms.CharField(label=False,max_length=10,
#                                 widget=forms.TextInput(attrs={"id":"servicetype"}))
#     vehicleno = forms.CharField(label=False,max_length=10,
#                                 widget=forms.HiddenInput(attrs={"id":"vehicleno"}))

class updateServiceForm(forms.Form):
    servicetype = forms.CharField(label=False,max_length=10,
                                widget=forms.TextInput(attrs={"id":"servicetype"}))
    vehicleno = forms.CharField(label=False,max_length=10,
                                widget=forms.HiddenInput(attrs={"id":"vehicleno"}))