.PHONY: venv

VENV_HOME := ${WORKON_HOME}/pydominion

all:

pex:
	python3 ./setup.py bdist_pex --pex-args '-vv'


venv:
	python3 -m venv ${VENV_HOME}
	${VENV_HOME}/bin/pip install -U pip
	${VENV_HOME}/bin/pip install -r requirements-dev.txt

clean:
	/bin/rm -rf ${VENV_HOME}
