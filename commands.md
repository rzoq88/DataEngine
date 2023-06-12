Run server
```
python3 -m venv venv

source venv/vevn/activate

pip3 install -r requirements.txt


uvicorn app.main:app --reload
```