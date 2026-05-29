run-api:
	uvicorn api.main:app --reload

test-contract:
	python scripts/contract_test_api.py

docker-build:
	docker build -t kurgin-formula-api .

docker-run:
	docker run --rm -p 8000:8000 --env-file .env.staging.example kurgin-formula-api

staging-env-check:
	python scripts/validate_staging_env.py

staging-build:
	docker compose -f docker-compose.staging.yml --env-file .env.staging build

staging-up:
	docker compose -f docker-compose.staging.yml --env-file .env.staging up -d

staging-down:
	docker compose -f docker-compose.staging.yml --env-file .env.staging down

staging-smoke:
	python scripts/staging_smoke_test.py --base-url http://127.0.0.1:8000 --api-key $(KURGIN_API_SECRET)
