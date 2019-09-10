CWD := $(shell pwd)
ARGS := ""

.PHONY: all
all: clean

.PHONY: install
install: env

.PHONY: uninstall
uninstall:
	-@rm -rf env >/dev/null || true

.PHONY: reinstall
reinstall: uninstall install
	@cd examples/javascript && make reinstall

.PHONY: format
format:
	@env/bin/yapf -ir -vv \
    $(CWD)/*.py \
    $(CWD)/sphinx_markdown_builder
	@env/bin/unify -ir \
    $(CWD)/*.py \
    $(CWD)/sphinx_markdown_builder

env:
	@virtualenv env
	@env/bin/pip3 install -r ./requirements.txt

.PHONY: invoke
invoke:
	@lambda invoke -v

.PHONY: deploy
deploy:
	@lambda deploy

.PHONY: init
init:
	@env/bin/python manage.py init ./config.template.yaml ./config.template.yaml

.PHONY: auth
auth: env
	@env/bin/python manage.py auth ./config.template.yaml ./config.yaml

.PHONY: clean
clean:
	@git clean -fXd -e \!env -e \!env/**/*
