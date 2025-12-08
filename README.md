# Digi-Farm

## Project Overview

### What is Digi-Farm?

Digi-Farm is a website where farmers can go to get helpful information and advice about farming. Instead of farmers having to guess or rely only on what they learned from their parents, they can use Digi-Farm to make smarter decisions about their crops.

### The Problem It Solves

Many small-scale farmers in Kenya face challenges like:

Not knowing when to plant - Should I plant now or wait for rain?
Dealing with pests - What is eating my crops and how do I stop it?
Getting the timing right - When should I harvest to get the best yield?
Learning from experience alone - They have no way to learn what other farmers are doing

__Digi-Farm__ fixes these problems by giving farmers access to:

* Real-time weather information
* Guidance on when to plant, weed, and harvest
* Information about common pests and how to treat them
* Tips and advice from other farmers in their community

### How Digi-Farm Works

1. **Farmers Create an Account**

    A farmer goes to Digi-Farm and signs up
    They enter their location, phone number, and which crops they grow
    They can now access everything the platform offers

2. **They Check the Weather**

    The farmer checks the weather forecast for their area
    They see temperature, rainfall predictions, and humidity
    This helps them decide: "Should I water today? Is rain coming?"

3. **They Follow the Crop Calendar**

    The farmer can see what activities they should do this month
    For example: "March is planting season for maize - plant now!"
    The app shows exactly what to do and when to do it

4. **They Learn About Pests**

    If a farmer sees an unknown insect on their crop, they can search for it
    Digi-Farm shows them what the pest is called
    It explains the symptoms to look for
    It tells them how to prevent the pest from spreading
    It suggests treatments (chemicals or natural methods)

5. **They Share Tips With Other Farmers**

    Farmers can post tips they've learned like "Intercropping beans with maize saves water"

    Other farmers can read these tips

    Farmers can like tips they find helpful

    This creates a community of learning

#### Installation & Setup

##### Prerequisites

* Python 3.12+
* pip
* Virtual environment
* Git
* Django

##### Setup Steps

```
1. Clone repository
    - git clone <repository-url>
    - cd agri_platform

2. Create virtual environment
    - python -m venv env
    - source/.env/Scripts/activate

3. Install dependencies
    - pip install -r requirements.txt

4. Create .env file with credentials
    DJANGO_SECRET_KEY=your-secret-key
    DEBUG=True
    WEATHER_API_KEY=your-openweathermap-key
    MPESA_CONSUMER_KEY=your-mpesa-key
    MPESA_CONSUMER_SECRET=your-mpesa-secret
    MPESA_SHORTCODE=174379
    MPESA_PASSKEY=your-mpesa-passkey
    MPESA_ENVIRONMENT=sandbox

5. Run migrations
    - python manage.py makemigrations
    - python manage.py migrate

6. Create superuser
    - python manage.py createsuperuser

7. Run server
    - python manage.py runserver

8. Access application
    - Homepage: http://localhost:8000
    - Admin: http://localhost:8000/admin
```

## Project Modules/Apps

### Core App (agriapp)

#### Description

The core authentication and user management module that handles user registration, login, weather integration, and user profiles.

#### How It Works

* Users register with their location and phone number
* Real-time weather data is fetched based on user location
* Farming tips are dynamically generated based on weather conditions
* User dashboard displays personalized information

#### Steps to Create

```
1. Create the app
python manage.py startapp agriapp

2. Create models for user profile

- User (from Django)
- FarmerProfile (custom model with location, phone, etc.)

3. Create forms for registration and login

4. Set up weather API integration

- Sign up at OpenWeatherMap API
- Add API key to settings.py

5. Create views for:

- home() - displays weather and farming tips
- login() - user authentication
- register() - user registration
- logout() - user logout

6. Create templates:

- home.html
- login.html
- register.html
- dashboard.html

7. Configure URLs in agriapp/urls.py

8. Add app to INSTALLED_APPS in settings.py

9. Run migrations

- python manage.py makemigrations
- python manage.py migrate

10. Start server
- python manage.py runserver
```

#### Key Features

* User authentication and authorization
* Real-time weather data (OpenWeatherMap API)
* Intelligent farming tips based on weather
* User profile management
* Location-based services


#### Future Improvements

 * Multi-language support (Swahili, Kikuyu, etc.)
 * SMS notifications for weather alerts
 * Social authentication (Google, Facebook login)
 * User preferences/settings customization
 * Mobile app integration with REST API

### Planner App (calendar)

#### Description

A comprehensive calendar and farming planning module that helps farmers plan their activities based on seasons, weather, and crop cycles.

#### How It Works

    Farmers create a calendar with planned activities
    System suggests optimal planting/harvesting dates
    Weather data informs recommendations
    Activity reminders can be set

#### Steps to Create

```

1. Create the app
python manage.py startapp planner

2. Create models:
 - FarmingCalendar
 - PlannedActivity
 - Season

3. Create forms for:
 - Adding planned activities
 - Editing calendar events

4. Create views for:
 - calendar_view() - display calendar
 - add_activity() - add new activity
 - edit_activity() - modify activity
 - view_activity() - see details

5. Create templates:
 - calendar.html
 - activity_form.html
 - activity_detail.html

6. Integrate with weather data
 - Use weather API to suggest dates

7. Configure URLs in planner/urls.py

8. Add to INSTALLED_APPS

9. Run migrations
    python manage.py makemigrations planner
    python manage.py migrate

10. run Server
    - python manage.py runserver
```

#### Key Features

* Interactive farming calendar
* Activity scheduling and reminders
* Weather-based recommendations
* Seasonal planning
* Activity history and tracking

#### Future Improvements

 * Google Calendar integration
 * Push notifications for scheduled activities
 * AI-powered scheduling recommendations
 * Weather forecasting integration (7-14 day predictions)
 * Crop yield prediction based on activities
 * Export calendar to PDF/CSV


### Tips & Articles App (tips)

#### Description

An educational content module that provides farming tips, best practices, and agricultural articles.

#### How It Works

    Admin creates farming tips and articles
    Tips are categorized by crop/season/topic
    Users can read and bookmark tips
    Recommendations shown based on user location/crops

#### Steps to Create

```
1. Create the app
python manage.py startapp tips

2. Create models:
 - Tip
 - Category
 - Tag

3. Create admin interface for tips management

4. Create views for:
 - list_tips() - show all tips
 - tip_detail() - show single tip
 - tips_by_category() - filter tips

5. Create templates:
 - tips_list.html
 - tip_detail.html
 - tips_by_category.html

6. Add search functionality

7. Configure URLs in tips/urls.py

8. Add to INSTALLED_APPS

9. Run migrations
 - python manage.py makemigrations tips
 - python manage.py migrate

10. Run Servver
 - python manage.py runserver
```

#### Key Features

* Categorized farming tips
* Search functionality
* Tip ratings and reviews
* Admin content management
* Multiple content formats

#### Future Improvements
   * Video tutorials and embedded content
   * User comments and discussion
   * Tip sharing on social media
   * Personalized tip recommendations (ML)
   * Expert-authored articles with credentials
   * Subscribe to tips by category/crop
   * Print/PDF export for offline reading


### 4. Pest Management App (pests)

#### Description
    A specialized module for identifying, tracking, and managing crop pests and diseases with **AI-powered image recognition** capabilities.

#### How It Works

    - Farmers report pest/disease problems by uploading photos
    - AI system analyzes images to automatically identify pests
    - System provides identification results with confidence scores
    - Treatment recommendations are generated based on identified pest
    - Local treatment solutions and availability information
    - Complete pest tracking and impact monitoring system

#### Steps to Create

```
1. Create the App
 - python manage.py startapp pests

2.  Install Dependencies
 - pip install tensorflow pillow opencv-python

3.  Create Models
    - Create these models in `pests/models.py`:
    - **Pest** - Database of pests with descriptions
    - **Disease** - Crop disease information
    - **Crop** - Crop types and varieties
    - **PestReport** - User pest reports with images
    - **Treatment** - Treatment options and recommendations

4. Set Up AI Pest Identification
    - Train or use pre-trained **TensorFlow model**
    - Create `pest_identifier.py` service file
    - Integrate image processing pipeline
    - Set up confidence scoring system

5. Create Forms
    - Create forms for:
        - Reporting pest sightings with **image upload**
        - Tracking pest treatments applied

6. Create Views
 - Create views in `pests/views.py`:

7. Create Templates
 - Create these HTML templates in `pests/templates/`:

8. Create Pest Image Database
 - Build database of pest/disease images for training
 - Organize images by pest type
 - Ensure good quality and variety

9. Create Pest Identification Service
In `pests/pest_identifier.py`:
    - Integrate **TensorFlow/ML model**
    - Build image preprocessing pipeline
    - Implement confidence scoring
    - Handle multiple pest predictions

10. Configure URLs
In `pests/urls.py`, add:
    - Route for `identify_pest` endpoint
    - All other pest-related URLs

11. Add to INSTALLED_APPS
 - Add `'pests'` to `INSTALLED_APPS` in `settings.py`

12. Run Migrations
 - python manage.py makemigrations pests
 - python manage.py migrate

13. Run Server
 - python manage.py runserver
```

### Key Features

Comprehensive pest and disease database  
    **Confidence Scoring** : Shows reliability of AI predictions 
    **Treatment Recommendations** : Personalized solutions for identified pests 
    **Pest Report Tracking** : Complete history of farmer pest reports 
    **Local Solutions** : Shows local availability of treatments 

### How AI Pest Identification Works

1. **Photo Upload** - Farmer uploads pest/disease photo
2. **Image Processing** - System preprocesses image for analysis
3. **AI Analysis** - TensorFlow model analyzes the image
4. **Pest Detection** - Returns identified pest(s) with confidence score
5. **Solution Generation** - Recommends treatments for identified pest
6. **User Feedback** - Farmer can confirm/correct identification to improve model
7. **Learning** - System improves with each confirmed identification

### Consultations & Q&A App (consultations)

#### Description

A comprehensive platform for expert consultations and community Q&A with M-Pesa payment integration.

#### How It Works

    Farmers ask questions in Q&A forum
    Experts provide answers
    Farmers can book paid consultations (3 types)
    M-Pesa STK Push handles payments
    Consultations can be online, office, or farm visits

#### Steps to Create

```
1. Create the app
 - python manage.py startapp consultations

2. Install dependencies
 - pip install django_daraja requests python-decouple

3. Create models:
 - Question
 - Expert
 - Consultation
 - ConsultationBooking
 - PaymentTransaction

4. Set up M-Pesa configuration
 - Sign up at https://developer.safaricom.co.ke
 - Get Consumer Key, Consumer Secret, Passkey, Shortcode
 - Add credentials to .env file:
    MPESA_CONSUMER_KEY=your_key
    MPESA_CONSUMER_SECRET=your_secret
    MPESA_SHORTCODE=174379
    MPESA_PASSKEY=your_passkey
    MPESA_ENVIRONMENT=sandbox

5. Create forms:
 - QuestionForm
 - AnswerForm
 - ConsultationForm

6. Create M-Pesa service class
 - MpesaDarajaService with django_daraja

7. Create views for:
 - qa_forum() - main Q&A page
 - ask_question() - post question
 - question_detail() - view Q&A
 - book_consultation() - booking form
 - initiate_payment() - start M-Pesa payment
 - mpesa_callback() - handle payment confirmation
 - my_consultations() - user's bookings

8. Create templates:
 - qa_forum.html
 - ask_question.html
 - question_detail.html
 - book_consultation.html
 - initiate_payment.html
 - payment_waiting.html
 - my_consultations.html

9. Configure URLs with callback endpoint
 - Add: path('mpesa-callback/', views.mpesa_callback)

10. Add to INSTALLED_APPS:
 - consultations
 - django_daraja

11. Add LOGGING configuration for payment tracking

12. Run migrations
- python manage.py makemigrations consultations
- python manage.py migrate

13. Runserver
- python manage.py runserver
```

#### Key Features

* Community Q&A forum
* Expert answer system
* 3 consultation types (Online, Office, Farm Visit)
* Dynamic pricing based on type
* M-Pesa STK Push payment integration
* Payment status tracking
* Consultation booking and scheduling
* User consultation history

#### M-Pesa Integration Details

- Online Consultation: KES 500 (30 minutes)
- Office Visit: KES 1,500 (1 hour)
- Farm Visit: KES 4,000 (on-site assessment)
- Payment via M-Pesa STK Push (USSD prompt)
- Callback verification for payment confirmation

#### Future Improvements

- Video call integration (Jitsi/Zoom)
- Real-time chat with experts
- Email notifications for Q&A activity
- Expert rating and review system
- Consultation recording and notes
- Appointment calendar for experts
- Refund policy and dispute resolution
- Multiple payment methods (card, bank transfer)
- Referral rewards program
- Expert verification and credentials display


### Technology Stack

#### Backend

- **Framework**: Django 5.2.9
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **Payment**: M-Pesa Daraja API (django_daraja)
- **Weather API**: OpenWeatherMap
- **Authentication**: Django built-in


#### Frontend

- **Template Engine**: Django Templates
- **CSS Framework**: Bootstrap 5
- **Icons**: Google Material Icons
- **JavaScript**: Vanilla JS (for AJAX)

#### AI/ML
- TensorFlow
- OpenCV
- Pillow: Image Processing

#### External APIs

- OpenWeatherMap (weather data)
- Safaricom M-Pesa Daraja (payments)

#### Contributing

To add new features or improvements:

 1. Create a new branch
 2. Make your changes
 3. Test thoroughly
 4. Submit a pull request

#### Support

For issues, questions, or suggestions, please contact the development team(sarahjoshua010@gmail.com) or open an issue on the repository.
