.PHONY: stubs

stubs:
	make clean
	poetry run python uaproject_backend_schemas/utils/generate_pyi.py

clean:
	rm -f uaproject_backend_schemas/models/*.pyi
