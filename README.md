# (installing virtualenv)
virtualenv env
. vb
pip install -r packages.txt
cd server
python manage.py runserver 0.0.0.0:8001
