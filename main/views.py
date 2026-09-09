from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Zayyan",
        "npm": "2506550955",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            """Passionate learners, aiming to become a polymath. Very interested in tinkering electronical devices and bootlegs. I spent my days experimenting with new things and creating something to be use for.
            
            Sometimes I play guitars, capturing moments, staring into the abysmal void of the universe, and most of the time reflecting on the meaning of life itself. The other time? probably chilling out, walking around the city."""
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Zayyan",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)