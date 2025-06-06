you can start the code with the help of 

installing all the requirements in the requirements.txt file 

running cmd

python -m src 


there are 5 test users in the data base 

user1@example.com
user2@example.com
user3@example.com
user4@example.com
user5@example.com


there are 3 classes as you told 

yoga,zumba,hiit



the swagger of the app will be available at url listed below
http://127.0.0.1:8000/docs

curl -X 'GET' \
  'http://127.0.0.1:8000/class' \
  -H 'accept: application/json'




returns => [
  {
    "class_name": "Yoga",
    "instructor": "anshul",
    "class_id": "f29d0b27-dc1e-4578-8c0b-5d27b40a75c4",
    "batch_creation": "2025-06-06T13:59:16.327507",
    "left_seats": 9
  },
  {
    "class_name": "Zumba",
    "instructor": "komal",
    "class_id": "a36d9a4f-b674-4c04-b6a2-f0ee776b6536",
    "batch_creation": "2025-06-06T14:34:43.913855",
    "left_seats": 11
  },
  {
    "class_name": "HIIT",
    "instructor": "HIIT123",
    "class_id": "0350406d-7c66-41de-a284-f30655ecf138",
    "batch_creation": "2025-06-06T14:48:16.775125",
    "left_seats": 10
  }
]



curl -X 'GET' \
  'http://127.0.0.1:8000/bookings?email_id=abc23%40example.com' \
  -H 'accept: application/json'

returns=>
{
  "user_id": "3e680d8e-6b94-4170-94de-c19cf1fbde8d",
  "user_name": "string",
  "total_classes": 1,
  "enrolled_classes": [
    {
      "class_id": "a36d9a4f-b674-4c04-b6a2-f0ee776b6536",
      "class_name": "Zumba",
      "start_time": "2025-06-06T09:08:35.785000",
      "end_time": "2025-06-06T09:08:35.785000",
      "capacity": 12,
      "status": 1
    }
  ]
}

//this api will have to change the class id because you cant enroll same student to same class again try with 0350406d-7c66-41de-a284-f30655ecf138
curl -X 'POST' \
  'http://127.0.0.1:8000/book' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "client_name": "abc23@example.com",
  "client_email": "abc23@example.com",
  "class_id": "f29d0b27-dc1e-4578-8c0b-5d27b40a75c4"
}'

returns=>
"added successfully"








you can also add the use and also add some more classes i have done that extra there is lot more in the model of the code but i have restricted what you can use through the swagger have a look at the code to see all the thing 
__main__
file in my code is used to register the models in the sqllite database and also running the uvicorn server at port 8000

lets talk about the structure of the code so the src contain all the main file related to the code part it has section

the api section consists of all the api and the base_api file in it is use to registed the api routers to the base app instance 

the validator section consists of different validator for different task of processor basically it is validating that before processing the data the data we are getting is it good and valid 

the processor section incudes the logic to how we are going to maupulate the data in the way we need to store in the database

the repository section is responsible for interecting with the database layer through sqlalchemy

the mapper section is just mappeing the data to create object of the table that we could insert directly 

utils has the singletone pattern code and also the jwt code which i left because you did not ask for it 

in the model section we are also connection with the database using async connection pool
and generating session and passing it from api to the repository layer so that we can maintain a transaction across the complete file 
