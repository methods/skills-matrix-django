from django.shortcuts import render


def admin_dashboard_view(request):
    return render(request, 'admin_user/admin_dashboard.html')
