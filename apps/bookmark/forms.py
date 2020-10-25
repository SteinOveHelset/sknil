from django.forms import ModelForm

from .models import Category, Bookmark

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description']
    
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'input'
        self.fields['title'].widget.attrs['v-model'] = 'title'
        self.fields['description'].widget.attrs['class'] = 'textarea'

class BookmarkForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ['title', 'description', 'url']
    
    def __init__(self, *args, **kwargs):
        super(BookmarkForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'input'
        self.fields['title'].widget.attrs['v-model'] = 'title'
        self.fields['url'].widget.attrs['class'] = 'input'
        self.fields['url'].widget.attrs['v-model'] = 'url'
        self.fields['description'].widget.attrs['class'] = 'textarea'