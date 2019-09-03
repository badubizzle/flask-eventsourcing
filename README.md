# Flask GraphQL application

1. Authentication with jwt
2. Protected Mutations and Queries
3. Flask migrate

### Running

1. Clone repo `git clone https://github.com/badubizzle/flask-graphql.git flask-graphql`
1. `cd flask-graphql`
1. Add config `cat config/sample.settings.py > config/settings.py`
1. Install virual env `pip install virtualenv`
1. Create virual environment `virtualenv venv`
1. Activate virtual env `source venv/bin/activate`
1. Install dependencies `pip install -r requirements.txt`
1. Create database `make db-upgrade`
1. Start server `make run`

1. open http://localhost:5000/graphql

## Running Tests

`make test`
