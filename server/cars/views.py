import json,requests
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET,require_POST
from django.middleware.csrf import get_token
from .models import CarMake
def home(request): return HttpResponse("<h1>Best Cars Dealership</h1>")
@ensure_csrf_cookie
def csrf(request): return JsonResponse({"csrfToken":get_token(request)})
@require_POST
def register(request):
 try: d=json.loads(request.body)
 except (ValueError,UnicodeDecodeError): return JsonResponse({"error":"Invalid JSON"},status=400)
 keys=("username","first_name","last_name","email","password")
 if any(not str(d.get(k,"")).strip() for k in keys): return JsonResponse({"error":"All fields are required"},status=400)
 if User.objects.filter(username=d["username"]).exists(): return JsonResponse({"error":"Username already exists"},status=409)
 u=User.objects.create_user(username=d["username"].strip(),first_name=d["first_name"].strip(),last_name=d["last_name"].strip(),email=d["email"].strip(),password=d["password"])
 login(request,u)
 return JsonResponse({"username":u.username,"message":"Registration successful"},status=201)
@require_POST
def login_view(request):
 try: d=json.loads(request.body)
 except (ValueError,UnicodeDecodeError): return JsonResponse({"error":"Invalid JSON"},status=400)
 u=authenticate(request,username=d.get("username",""),password=d.get("password",""))
 if not u: return JsonResponse({"error":"Invalid username or password"},status=401)
 login(request,u); return JsonResponse({"username":u.username})
@require_POST
def logout_view(request): logout(request); return JsonResponse({"message":"Logged out"})
def session_view(request): return JsonResponse({"authenticated":request.user.is_authenticated,"username":request.user.username if request.user.is_authenticated else None})
def cars(request): return JsonResponse([{"id":m.id,"name":m.name,"models":[{"id":x.id,"name":x.name,"year":x.year} for x in m.models.all()]} for m in CarMake.objects.prefetch_related("models")],safe=False)
def proxy(path,params=None):
 try:
  r=requests.get(settings.DEALER_API_URL.rstrip("/")+"/"+path.lstrip("/"),params=params,timeout=5); r.raise_for_status(); data=r.json()
  return JsonResponse(data,safe=not isinstance(data,list))
 except requests.RequestException: return JsonResponse({"error":"Dealer service unavailable; check DEALER_API_URL"},status=503)
 except ValueError: return JsonResponse({"error":"Dealer service returned invalid JSON"},status=502)
def dealers(request):
 state=request.GET.get("state")
 return proxy("dealers"+("/"+state if state else ""),request.GET)
def dealer_detail(request,dealer_id): return proxy("dealer/"+dealer_id)
def reviews(request,dealer_id): return proxy("reviews/"+dealer_id)
@require_POST
def submit_review(request,dealer_id):
 if not request.user.is_authenticated: return JsonResponse({"error":"Log in to review"},status=401)
 try:
  d=json.loads(request.body); r=requests.post(settings.DEALER_API_URL.rstrip("/")+"/reviews/"+dealer_id,json={**d,"username":request.user.username},timeout=5); r.raise_for_status(); return JsonResponse(r.json())
 except (requests.RequestException,ValueError): return JsonResponse({"error":"Review service unavailable"},status=503)
def analyze(request,text=None):
 text=text or request.GET.get("text","")
 if not text:return JsonResponse({"error":"Supply text query parameter"},status=400)
 if not settings.SENTIMENT_API_URL:return JsonResponse({"error":"SENTIMENT_API_URL is not configured"},status=503)
 try:
  r=requests.get(settings.SENTIMENT_API_URL,params={"text":text},timeout=8);r.raise_for_status();d=r.json();return JsonResponse(d,safe=not isinstance(d,list))
 except requests.RequestException:return JsonResponse({"error":"Sentiment service unavailable"},status=503)
 except ValueError:return JsonResponse({"error":"Sentiment service returned invalid JSON"},status=502)

