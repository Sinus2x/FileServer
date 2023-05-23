minio:
	@docker compose up
venv:
	python3 -m venv env
	sh ./env/bin/activate
	pip install -r requirements.txt
server:
	python3 server.py

code:
	@python -m grpc_tools.protoc --python_out=. --pyi_out=. --grpc_python_out=. -I./ file_service.proto