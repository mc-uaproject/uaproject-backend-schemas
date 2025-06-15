.PHONY: stubs

stubs:
	@echo "🔄 Generating stub files..."
	@start_time=$$(date +%s.%N); \
	make clean; \
	poetry run python uaproject_backend_schemas/utils/generate_pyi.py; \
	end_time=$$(date +%s.%N); \
	duration=$$(echo "$$end_time - $$start_time" | bc -l); \
	printf "✅ Stub files generated successfully in %.3f seconds!\n" $$duration

clean:
	rm -f uaproject_backend_schemas/models/*.pyi
