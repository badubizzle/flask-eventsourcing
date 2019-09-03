TESTS_DIR = ./flaskes/test/tests/*.py

db-init:;FLASK_APP=flaskges/main.py flask db init
db-migrate:;FLASK_APP=flaskes/main.py flask db migrate
db-upgrade:;FLASK_APP=flaskes/main.py flask db upgrade
run:;python3 -m flaskes.main
# test:; pytest -s

test:; @for f in ${TESTS_DIR};\
 do echo "Running test $${f}";\
  pytest -s -vv $${f}; done