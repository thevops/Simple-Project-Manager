# Simple-Project-Manager


## How to use it?
- create virtual environment for Python3: virtualenv -p python3 venv
- download this project: git clone https://github.com/vizarch/Simple-Project-Manager.git
- install requirements: Requirements.txt is for help, don't install from it !!
  - source venv/bin/active
  - pip install Django==1.10.3
  - pip install django-bootstrap-form
  - pip install django-directmessages
  - pip install chartkick
  - pip install daphne==0.15.0 (!!! important, 1.0.2 don't work - I don't know why)
  - pip install channels==0.17.3 (!!! important, 1.0.2 don't work - I don't know why)
  - rest of requirements will be installed automatically with others
- python manager.py runserver

