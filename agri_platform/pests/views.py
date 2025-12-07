from django.shortcuts import render, get_object_or_404, redirect
from .models import Plant
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
from PIL import Image
import tempfile
import os
import requests
from agriapp.models import FarmerProfile

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

# Pest diagnosis data
PEST_DATABASE = {
    'Tomato Early Blight': {
        'symptoms': 'Brown circular spots with concentric rings on lower leaves',
        'treatment': 'Remove infected leaves, spray with copper fungicide weekly',
        'prevention': 'Provide good air circulation, avoid overhead watering'
    },
    'Tomato Late Blight': {
        'symptoms': 'Water-soaked spots on leaves and stems, white mold on underside',
        'treatment': 'Spray with chlorothalonil or mancozeb, remove infected plants',
        'prevention': 'Plant resistant varieties, avoid wet conditions'
    },
    'Leaf Spot': {
        'symptoms': 'Circular brown or black spots with yellow halos on leaves',
        'treatment': 'Remove affected leaves, spray with fungicide',
        'prevention': 'Improve air circulation, avoid leaf wetness'
    },
    'Powdery Mildew': {
        'symptoms': 'White powder coating on leaves, stems, and flowers',
        'treatment': 'Spray with sulfur or neem oil every 7-10 days',
        'prevention': 'Ensure good air flow, avoid overcrowding'
    },
    'Rust': {
        'symptoms': 'Orange/brown pustules on leaf undersides',
        'treatment': 'Remove infected leaves, spray with fungicide',
        'prevention': 'Plant resistant varieties, maintain good drainage'
    },
    'Blight': {
        'symptoms': 'Rapid wilting and darkening of leaves and stems',
        'treatment': 'Remove entire plant, disinfect tools, improve drainage',
        'prevention': 'Plant in well-draining soil, avoid overcrowding'
    },
    'Mosaic Virus': {
        'symptoms': 'Mottled, discolored leaves, stunted growth',
        'treatment': 'Remove infected plant (no cure), control aphids',
        'prevention': 'Use disease-resistant varieties, control insect vectors'
    },
    'Healthy': {
        'symptoms': 'No visible disease symptoms',
        'treatment': 'Continue regular maintenance and monitoring',
        'prevention': 'Maintain good crop hygiene and spacing'
    }
}


def get_pest_info(disease_name):
    """Get pest information from database"""
    for pest, info in PEST_DATABASE.items():
        if pest.lower() in disease_name.lower() or disease_name.lower() in pest.lower():
            return pest, info
    
    return disease_name, {
        'symptoms': 'Unable to identify specific symptoms',
        'treatment': 'Consult an agricultural expert for specific treatment',
        'prevention': 'Maintain good crop hygiene and spacing'
    }


def simple_pest_detection(image_path):
    """Simple color-based pest detection"""
    try:
        img = Image.open(image_path)
        img = img.resize((100, 100))
        pixels = img.load()
        
        brown_count = 0
        green_count = 0
        yellow_count = 0
        white_count = 0
        
        for i in range(100):
            for j in range(100):
                r, g, b = pixels[i, j][:3]
                
                if 100 < r < 200 and 50 < g < 150 and b < 100:
                    brown_count += 1
                elif g > r and g > b:
                    green_count += 1
                elif r > 150 and g > 150 and b < 100:
                    yellow_count += 1
                elif r > 200 and g > 200 and b > 200:
                    white_count += 1
        
        total = 10000
        brown_ratio = brown_count / total
        green_ratio = green_count / total
        yellow_ratio = yellow_count / total
        white_ratio = white_count / total
        
        if white_ratio > 0.3:
            return 'Powdery Mildew', 75
        elif brown_ratio > 0.3 and green_ratio < 0.5:
            return 'Leaf Spot', 70
        elif yellow_ratio > 0.2:
            return 'Rust', 65
        elif brown_ratio > 0.2:
            return 'Blight', 60
        else:
            return 'Healthy', 85
    
    except:
        return 'Unable to analyze', 0


@login_required(login_url='login')
def pest_diagnosis(request):
    """AI Pest diagnosis view"""
    if request.method == 'POST':
        if 'image' not in request.FILES:
            messages.error(request, 'Please upload an image')
            return redirect('pest_diagnosis')
        
        image_file = request.FILES['image']
        
        if image_file.size > 5 * 1024 * 1024:
            messages.error(request, 'Image size must be less than 5MB')
            return redirect('pest_diagnosis')
        
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                for chunk in image_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            
            disease_name, confidence = simple_pest_detection(tmp_path)
            pest_name, pest_info = get_pest_info(disease_name)
            
            try:
                os.remove(tmp_path)
            except:
                pass
            
            context = {
                'pest_name': pest_name,
                'confidence': int(confidence * 100) if confidence else 0,
                'symptoms': pest_info.get('symptoms', ''),
                'treatment': pest_info.get('treatment', ''),
                'prevention': pest_info.get('prevention', ''),
                'diagnosis_done': True
            }
            
            return render(request, 'pests/pest_diagnosis.html', context)
        
        except Exception as e:
            messages.error(request, f'Error analyzing image: {str(e)}')
            return redirect('pest_diagnosis')
    
    return render(request, 'pests/pest_diagnosis.html', {'diagnosis_done': False})