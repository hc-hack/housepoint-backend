# Housepoint Backend

## Installation & Running as Dev

Python 3.6 and above should be fine - I'm using Python 3.7.2.

### Create your virtual environment

**Make sure you're in the git repo folder!**

```bash
python --version
# Should output Python 3.7.2 or something similar.

python -m virtualenv venv
# This should create a virtual environment in the folder "venv"
```

### Activate the virtual environment

```bash
# Windows
.\venv\Scripts\activate

# Linux
source venv/bin/activate
```

### Install local dependencies

```bash
pip install -r requirements.txt
```

### Run the app!

```bash
python application.py
```

Check that the app is running by navigating to [http://localhost:5000](http://localhost:5000).
