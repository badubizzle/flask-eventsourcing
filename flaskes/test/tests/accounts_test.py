from hypothesis import given
import hypothesis.strategies as st
from flask import url_for

from hypothesis import settings


seen = {}
@given(username=st.text(min_size=3,alphabet=st.characters(whitelist_categories=('Lu','Ll'), min_codepoint=ord('A'), max_codepoint=ord('z'))))
@settings(deadline=None)
def test_create_user(client, username,snapshot):
     global seen
     if username in seen:
          return
     
     
     response = client.post("/api/users/", data={'username': username})
     assert response.status_code == 200          
     assert 'user' in response.json
     assert 'token' in response.json
     seen[username] = response.json
     assert response.status_code == 200


@st.composite
def some_user(draw):
     global seen
     return draw(st.sampled_from(list(seen.keys())))


@given(username=some_user())
@settings(deadline=None)
def test_create_user_bank_account(app, client, username):
     
     global seen

     response_json = seen[username]
     token = response_json['token'][0]
     with app.app_context():
          url = url_for('api.user_accounts', username=username)
          response = client.post(url, headers={'Authorization': 'Bearer {0}'.format(token)})
          assert response.status_code == 201 
          
                                                                



@given(username=some_user())
@settings(deadline=None)
def test_get_user_bank_accounts(app, client, username):
     
     global seen

     response_json = seen[username]
     token = response_json['token'][0]
     with app.app_context():
          url = url_for('api.user_accounts', username=username)
          response = client.get(url, headers={'Authorization': 'Bearer {0}'.format(token)})#, query_string={'username': username})
                 
          assert response.status_code == 200 

          assert 'accounts' in response.json
          seen[username]['accounts'] = response.json['accounts']
          


@given(username=some_user(), amount=st.integers(min_value=1, max_value=999999))
@settings(deadline=None)
def test_get_deposit_money(app, client, username, amount):
     
     global seen

     if not username in seen:
          return

     response_json = seen[username]

     if not 'accounts' in response_json or len(response_json['accounts'])==0:
          return

     token = response_json['token'][0]
     account = response_json['accounts'][0]
     with app.app_context():
          url = url_for('api.deposit', username=username, account_id=account['uuid'])
          headers={'Authorization': 'Bearer {0}'.format(token)}
          response = client.post(url, data={'amount':amount}, headers=headers)     
          assert response.status_code == 201 

          url = url_for('api.user_account_details', username=username, account_id=account['uuid'])
          response = client.get(url, headers=headers)
          
          assert response.status_code == 200
          assert 'balance' in response.json
          assert response.json['balance'] >= amount
          
                                                               
                    
     