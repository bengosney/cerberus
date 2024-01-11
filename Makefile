.PHONY: help clean test install all init dev css
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

HOOKS=$(.git/hooks/pre-commit)
REQS=$(wildcard requirements.*.txt)

CSS_FILES:=$(shell find assets -name *.css)

PYTHON_VERSION:=$(shell python --version | cut -d " " -f 2)
PIP_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/pip
WHEEL_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/wheel
PIP_SYNC_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/pip-sync
PRE_COMMIT_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/pre-commit

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml: $(PRE_COMMIT_PATH) .git
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/.pre-commit-config.yaml > $@
	pre-commit autoupdate
	@touch $@

pyproject.toml:
	curl https://gist.githubusercontent.com/bengosney/f703f25921628136f78449c32d37fcb5/raw/pyproject.toml > $@
	@touch $@

requirements.%.txt: $(PIP_SYNC_PATH) pyproject.toml
	@echo "Builing $@"
	@python -m piptools compile --generate-hashes -q --extra $* -o $@ $(filter-out $<,$^)

requirements.txt: $(PIP_SYNC_PATH) pyproject.toml
	@echo "Builing $@"
	@python -m piptools compile --generate-hashes -q $(filter-out $<,$^)

.direnv: .envrc
	@python -m ensurepip
	@python -m pip install --upgrade pip
	@touch $@ $^

.git/hooks/pre-commit: .git $(PRE_COMMIT_PATH) .pre-commit-config.yaml
	pre-commit install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python3.11" > $@
	@touch -d '+1 minute' $@
	@false

$(PIP_PATH):
	@python -m ensurepip
	@python -m pip install --upgrade pip

$(WHEEL_PATH): $(PIP_PATH)
	@python -m pip install wheel

$(PIP_SYNC_PATH): $(PIP_PATH) $(WHEEL_PATH)
	@python -m pip install pip-tools

$(PRE_COMMIT_PATH): $(PIP_PATH) $(WHEEL_PATH)
	@python -m pip install pre-commit

init: .direnv $(PIP_SYNC_PATH) requirements.dev.txt .git/hooks/pre-commit ## Initalise a enviroment
	@python -m pip install --upgrade pip

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -f .testmondata
	rm -rf *.egg-info

cerberus_crm/static/css/%.min.css: assets/css/%.css $(CSS_FILES)
	npx lightningcss --minify --bundle --nesting --targets '>= 0.25%' $< -o $@
	@touch $@

css: cerberus_crm/static/css/main.min.css ## Build the css

watch-css: ## Watch and build the css
	@echo "Watching scss"
	$(MAKE) css
	@while inotifywait -qr -e close_write assets/; do \
		$(MAKE) css; \
	done

install: $(PIP_SYNC_PATH) requirements.txt requirements.dev.txt ## Install development requirements (default)
	@echo "Installing $(filter-out $<,$^)"
	@python -m piptools sync requirements.txt $(filter-out $<,$^)
