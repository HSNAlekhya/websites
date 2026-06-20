from django.urls import reverse

def overview(request):
    """Refresh or compute overview data. Store a small message in session."""
    # Placeholder: user can replace with their Python logic
    request.session['last_action_msg'] = 'Overview refreshed — summary updated.'
    return 'overview'

def monthly(request):
    """Compute monthly trends placeholder."""
    request.session['last_action_msg'] = 'Monthly trends computed — check charts.'
    return 'monthly'

def toggle_theme(request):
    cur = request.session.get('alt_theme', False)
    request.session['alt_theme'] = not cur
    request.session['last_action_msg'] = 'Theme toggled.'
    return None

def recent_transactions(request):
    """Return the view name for recent transactions so the handler redirects there."""
    return 'transactions'
