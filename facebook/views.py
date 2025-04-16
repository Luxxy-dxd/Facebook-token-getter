from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests, json

@csrf_exempt
def login_view(request):
    result = None
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            session = requests.Session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10)',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            payload = {
                'email': email,
                'password': password,
                'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                'format': 'JSON',
                'sdk_version': '2',
                'generate_session_cookies': '1',
                'locale': 'en_US',
                'sig': '3f555f99fb61fcd7aa0c44f58f522ef6'
            }

            try:
                response = session.post("https://b-api.facebook.com/method/auth.login", headers=headers, data=payload)
                data = response.json()

                if 'access_token' in data:
                    token = data['access_token']
                    cookies = data.get('session_cookies', [])
                    cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])

                    c_user = next((c['value'] for c in cookies if c['name'] == 'c_user'), None)
                    datr = next((c['value'] for c in cookies if c['name'] == 'datr'), None)

                    appstate = [
                        {
                            "key": c['name'],
                            "value": c['value'],
                            "domain": ".facebook.com",
                            "path": "/",
                            "secure": False,
                            "httpOnly": False
                        } for c in cookies
                    ]

                    result = {
                        'token': token,
                        'cookie': cookie_str,
                        'c_user': c_user,
                        'datr': datr,
                        'appstate': json.dumps(appstate, indent=4)
                    }
                else:
                    error = data.get('error_msg', 'Login failed. Unknown error.')

            except Exception as e:
                error = str(e)
        else:
            error = "Email and password are required."

    return render(request, 'facebook/login_result.html', {'result': result, 'error': error})
