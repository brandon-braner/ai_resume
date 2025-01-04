
.PHONY: gen_resume

gen_resume:
	@if [ -z "$(company)" ]; then \
		echo "Error: company argument is required. Usage: make gen_resume company=COMPANY [resume=RESUME_FILE]"; \
		exit 1; \
	fi
	@uv run main.py --company "$(company)" --resume "$(if $(resume),$(resume),resume.pdf)"
