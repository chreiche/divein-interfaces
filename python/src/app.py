from src.backend import magic_numbers, day_calculator, employee
import falcon
import json
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend


class ExampleResource(object):
    def on_get(self, req, resp):
        resp.text = "Hello World"
        resp.status = falcon.HTTP_200


"""
Task 1:

GET /lucky_number

by calling this endpoint an response is expected like

200 Your lucky number for the day is: 42

consider using the backend feature 'magic_numbers.get_magic_number()'

"""


class LuckyNumberResource(object):
    def on_get(self, req, resp):

        resp.text = "implement me"
        resp.status = falcon.HTTP_200


"""
Task 2:

GET /greetings

by calling this endpoint with a mandatory parameter 'name' an response is expected like

200 Welcome DiveIn

if the parameter 'name' is omitted a status code 400 is expected with some details on the missing parameter

"""


class GreetingResource(object):
    def on_get(self, req, resp):

        resp.text = "implement me"
        resp.status = falcon.HTTP_200


"""
Task 3:

GET /weekday_calculator

by calling this endpoint with a mendatory header 'n' an response is expected like

200 5.0 days from now is a Monday

if the header 'n' is omitted a status code 400 is expected with some details on the missing header
if the header 'n' is not a valid float a status code 400 is expected with some details on expected data type

consider using the backend feature 'day_calculator.get_weekday_in_n_days(n)'

"""


class WeekdayCalculatorResource(object):
    def on_get(self, req, resp):

        resp.text = "implement me"
        resp.status = falcon.HTTP_200


"""
Task 4:

GET /login

by calling this endpoint with the mandatory baseAuth header (username: DiveIn password: 1234) an response is expected like

200 Login successful!

if the baseAuth header is omitted a status code 401 is expected with some details on the missing baseAuth
if no valid username and/or password are provided a status code 401 is expected with the hint that username/password is invalid

consider implementing user_loader() with check for DiveIn:1234

"""


def user_loader(username, password):
    # check for username = DiveIn and password = 1234

    return {'username': username}


class LoginResource(object):
    def on_get(self, req, resp):

        resp.text = "implement me"
        resp.status = falcon.HTTP_200


"""
Task 5:

consider using the 'db' to perform CRUD operations

"""

db = employee.EmployeeDB()
db.create(name="Alice", age=20)
db.create(name="Bob", age=42)
db.create(name="Charles", age=50)


class EmployeeResource(object):
    """
    Read

    GET /employee/{id}

    by calling this endpoint with the 'id' a response is expected like

    200 {
            "id": 1,
            "name": "Alice",
            "age": 20
        }

    if the id does not correspond to an id in the db a status code 404 is expected with some information that no resource for the id is not found    

    consider using the backend feature 'db.read(id=id)'
    """

    def on_get(self, req, resp, id):

        resp.text = "implement me"
        resp.status = falcon.HTTP_200

    """
    Delete

    DELETE /employee/{id}

    by calling this endpoint with 'id' a response is expected like

    200 {
            "id": 4
            "name": "DiveIn",
            "age": 99
        }

    if the resource for the header 'id' is not found in the backend a status code 204 is expected with some information on the missing resource

    consider using the backend feature 'db.delete(id=id)'
    """

    def on_delete(self, req, resp, id):

        resp.text = "implement me"
        resp.status = falcon.HTTP_200


class EmployeesResource(object):
    """
    Read

    GET /employee

    by calling this endpoint a response is expected like

    200 {
          "1": {
              "name": "Alice",
              "age": 20
          },
          "2": {
              "name": "Bob",
              "age": 42
          },
          "3": {
              "name": "Charles",
              "age": 50
          }
      }

    consider using the backend feature 'db.get_all()'
    """

    def on_get(self, req, resp):

        resp.text = "implement me"
        resp.status = falcon.HTTP_200

    """
    Create

    POST /employee

    by calling this endpoint with a payload like

    {
        "name": "DiveIn",
        "age": 42
    }
    
    a response is expected like

    201 {
            "id": 4
            "name": "DiveIn",
            "age": 42
        }

    if the endpoint is called without payload a status code 400 is expected with some information on the needed payload
    if the key 'age' is not a valid int a status code 400 is expected with some information on the expexted data type 

    consider using the backend feature 'db.create(name=name, age=age)'
    """

    def on_post(self, req, resp):
        payload = req.media

        resp.text = json.dumps(payload)
        resp.status = falcon.HTTP_201

    """
    Update

    PUT /employee

    by calling this endpoint with a payload like

    {
        "id": 4
        "name": "DiveIn",
        "age": 99
    }
    
    a response is expected like

    200 {
            "id": 4
            "name": "DiveIn",
            "age": 99
        }

    if the endpoint is called without payload a status code 400 is expected with some information on the needed payload
    if the key 'age' or 'id' is not a valid int a status code 400 is expected with some information on the expexted data type 
    if the resource for the key 'id' is not found in the backend a status code 404 is expected with some information on the missing resource

    consider using the backend feature 'db.update(id=id, name=name, age=age)'
    """

    def on_put(self, req, resp):
        payload = req.media

        resp.text = json.dumps(payload)
        resp.status = falcon.HTTP_200


auth_backend = BasicAuthBackend(user_loader)
auth_middleware = FalconAuthMiddleware(auth_backend,
                                       exempt_routes=['/example', '/lucky_number', '/greetings', '/weekday_calculator'])

# basic auth enabled with exempts
api = application = falcon.App(middleware=[auth_middleware])

example_endpoint = ExampleResource()
lucky_number_endpoint = LuckyNumberResource()
greeting_endpoint = GreetingResource()
weekday_calculator_endpoint = WeekdayCalculatorResource()
login_endpoint = LoginResource()
employees_endpoint = EmployeesResource()
employee_endpoint = EmployeeResource()

api.add_route('/example', example_endpoint)
api.add_route('/lucky_number', lucky_number_endpoint)
api.add_route('/greetings', greeting_endpoint)
api.add_route('/weekday_calculator', weekday_calculator_endpoint)
api.add_route('/login', login_endpoint)
api.add_route('/employee', employees_endpoint)
api.add_route('/employee/{id:int}', employee_endpoint)
