test-coverage:
	@nosetests --with-coverage --cover-package doxygen_whiner \
		--cover-erase --cover-html --cover-html-dir coverage
