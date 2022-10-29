# food-delivery
Clone the repo
https://github.com/Arlend42/food-delivery.git

Enter repo and create virtual environment

cd food-delivery
python -m venv --prompt=food venv
. venv\bin\Activate
pip install -r requirements.txt

Run migrations

python manage.py migrate food-delivery
Run local development server

python manage.py runserver
Visit the following url on your browser: http://localhost:8000/
