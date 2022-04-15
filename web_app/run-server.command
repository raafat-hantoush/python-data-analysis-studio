#! /bin/bash
cd "$(dirname "$0")"
python manage.py runserver
open http://localhost:8000/mlstudio