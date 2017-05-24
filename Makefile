SHELL := /bin/bash
CWD := $(shell pwd)

.PHONY: all
all: clean

env:
	@virtualenv env
	@env/bin/pip install -r ./requirements.txt
	@echo created virtualenv

.PHONY: freeze
freeze:
	@env/bin/pip freeze > ./requirements.txt
	@echo froze requirements

.PHONY: invoke
invoke:
	@lambda invoke -v

.PHONY: deploy
deploy:
	@lambda deploy
	@echo deployed

.PHONY: init
init:
	@./env/bin/python manage.py init ./config.template.yaml ./config.template.yaml
	@echo initialized ./config.template.yaml

.PHONY: auth
auth: env
	@./env/bin/python manage.py auth ./config.template.yaml ./config.yaml
	@echo created ./config.yaml

.PHONY: clean
clean:
	-@rm -rf ./env ./config.yaml ./dist ./*.pyc
	@echo cleaned
