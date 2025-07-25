from django.utils import timezone

COUNTRY_TIMEZONES = {
    "Albania": "Europe/Tirane",
    "Andorra": "Europe/Andorra",
    "Armenia": "Asia/Yerevan",
    "Austria": "Europe/Vienna",
    "Azerbaijan": "Asia/Baku",
    "Belarus": "Europe/Minsk",
    "Belgium": "Europe/Brussels",
    "Bosnia and Herzegovina": "Europe/Sarajevo",
    "Bulgaria": "Europe/Sofia",
    "Croatia": "Europe/Zagreb",
    "Cyprus": "Asia/Nicosia",
    "Czech Republic": "Europe/Prague",
    "Denmark": "Europe/Copenhagen",
    "Estonia": "Europe/Tallinn",
    "Finland": "Europe/Helsinki",
    "Macedonia": "Europe/Skopje",
    "France": "Europe/Paris",
    "Georgia": "Asia/Tbilisi",
    "Germany": "Europe/Berlin",
    "Greece": "Europe/Athens",
    "Hungary": "Europe/Budapest",
    "Iceland": "Atlantic/Reykjavik",
    "Ireland": "Europe/Dublin",
    "Italy": "Europe/Rome",
    "Kosovo": "Europe/Belgrade",
    "Latvia": "Europe/Riga",
    "Liechtenstein": "Europe/Vaduz",
    "Lithuania": "Europe/Vilnius",
    "Luxembourg": "Europe/Luxembourg",
    "Malta": "Europe/Malta",
    "Moldova": "Europe/Chisinau",
    "Monaco": "Europe/Monaco",
    "Montenegro": "Europe/Podgorica",
    "Netherlands": "Europe/Amsterdam",
    "Norway": "Europe/Oslo",
    "Poland": "Europe/Warsaw",
    "Portugal": "Europe/Lisbon",
    "Romania": "Europe/Bucharest",
    "Russia": "Europe/Moscow",
    "San Marino": "Europe/San_Marino",
    "Serbia": "Europe/Belgrade",
    "Slovakia": "Europe/Bratislava",
    "Slovenia": "Europe/Ljubljana",
    "Spain": "Europe/Madrid",
    "Sweden": "Europe/Stockholm",
    "Switzerland": "Europe/Zurich",
    "Turkey": "Europe/Istanbul",
    "Ukraine": "Europe/Kyiv",
    "United Kingdom": "Europe/London"
}


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            user_profile = user.user_profile  # every user has an associated user_profile
            # user_country can be a valid country or an empty string (user doesn't have a selected country)
            user_country = user_profile.country

            if user_country != "":
                tzname = COUNTRY_TIMEZONES.get(user_country)
            else:
                tzname = 'UTC'  # default timezone for users that doesn't have a selected country

            timezone.activate(tzname)
            request.session['django_timezone'] = tzname

        else:
            timezone.deactivate()

        return self.get_response(request)
