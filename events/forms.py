from django import forms
from events import models


class StyledFormMixin:
    """Mixing to apply style to form field"""

    default_classes = "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-5"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or isinstance(
                field.widget, forms.EmailInput
            ):
                field.widget.attrs.update(
                    {
                        "class": self.default_classes,
                        "placeholder": f"Enter {field.label.lower()}",
                    }
                )
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {
                        "class": self.default_classes,
                        "placeholder": f"Enter {field.label.lower()}",
                        "rows": 5,
                    }
                )
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update(
                    {
                        "class": "shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline "
                    }
                )
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.update({"class": "space-y-2"})
            elif isinstance(field.widget, forms.ImageField):
                field.widget.attrs.update(
                    {"class": "border rounded w-xl py-2 px-3 text-gray-700 "}
                )


class EventForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = models.Event
        fields = "__all__"
        widgets = {
            "category": forms.Select,
            "date": forms.SelectDateWidget,
        }
        labels = {
            "name": "Event Name",
            "description": "Event Description"
        }
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'hidden'
        })
        self.apply_styled_widgets()



class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = models.Category
        fields = "__all__"

        labels = {
            "name": "Category Name",
            "description": "Category Description"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

class SearchForm(StyledFormMixin, forms.Form):  
    name = forms.CharField(
        max_length=100,
        required=False,
        label='',  # Remove the label
        widget=forms.TextInput(attrs={'placeholder': 'Enter your search term...', "class": "form-control"})  # Add a placeholder
    )
    categories = models.Category.objects.all()
    CHOICES = (("all", "all"),)
    for category in categories:
        CHOICES = (*CHOICES, (category.name, category.name),)
    # CHOICES = (("GOOD", "GOOD"),)
    category = forms.ChoiceField(choices=CHOICES, required=False, label="")
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
