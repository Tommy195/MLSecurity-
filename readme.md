### To set up and run the app
- pip install requirements.txt
- update you keys con .env file 

### Start Postgres or SQL Server db and update credentials on `config.py`
* update `SQLALCHEMY_DATABASE_URI` in app.py with db config name
* SQL alchemy will create the database objects on app creation.

### Example endpoints
#### Add user 
`curl -d "username=user1&password=abcd" -X POST http://localhost:5000/register`

#### Login
###### _`(Returns Auth Token)`_
`curl -d "username=user1&password=abcd" -X POST http://localhost:5000/user`

#### Import from external api
###### _`(Replace with Auth Token)`_
`curl -XGET -H "Authorization: Bearer paste_token_here http://localhost:5000/information

#### Get list of imported data
###### _`(Replace with Auth Token)`_
`curl -XGET -H "Authorization: Bearer paste_token_here http://localhost:5000/infomationlist

#### Get one information by id
###### _`(Replace with Auth Token)`_
`curl -XGET -d "id=1" -H "Authorization: Bearer paste_token_here http://localhost:5000/information/id

#### Delete one information by id
###### _`(Replace with Auth Token)`_
`curl -DELETE -d "id=1" -H "Authorization: Bearer paste_token_here http://localhost:5000/information/id