

from hypothesis import given
import hypothesis.strategies as st
from flask import url_for


seen = {}
@given(username=st.text(min_size=3,alphabet=st.characters(min_codepoint=ord('A'), max_codepoint=ord('z'))))
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
def test_get_user_details(app, client, username, snapshot):
      
     response_json = seen[username]
     token = response_json['token'][0]
     with app.app_context():
          url = url_for('api.user_details', username=username)
          response = client.get(url, headers={'Authorization': 'Bearer {0}'.format(token)})
          
          assert response.status_code == 200          
          assert 'uuid' in response.json
          assert 'username' in response.json          
               
          assert response.status_code == 200
     