.PHONY: help
help:
	@echo "The following commands are meant to be run inside the python container:"
	@echo
	@echo "  make test - Run lint"
	@echo "  make lint - Check syntax and style"
	@echo "  make build - Build the package"
	@echo

GITHUB_ACTIONS ?= false

# Helper function to define a GitHub Actions group
define group
	@if [ "$(GITHUB_ACTIONS)" = "true" ]; then \
		echo "::group::$1"; \
	fi
endef


.PHONY: test
test: lint checkmanifest checksetup

.PHONY: lint
lint:
	# Check syntax and style
	$(call group,Checking syntax and style)
	ruff check
	ruff format --check --diff
	$(call endgroup)

.PHONY: lintfix
lintfix:
	# Automatically fix syntax and style issues
	ruff check --fix-only
	ruff format

.PHONY: clean
clean:
	# Clean up build files
	$(call group,Cleaning up)
	rm -rf dist/*.whl dist/*.tar.gz
	$(call endgroup)

.PHONY: checkmanifest
checkmanifest:
	# Check if all files are included in the sdist
	$(call group,Checking manifest)
	check-manifest
	$(call endgroup)

.PHONY: checksetup
checksetup: build
	# Check metadata
	$(call group,Checking package metadata)
	twine check ./dist/*.whl
	$(call endgroup)

.PHONY: build
build: clean
	# Build the package
	$(call group,Building package)
	python -m build --installer uv
	$(call endgroup)

.PHONY: install-pipeline
install-pipeline:
	# Install the package
	$(call group,Installing package)
	uv pip install -r requirements_dev.txt
	$(call endgroup)
