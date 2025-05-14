dev:
	 uvicorn app.main:app --reload

local:
	uvicorn app.main:app --host 192.168.1.4 --port 8000 --reload