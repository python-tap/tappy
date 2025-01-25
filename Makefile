test:
	uv run pytest

clean:
	@rm -rf \
		.coverage \
		coverage.xml \
		dist \
		htmlcov \
		results \
		testout

