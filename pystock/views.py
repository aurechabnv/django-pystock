from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')
        else:
            return redirect('stock:list')

    return render(request, 'home.html')
