virtualenv env &&\
cd env/bin &&\
source activate &&\
cd ../.. &&\
pip install -r ./requirements.txt &&\
cd src &&\
python manage.py makemigrations &&\
python manage.py migrate &&\
python manage.py test