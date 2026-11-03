# notas-lab

App Flask pequeña para practicas de auditoria con Snyk.
**SOLO PARA LABORATORIO. NO DESPLEGAR NI EXPONER A INTERNET.**

## PowerShell (Python 3.12)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python init_db.py
python -m pytest
python app.py
```
La app escucha solo en http://127.0.0.1:5000
