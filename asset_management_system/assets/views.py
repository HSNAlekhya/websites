from django.shortcuts import render, redirect
from .models import Asset, AssetRequest
from .forms import AssetForm, RequestForm
from accounts.models import Employee
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def dashboard(request):
    assets = Asset.objects.all()
    return render(request, 'dashboard.html', {'assets': assets})


@login_required(login_url='/accounts/login/')
def add_asset(request):
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AssetForm()
    return render(request, 'add_asset.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404

@login_required(login_url='/accounts/login/')
def request_asset(request, asset_id=None):
    try:
        emp = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('/accounts/register/')

    asset = None
    if asset_id is not None:
        asset = get_object_or_404(Asset, pk=asset_id)

    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employee = emp
            obj.save()
            return redirect('dashboard')
    else:
        initial = {'asset': asset} if asset is not None else None
        form = RequestForm(initial=initial)

    return render(request, 'request_asset.html', {'form': form})
# Create your views here.
