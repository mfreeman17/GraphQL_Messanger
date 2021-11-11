from app.main import schema
from app.database import  get_db
from app.models import Users
import pytest

USER1 = "test_user"
USER2 = "test_user_2"
PASSWORD = "123456"
MESSAGE = "Hi user 2"

def pytest_configure():
    pytest.jwt1 = None
    pytest.jwt2 = None

def test_create_users():

    query = """
        mutation testcreate($user: String!, $password: String!){
          createUser(username: $user, password : $password)
        }

    """

    result = schema.execute_sync(
        query,
        variable_values = {
        "user": USER1,
        "password": PASSWORD},
         )
    assert(result.errors is  None)
    assert(result.data["createUser"] == f"created user {USER1}")
    #create a second user
    result2 = schema.execute_sync(
        query,
        variable_values = {
        "user": USER2,
        "password": PASSWORD},
         )
    assert(result2.errors is  None)
    assert(result2.data["createUser"] == f"created user {USER2}")

def test_login():
    # note if  create users fails this will also fail

    query = """
        mutation login($user: String!, $password: String!){
          login(username: $user, password : $password){
              __typename
                ... on LoginSuccess {
                  token
                  tokenType
                }
                ... on LoginError {
                  message
                }
          }
        }
    """
    #login user 1
    result = schema.execute_sync(
        query,
        variable_values = {
        "user": USER1,
        "password": PASSWORD},
         )
    assert(result.errors is  None)
    assert(result.data["login"]["tokenType"] == "bearer")
    pytest.jwt1 = result.data["login"]["token"]
    result2 = schema.execute_sync(
        query,
        variable_values = {
        "user": USER2,
        "password": PASSWORD},
         )
    assert(result2.errors is  None)
    assert(result2.data["login"]["tokenType"] == "bearer")
    pytest.jwt2 = result2.data["login"]["token"]
def test_failed_login():
    query = """
        mutation login($user: String!){
          login(username: $user, password : "wrong password;"){
              __typename
                ... on LoginSuccess {
                  token
                  tokenType
                }
                ... on LoginError {
                  message
                }
          }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values = {
        "user": USER1}
        )
    assert(result.errors is  None)
    assert(result.data["login"]["message"] is not None)


def test_send_message():
    # note if  login fails this will also fail

    # sends a message from user 1 to user 2
        query = """
            mutation testSend($recipient: String!, $message: String!, $token: String!){
              sendMessage(recipientUsername: $recipient, message : $message, jwtToken: $token)
            }
        """
        result = schema.execute_sync(
            query,
            variable_values = {
            "recipient": USER2,
            "message": MESSAGE,
            "token" : str(pytest.jwt1)
            }
        )
        assert(result.errors is  None)
        assert(result.data["sendMessage"] == "message sent")
def test_read_message():
    # read messages as USER2
    query = """
        query testGet($token: String!){
          getYourMessages( jwtToken: $token){
            content
          }

        }
    """
    result = schema.execute_sync(
        query,
        variable_values = {
        "token" : pytest.jwt2
        }
    )
    print("RESULTS", result)
    assert(result.errors is  None)
    assert(result.data["getYourMessages"][0]['content']==MESSAGE)
def test_delete_users():
    db = next(get_db())
    db.query(Users).filter(Users.username==USER1).delete()
    db.query(Users).filter(Users.username==USER2).delete()
    db.commit()
