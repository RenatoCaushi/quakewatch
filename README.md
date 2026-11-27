# QuakeWatch

**Live demo:** https://earthquakewatch.onrender.com

Dashboard tërmetesh në kohë reale me Django. Të dhënat vijnë nga API-ja publike e USGS.

## Funksionet
- Marrje automatike e tërmeteve nga USGS (`fetch_earthquakes`)
- Filtra sipas magnitudës, periudhës dhe vendit
- Hartë interaktive (Leaflet) me pika sipas magnitudës
- Grafik me tërmetet për ditë (Chart.js)
- Panel administrimi në Django Admin

## Teknologjitë
Python, Django, SQLite/PostgreSQL, Leaflet, Chart.js, USGS GeoJSON API

## Instalimi
```bash
git clone https://github.com/RenatoCaushi/quakewatch.git
cd quakewatch
python -m venv myEnv
myEnv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py fetch_earthquakes
python manage.py runserver
```
Hape http://127.0.0.1:8000/

## Përditësimi i të dhënave
`python manage.py fetch_earthquakes --feed 2.5_week`

## Burimi i të dhënave
USGS Earthquake Hazards Program
