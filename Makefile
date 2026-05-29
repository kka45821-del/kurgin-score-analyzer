run-api:
	uvicorn api.main:app --reload

test-contract:
	python scripts/contract_test_api.py

docker-build:
	docker build -t kurgin-formula-api .

docker-run:
	docker run --rm -p 8000:8000 --env-file .env.staging.example kurgin-formula-api
