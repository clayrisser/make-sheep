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

.PHONY: format
format:
	@env/bin/yapf -ir -vv \
    $(CWD)/*.py
	@env/bin/unify -ir \
    $(CWD)/*.py

env:
	@virtualenv env
	@env/bin/pip3 install -r ./requirements.txt

.PHONY: invoke
invoke:
	@env/bin/lambda invoke -v

.PHONY: deploy
deploy:
	@env/bin/lambda deploy

.PHONY: clean
clean:
	@git clean -fXd -e \!env -e \!env/**/*
