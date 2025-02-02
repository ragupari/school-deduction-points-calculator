# SCHOOL DEDUCTION POINT CALCULATOR 

## Demo 
Can watch the demo on [Youtube](https://youtu.be/TK8zg94yjFQ?si=hduZNPY8J0XZhX3x)
<img src="/Images/image1.png" alt="Alt text" width="500" height="300">
<img src="/Images/image2.png" alt="Alt text" width="500" height="300">
<img src="/Images/image3.png" alt="Alt text" width="500" height="300">

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/ragupari/school-deduction-points-calculator.git
$ cd school-deduction-points-calculator
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Setup your `GOOGLE_MAPS_API` in `project/map_project/settings.py` 

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/map/`.
