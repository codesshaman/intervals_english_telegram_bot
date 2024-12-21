name = Python Application
APPNAME:=$(word 2, $(MAKECMDGOALS))
DIR:= $(abspath $(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
VENV_DIR=.venv
VENV=$(DIR)/$(VENV_DIR)
VENV_BIN=$(VENV)/bin
PYTHON=$(VENV_BIN)/python3
PIP=$(VENV_BIN)/pip3

NO_COLOR=\033[0m	# Color Reset
COLOR_OFF=\e[0m		# Color Off
OK_COLOR=\033[32;01m	# Green Ok
ERROR_COLOR=\033[31;01m	# Error red
WARN_COLOR=\033[33;01m	# Warning yellow


# git clone github-repo:codesshaman/telegram_messages_sendler_bot.git

all:
	@printf "Launch configuration ${name}...\n"
	$(PYTHON) main.py

env:
	@printf "$(ERROR_COLOR)==== Create environment file for ${name}... ====$(NO_COLOR)\n"
	@if [ -f .env ]; then \
		rm .env; \
	fi; \
	cp .env.example .env

freeze:
	@$(PIP) freeze

git:
	@printf "$(YELLOW)==== Set user name and email to git for ${name} repo... ====$(NO_COLOR)\n"
	@bash gituser.sh

help:
	@echo -e "$(OK_COLOR)==== All commands of ${name} configuration ====$(NO_COLOR)"
	@echo -e "$(WARN_COLOR)- make help				: 0. Manual"
	@echo -e "$(WARN_COLOR)- make env				: 1. Create .env-file (change manualy!)"
	@echo -e "$(WARN_COLOR)- make git				: 2. Set user and mail for git"
	@echo -e "$(WARN_COLOR)- make venv				: 3. Create virtual environment"
	@echo -e "$(WARN_COLOR)- make req				: 4. Install requirements"
	@echo -e "$(WARN_COLOR)- make				    	: 5. Application launch"
	@echo -e "$(WARN_COLOR)- make install				: Install library in pip"
	@echo -e "$(WARN_COLOR)- make freeze				: Libraryes list"
	@echo -e "$(WARN_COLOR)- make push				: Push to the repository"
	@echo -e "$(WARN_COLOR)- make clean				: Clean applicatin cache"
	@echo -e "$(WARN_COLOR)- make fclean				: Remove virtual environment"

install:
	@printf "$(OK_COLOR)==== Launch pip install ====$(NO_COLOR)\n"
	@printf "$(OK_COLOR)==== Downloading a new library ====$(NO_COLOR)\n"
	@$(eval args := $(words $(filter-out --,$(MAKECMDGOALS))))
	@if [ "${args}" -eq 2 ]; then \
		echo "$(OK_COLOR) Downloading the library ${APPNAME}$(NO_COLOR)\n"; \
		cd apps; \
		$(PIP) install ${APPNAME}; \
		cd ..; \
	elif [ "${args}" -gt 2 ]; then \
		echo "$(ERROR_COLOR)The library name must not contain spaces!$(NO_COLOR)\n"; \
	else \
		echo "$(ERROR_COLOR)Enter the library name!$(NO_COLOR)\n"; \
	fi

venv:
	@printf "$(OK_COLOR)==== Launch virtual environment for ${name} ====$(NO_COLOR)\n"
	@if [ ! -d "${VENV}" ]; then \
        echo "Creating virtual environment..."; \
        python3 -m venv ${VENV}; \
    fi

push:
	@bash push.sh

req:
	@printf "$(OK_COLOR)==== Install python requirements ====$(NO_COLOR)\n"
	@if [ -d "${VENV}" ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "Окружение отсутствует"; \
		echo "Команда для создания:"; \
		echo "make venv"; \
	fi

clean:
	@printf "$(ERROR_COLOR)==== Cleaning cache ${name}... ====$(NO_COLOR)\n"
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d | xargs rm -fr

fclean: clean
	@printf "$(ERROR_COLOR)==== Cleaning configuration ${name}... ====$(NO_COLOR)\n"
	@rm -rf ${VENV}

.PHONY	: all help make migrate venv vexit clean
