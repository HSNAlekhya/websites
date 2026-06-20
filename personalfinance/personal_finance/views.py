from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import importlib
from django.urls import reverse
from datetime import datetime, date
from collections import OrderedDict
import json


def dashboard(request):
    year = timezone.now().year
    transactions = request.session.get('transactions', [])
    # Pass theme and last action message from session
    alt_theme = request.session.get('alt_theme', False)
    last_action_msg = request.session.pop('last_action_msg', None)
    # Compute overview stats from session-stored transactions
    total = 0.0
    count = 0
    month_totals = OrderedDict()
    # prepare last 6 months keys
    today = date.today()
    for i in range(5, -1, -1):
        m = (today.month - i - 1) % 12 + 1
        y = today.year + ((today.month - i - 1) // 12)
        key = f"{y}-{m:02d}"
        month_totals[key] = 0.0

    for t in transactions:
        count += 1
        try:
            amt = float(t.get('amount') or 0)
        except Exception:
            amt = 0.0
        total += amt
        # parse date and attribute to month
        dstr = t.get('date') or ''
        try:
            d = datetime.fromisoformat(dstr).date()
            key = f"{d.year}-{d.month:02d}"
            if key in month_totals:
                month_totals[key] += amt
        except Exception:
            pass

    # Format month labels and values for template
    month_labels = [k for k in month_totals.keys()]
    month_values = [round(v, 2) for v in month_totals.values()]

    # Build simple chart geometry for SVG (600x60 area)
    chart_width = 600
    chart_height = 60
    n = len(month_values) or 1
    bw = chart_width / n
    maxv = max(month_values) if month_values else 0.0
    chart_bars = []
    for i, val in enumerate(month_values):
        width = bw * 0.7
        x = i * bw + (bw - width) / 2
        height = (maxv > 0) and (val / maxv * chart_height) or 0
        y = chart_height - height
        chart_bars.append({'x': round(x,2), 'y': round(y,2), 'width': round(width,2), 'height': round(height,2), 'label': month_labels[i], 'value': val})


    context = {
        'year': year,
        'transactions': transactions,
        'alt_theme': alt_theme,
        'last_action_msg': last_action_msg,
        'overview_total': round(total, 2),
        'overview_count': count,
        # simple placeholder conversion rate USD -> INR (user can replace with live rate)
        'overview_total_inr': round(total * 82.0, 2),
        'month_labels': month_labels,
        'month_values': month_values,
        'chart_bars': chart_bars,
    }
    return render(request, 'dashboard.html', context)


def transactions_view(request):
    transactions = request.session.get('transactions', [])
    year = timezone.now().year
    alt_theme = request.session.get('alt_theme', False)
    last_action_msg = request.session.pop('last_action_msg', None)
    # compute total amount for display
    total = 0.0
    for t in transactions:
        try:
            total += float(t.get('amount') or 0)
        except Exception:
            pass
    total = round(total, 2)
    return render(request, 'transactions.html', {'transactions': transactions, 'year': year, 'alt_theme': alt_theme, 'last_action_msg': last_action_msg, 'total_amount': total})


def delete_transaction(request, idx):
    """Delete a transaction at the given zero-based index from session-stored transactions."""
    if request.method != 'POST':
        request.session['last_action_msg'] = 'Invalid delete request method.'
        return redirect('transactions')
    txs = request.session.get('transactions', [])
    try:
        removed = txs.pop(idx)
        request.session['transactions'] = txs
        request.session['last_action_msg'] = f"Deleted transaction: {removed.get('description', '')} ({removed.get('amount', '')})"
    except Exception:
        request.session['last_action_msg'] = 'Failed to delete transaction.'
    return redirect('transactions')


def add_transaction(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        receipt = request.FILES.get('receipt')
        receipt_url = None
        if receipt:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(receipt.name, receipt)
            # fs.url returns path relative to MEDIA_URL only when using default storage configured
            receipt_url = settings.MEDIA_URL + filename
        tx = {'date': date, 'description': description, 'amount': amount, 'receipt': receipt_url}
        txs = request.session.get('transactions', [])
        txs.append(tx)
        request.session['transactions'] = txs
        return redirect('transactions')
    year = timezone.now().year
    alt_theme = request.session.get('alt_theme', False)
    last_action_msg = request.session.pop('last_action_msg', None)
    return render(request, 'add_transaction.html', {'year': year, 'alt_theme': alt_theme, 'last_action_msg': last_action_msg})


def action_handler(request, action):
    """Call server-side action functions defined in personal_finance.actions.
    The action function may modify session and optionally return a view name to redirect to.
    """
    try:
        actions = importlib.import_module('personal_finance.actions')
        func = getattr(actions, action)
    except Exception:
        request.session['last_action_msg'] = f'Unknown action: {action}'
        return redirect('dashboard')
    try:
        result = func(request)
        # if action returned a view name, redirect there
        if isinstance(result, str):
            # assume result is a URL name
            try:
                return redirect(result)
            except Exception:
                # fallback to reverse
                return redirect(reverse(result))
    except Exception as e:
        request.session['last_action_msg'] = f'Action error: {e}'
    return redirect('dashboard')


def overview_view(request):
    # reuse dashboard computations but present a fuller overview
    transactions = request.session.get('transactions', [])
    total = sum([float(t.get('amount') or 0) for t in transactions]) if transactions else 0.0
    count = len(transactions)
    recent = list(reversed(transactions))[:5] if transactions else [
        {'date': '2026-06-01', 'description': 'Sample coffee', 'amount': '3.50'},
        {'date': '2026-06-02', 'description': 'Sample groceries', 'amount': '24.75'},
    ]
    summary = {
        'total': round(total,2),
        'count': count,
        'recent': recent,
    }
    alt_theme = request.session.get('alt_theme', False)
    last_action_msg = request.session.pop('last_action_msg', None)
    return render(request, 'overview.html', {'summary': summary, 'alt_theme': alt_theme, 'last_action_msg': last_action_msg})


def monthly_view(request):
    transactions = request.session.get('transactions', [])
    # compute last 6 months totals similar to dashboard
    today = date.today()
    month_totals = OrderedDict()
    for i in range(5, -1, -1):
        m = (today.month - i - 1) % 12 + 1
        y = today.year + ((today.month - i - 1) // 12)
        key = f"{y}-{m:02d}"
        month_totals[key] = 0.0
    for t in transactions:
        try:
            amt = float(t.get('amount') or 0)
        except Exception:
            amt = 0.0
        dstr = t.get('date') or ''
        try:
            d = datetime.fromisoformat(dstr).date()
            key = f"{d.year}-{d.month:02d}"
            if key in month_totals:
                month_totals[key] += amt
        except Exception:
            pass
    labels = list(month_totals.keys())
    values = [round(v,2) for v in month_totals.values()]
    # prepare chart bars (600x90 drawing area)
    chart_width = 600
    chart_height = 90
    n = len(values) or 1
    bw = chart_width / n
    maxv = max(values) if values else 0.0
    chart_bars = []
    for i, val in enumerate(values):
        width = bw * 0.6
        x = i * bw + (bw - width) / 2
        height = (maxv > 0) and (val / maxv * (chart_height - 20)) or 0
        y = chart_height - height
        chart_bars.append({'x': round(x,2), 'y': round(y,2), 'width': round(width,2), 'height': round(height,2), 'label': labels[i], 'value': val})

    alt_theme = request.session.get('alt_theme', False)
    last_action_msg = request.session.pop('last_action_msg', None)
    labels_json = json.dumps(labels)
    values_json = json.dumps(values)
    return render(request, 'monthly.html', {'labels': labels, 'values': values, 'chart_bars': chart_bars, 'labels_json': labels_json, 'values_json': values_json, 'alt_theme': alt_theme, 'last_action_msg': last_action_msg})
