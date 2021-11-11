To run this api run uvicorn app.main:app
This will start a session on localhost:8000
In your browser go to localhost:8000/graphql.
This will take you to GraphiQL which is an in-browser tool for writing, validating, and testing GraphQL queries.

Several queeries and mutations are possible.

The first mutation one should run is to make a new user. This requires a username and a password. 
The query should look as follows:

mutation{
  createUser(username: "{Your username}", password : "{Your password}")
}

This will return a string saying user created or it will throw an error if the username has already been used.

The next queery one should run is login:

mutation{
 login(username: "{username}", password : "{password}")
 {
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
This will return a login success type if the login was succesful. The login success will include a JSON Web Token and a token type (in this case the type is always bearer)
The JWT is currently set to expier after 30 minuets, so you will have to login to get a new token after that. 

You should save the Token as the next queeries and mutations will require the token to perform any action.

If there is a LoginError you will recieve a message explaining the login error.


The next mutation is send message:

mutation{
 sendMessage(recipientUsername: "{recipient username}", message: "{Your message}"
   jwtToken: "{the token from the login}")
}
This will return saying either message sent or could not validate token, or could not find username.

And finally you can read the message using the following queery

query{
  getYourMessages(jwtToken: "{token}"){
    author, conent, time_created
  }
}
This will return a list of all messages sent to you.

Next Steps:
CI/CD pipeline
Dockerize
Encrypt Messages
Build Front End
