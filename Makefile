dev:
	 uvicorn app.main:app --reload

local:
	uvicorn app.main:app --host 192.168.1.3 --port 8000 --reload