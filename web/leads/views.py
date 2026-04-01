from django.shortcuts import render, redirect
from .models import Lead
from .forms import LeadForm  # импорт из forms.py

def lead_list(request):
    leads = Lead.objects.all().order_by('-created_at')
    return render(request, 'leads/lead_list.html', {'leads': leads})

def add_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    else:
        form = LeadForm()
    return render(request, 'leads/add_lead.html', {'form': form})