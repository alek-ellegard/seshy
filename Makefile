
install:
	uv tool install .
	@echo 'installed!'

install-edit:
	uv tool install -e .
	@echo 'installed!'
