from django.shortcuts import render
from .models import Plant

# Create your views here.
def plant_list(request):
    plants = Plant.objects.all()
    return render(request, 'pests/plant_list.html', {'plants': plants})

# Details for a single plant
def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    pests = plant.pests.all()
    diseases = plant.diseases.all()
    return render(request, 'pests/plant_detail.html', {
        'plant': plant,
        'pests': pests,
        'diseases': diseases
    })