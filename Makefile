PIP_TOOLS_VERSION=3.3.1

compile-requirements-py2:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		for reqfile in $$(find requirements/ -maxdepth 1 -name '*.in' -print); do \
			final_reqfile="requirements/py2/$$( basename $${reqfile%.*}.txt )";\
			echo "Compiling $$reqfile to $$final_reqfile"; \
			python2 -m piptools compile --output-file $$final_reqfile $$reqfile; done

sync-installed-pip-requirements-py2:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		reqs=""; for reqfile in $$(find $(CURDIR)/requirements/py2 -maxdepth 1 -name '*.txt' -print); do \
			reqfile=$$(realpath --relative-to=$(CURDIR) $$reqfile); \
			reqs="$$reqs $$reqfile"; done; \
			python2 -m piptools sync $$reqs

upgrade-pip-requirement-py2:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		for reqfile in $$(find requirements/ -maxdepth 1 -name '*.in' -print); do \
			final_reqfile="requirements/py2/$$( basename $${reqfile%.*}.txt )";\
			echo "Upgrading $(req) in $$final_reqfile"; \
			python2 -m piptools compile --output-file $$final_reqfile $$reqfile -P $(req); done

upgrade-requirements-py2:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		for reqfile in $$(find requirements/ -maxdepth 1 -name '*.in' -print); do \
			final_reqfile="requirements/py2/$$( basename $${reqfile%.*}.txt )";\
			echo "Compiling $$reqfile to $$final_reqfile"; \
			python2 -m piptools compile -U --output-file $$final_reqfile $$reqfile; done

compile-requirements-py3:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		for reqfile in $$(find requirements/ -maxdepth 1 -name '*.in' -print); do \
			final_reqfile="requirements/py3/$$( basename $${reqfile%.*}.txt )";\
			echo "Compiling $$reqfile to $$final_reqfile"; \
			python3 -m piptools compile --output-file $$final_reqfile $$reqfile; done

sync-installed-pip-requirements-py3:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		reqs=""; for reqfile in $$(find $(CURDIR)/requirements/py3 -maxdepth 1 -name '*.txt' -print); do \
			reqfile=$$(realpath --relative-to=$(CURDIR) $$reqfile); \
			reqs="$$reqs $$reqfile"; done; \
			python3 -m piptools sync $$reqs

upgrade-pip-requirement-py3:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		for reqfile in $$(find requirements/ -maxdepth 1 -name '*.in' -print); do \
			final_reqfile="requirements/py3/$$( basename $${reqfile%.*}.txt )";\
			echo "Upgrading $(req) in $$final_reqfile"; \
			python3 -m piptools compile --output-file $$final_reqfile $$reqfile -P $(req); done

upgrade-requirements-py3:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		for reqfile in $$(find requirements/ -maxdepth 1 -name '*.in' -print); do \
			final_reqfile="requirements/py3/$$( basename $${reqfile%.*}.txt )";\
			echo "Compiling $$reqfile to $$final_reqfile"; \
			python3 -m piptools compile -U --output-file $$final_reqfile $$reqfile; done
