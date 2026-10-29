# Best Cars Dealership Application

Simple Django, SQLite, and React dealership directory. Django manages accounts and proxies dealer/review requests to an Express service.

Requirements: Python 3.10+ and Node.js 18+.

From the project root, create and activate a virtual environment, then run:
  pip install -r server/requirements.txt
  python server/manage.py migrate
  python server/manage.py runserver

In another terminal:
  cd server/frontend
  npm install
  npm run dev

Open http://localhost:5173. Create admin user with python server/manage.py createsuperuser.

Copy .env.example to .env. Configure DJANGO_SECRET_KEY, DEALER_API_URL, and SENTIMENT_API_URL. Run the existing Express/MongoDB service separately. Expected dealer routes are dealers, dealers/{state}, dealer/{id}, reviews/{id}; adjust proxy paths in server/cars/views.py to match your service. Sentiment request forwards review text in the text query parameter. Car makes and models are maintained in Django admin and start empty. Missing services return error responses.
