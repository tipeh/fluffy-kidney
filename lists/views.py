from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        new_text_item = request.POST["item_text"]
        Item.objects.create(text=new_text_item)
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

# Create your views here.
