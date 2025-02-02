from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.conf import settings
from map.models import School
from django.views.decorators.csrf import csrf_exempt
import json
from geopy.distance import geodesic
from django.urls import reverse

def map(request):
    # Retrieve schools dynamically from the database
    schoolslist = list(School.objects.all().values())

    if not schoolslist:
        return HttpResponse("No schools available", status=404)

    schoolslisttobepassed = schoolslist[14:15]+schoolslist[4:5]+ schoolslist[0:4]+schoolslist[5:14]+schoolslist[15:]
    lat = schoolslisttobepassed[0].get('lat')
    lng = schoolslisttobepassed[0].get('lng')

    template = loader.get_template('index.html')
    context = {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        "lat": lat,
        "lng": lng,
        "schoollist": schoolslisttobepassed,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def navigate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extract values safely
            student_name = data.get("student_name", "").strip()
            gender = data.get("gender")
            home_lat = data.get("home_lat")
            home_lng = data.get("home_lng")
            school_lat = data.get("school_lat")
            school_lng = data.get("school_lng")

            if None in [home_lat, home_lng, school_lat, school_lng]:
                return JsonResponse({"message": "Missing location data"}, status=400)

            school_coor = (school_lat, school_lng)  # Coordinates of the school (optional if you're comparing with home)
            home_coor = (home_lat, home_lng)  # Coordinates of the home

            radius = geodesic(home_coor, school_coor).kilometers  # Calculate radius from home to school

            schoolslist = list(School.objects.all().values())  # Fetch fresh data

            nearby_schools = [
                school for school in schoolslist
                if school.get('lat') is not None and school.get('lng') is not None
                and geodesic(home_coor, (school.get('lat'), school.get('lng'))).kilometers < radius  # Distance from home
                and (gender == school.get('gender') or school.get('gender') == "Mixed")
            ]

            return JsonResponse({
                "message": "Success",
                "radius": radius,
                "nearby_schools": nearby_schools,

                    # Only return names
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

    return JsonResponse({"message": "Invalid request"}, status=400)

import json
from django.shortcuts import render
from django.conf import settings

def calculatedPoints(request):
    student_name = request.GET.get("student_name", "Unknown")
    radius = request.GET.get("radius", "N/A")
    nearby_schools = request.GET.get("nearby_schools", "[]")
    h_lat = request.GET.get("h_lat", "N/A")
    h_lng = request.GET.get("h_lng", "N/A")
    s_lat = request.GET.get("s_lat", "N/A")
    s_lng = request.GET.get("s_lng", "N/A")

    school_name = request.GET.get("school_name", "N/A")

    # Convert nearby_schools back to a Python list safely
    try:
        nearby_schools = json.loads(nearby_schools)
        if not isinstance(nearby_schools, list):
            nearby_schools = []
    except json.JSONDecodeError:
        nearby_schools = []

    # Convert radius safely to float
    try:
        radius = round(float(radius), 1)
    except ValueError:
        radius = "N/A"

    # Calculate deduction points
    deduction_points = -(len(nearby_schools) * 5)

    return render(request, 'points.html', {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        "student_name": student_name,
        "h_lat": h_lat,
        "h_lng": h_lng,
        "s_lat": s_lat,
        "s_lng": s_lng,
        "school_name": school_name,
        "radius": radius,
        "nearby_schools": nearby_schools,
        "points": deduction_points
    })

