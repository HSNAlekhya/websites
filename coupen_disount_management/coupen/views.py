from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CouponForm
from .agent import CouponAgent
from .models import Coupon


def dashboard(request):
	query = request.GET.get('q', '').strip()
	status = request.GET.get('status', '')
	coupons = Coupon.objects.all()
	if query:
		coupons = coupons.filter(Q(code__icontains=query) | Q(description__icontains=query))
	coupons = [coupon for coupon in coupons if not status or coupon.status.lower() == status.lower()]
	all_coupons = Coupon.objects.all()
	stats = {
		'total': len(all_coupons),
		'active': sum(coupon.status == 'Active' for coupon in all_coupons),
		'scheduled': sum(coupon.status == 'Scheduled' for coupon in all_coupons),
		'redemptions': sum(coupon.used_count for coupon in all_coupons),
	}
	return render(request, 'coupen/dashboard.html', {'coupons': coupons, 'stats': stats, 'query': query, 'status': status})


def coupon_create(request):
	form = CouponForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Coupon created successfully.')
		return redirect('dashboard')
	return render(request, 'coupen/coupon_form.html', {'form': form, 'heading': 'Create coupon'})


def coupon_edit(request, pk):
	coupon = get_object_or_404(Coupon, pk=pk)
	form = CouponForm(request.POST or None, instance=coupon)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Coupon updated successfully.')
		return redirect('dashboard')
	return render(request, 'coupen/coupon_form.html', {'form': form, 'heading': f'Edit {coupon.code}', 'coupon': coupon})


def coupon_delete(request, pk):
	coupon = get_object_or_404(Coupon, pk=pk)
	if request.method == 'POST':
		coupon.delete()
		messages.success(request, 'Coupon deleted.')
	return redirect('dashboard')


def agent_task(request):
	if request.method != 'POST':
		return redirect('dashboard')
	command = request.POST.get('command', '')
	response, affected = CouponAgent().run(command)
	return render(request, 'coupen/agent_result.html', {'command': command, 'response': response, 'affected': affected})
