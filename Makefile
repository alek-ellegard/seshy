help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# =============================================================================
# Setup
# =============================================================================

install: ## Install 
	uv tool install .
	@echo 'installed!'

install-edit: ## Install dev 
	uv tool install -e .
	@echo 'installed!'
