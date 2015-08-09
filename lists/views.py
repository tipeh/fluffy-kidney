from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        new_text_item = request.POST["item_text"]
        Item.objects.create(text=new_text_item)
        return redirect("/")

    items = Item.objects.all()

    return render(request, 'home.html', {'items':items})

# Create your views here.
