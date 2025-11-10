# Bee Kind Application

An application for beekeeping

This project is under dev and not suitable for use of any kind


## Dev Installation

### Requirements

* Python3.12

### Prepare

It is strongly recommended that you use a separate python environment for this work. These instructions assume the use of venv
on linux, other envs and OSes are available, and if you prefer them, then please amend the instructions as required:

#### Checkout the code

```shell
$ git clone git@github.com:<<Repo>>
$ cd <<folder>>
```

#### Prepare the venv

```shell
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -U pip
```

A requirements.txt is committed with this repo and can be used, but it is recommended to recompile the requirements.txt file from
the pyproject.toml - especially if developing on windows (you monster).

```shell
(venv) $ pip install pip-tools
(venv) $ pip-compile --extra dev pyproject.toml
```

(if you are not planning on developing you can/should omit the `--extra dev` argument)

Install the requirements

```shell
(venv) $ pip install -r requirements.txt
```

#### Install pre-commit hooks

```shell
(venv) $ pre-commit install
```

The pre-commit hooks:

* `black` (using rules in `pyproject.yaml`)
* `flake8` (using the rules in `.flake8`)
