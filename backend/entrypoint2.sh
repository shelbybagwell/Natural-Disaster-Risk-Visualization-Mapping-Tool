#!/bin/bash

python -c "
import time
import socket

while True:
    try:
        s = socket.create_connection(('db', 3306), timeout=2)
        s.close()
        break
    except (OSError, ConnectionRefusedError):
        time.sleep(1)
"

# Apply migrations and start server
python manage.py migrate
# python manage.py runserver 0.0.0.0:8000