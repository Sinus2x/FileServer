run:
	@docker compose up
code:
	@python -m grpc_tools.protoc --python_out=. --pyi_out=. --grpc_python_out=. -I./ file_service.proto
