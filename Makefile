.PHONY: docs clean

docs:
	@echo "Building Sphinx documentation..."
	@mkdir -p docs/_build
	@sphinx-build -b html docs docs/_build

clean:
	@echo "Cleaning Sphinx documentation build directory..."
	@rm -rf docs/_build
