# Lensy App – Quick Start Guide

 ---

## 1. Clone the Repository

```bash
git clone https://github.com/martrzeciak/lensy-app.git
cd lensy-app
```

---

## 2. Install virtual environment and create it

```powershell
pip install virtualenv
python -m venv env
```

---

## 3. Activate virtual environment

### Option A: Windows

```powershell
env\Scripts\activate
```

### Option B: Linux/macOS

```powershell
source env/bin/activate
```

---

## 4. Install dependencies from requirements.txt

```powershell
cd lensy_backend
pip install -r requirements.txt
```

---

## 5. Database migrations

```powershell
python manage.py migrate
```

---

## 6. Run the Application

```powershell
python manage.py runserver
```

