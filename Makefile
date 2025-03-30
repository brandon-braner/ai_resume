
.PHONY: gen_resume gen_longform_resume airtable_sync, upwork_proposal

gen_resume:
	@if [ -z "$(company)" ]; then \
		echo "Error: company argument is required. Usage: make gen_resume company=COMPANY [resume=RESUME_FILE]"; \
		exit 1; \
	fi
	@uv run main.py --company "$(company)" --resume "$(if $(resume),$(resume),resume.pdf)"


gen_longform_resume:
	@if [ -z "$(company)" ]; then \
		echo "Error: company argument is required. Usage: make gen_resume company=COMPANY [resume=RESUME_FILE]"; \
		exit 1; \
	fi
	@uv run longform.py --company "$(company)" --resume "$(if $(resume),$(resume),resume.md)"


upwork_proposal:
	@if [ -z "$(company)" ]; then \
		echo "Error: company argument is required. Usage: make gen_resume company=COMPANY [resume=RESUME_FILE]"; \
		exit 1; \
	fi
	@uv run upwork_coverletter.py --company "$(company)" --resume "$(if $(resume),$(resume),resume.md)"

airtable_sync:
	@uv run airtable_sync.py
