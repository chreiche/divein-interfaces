from src.backend import magic_numbers, day_calculator, employee
import falcon
import json
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend


class LuckyNumberResource(object):
    def on_get(self, req, resp):
        resp.text = f"Your lucky number for the day is: {magic_numbers.get_magic_number()}"
        resp.status = falcon.HTTP_200


class GreetingResource(object):
    def on_get(self, req, resp):

        name = req.get_param("name", required=True)

        resp.text = f"Welcome {name}!"
        resp.status = falcon.HTTP_200


class WeekdayCalculatorResource(object):
    def on_get(self, req, resp):

        header_n = req.get_header("n", required=True)

        try:
            n = float(header_n)
        except ValueError:
            resp.text = f"{header_n} is no valid float! Valid examples are -1, 0, 5.5"
            resp.status = falcon.HTTP_400
            return

        resp.text = f"{n} days from now is a {day_calculator.get_weekday_in_n_days(n)}"
        resp.status = falcon.HTTP_200


class LoginResource(object):
    def on_get(self, req, resp):

        resp.text = f"Login successful!"
        resp.status = falcon.HTTP_200


db = employee.EmployeeDB()
db.create(name="Alice", age=20)
db.create(name="Bob", age=42)
db.create(name="Charles", age=50)


class EmployeeResource(object):
    def on_get(self, req, resp):

        id = req.get_header("id", required=False)

        if id:
            try:
                id = int(id)
            except ValueError:
                resp.text = f"{id} is no valid int! Valid examples are 0, 1, 2"
                resp.status = falcon.HTTP_400
                return
            res = db.read(id=id)

            if res:
                resp.text = json.dumps(res)
                resp.status = falcon.HTTP_200
                return

            resp.text = f"no employee found with id: {id}"
            resp.status = falcon.HTTP_404
            return

        resp.text = json.dumps(db.get_all())
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        payload = req.media

        name = payload["name"]
        age = payload["age"]

        try:
            age = int(age)
        except ValueError:
            resp.text = f"{age} is no valid int! Valid examples are 20, 42, 50"
            resp.status = falcon.HTTP_400
            return

        res = db.create(name=name, age=age)

        resp.text = json.dumps(res)
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp):
        payload = req.media

        id = payload["id"]
        name = payload["name"]
        age = payload["age"]

        try:
            id = int(id)
        except ValueError:
            resp.text = f"{id} is no valid int! Valid examples are 0, 1, 2"
            resp.status = falcon.HTTP_400
            return

        try:
            age = int(age)
        except ValueError:
            resp.text = f"{age} is no valid int! Valid examples are 20, 42, 50"
            resp.status = falcon.HTTP_400
            return

        res = db.update(id=id, name=name, age=age)

        if res:
            resp.text = json.dumps(res)
            resp.status = falcon.HTTP_200
            return

        resp.text = f"no employee found with id: {id}"
        resp.status = falcon.HTTP_404

    def on_delete(self, req, resp):
        id = req.get_header("id", required=True)

        try:
            id = int(id)
        except ValueError:
            resp.text = f"{id} is no valid int! Valid examples are 0, 1, 2"
            resp.status = falcon.HTTP_400
            return

        res = db.delete(id=id)

        if res:
            resp.text = json.dumps(res)
            resp.status = falcon.HTTP_200
            return

        resp.text = f"no employee found with id: {id}"
        resp.status = falcon.HTTP_204


def user_loader(username, password):
    user = {"DiveIn": "1234"}

    if user.get(username):
        if password == user.get(username):
            return {'username': username}

    return None


auth_backend = BasicAuthBackend(user_loader)
auth_middleware = FalconAuthMiddleware(auth_backend,
                                       exempt_routes=['/lucky_number', '/greetings', '/weekday_calculator'])

api = application = falcon.App(middleware=[auth_middleware])

lucky_number_endpoint = LuckyNumberResource()
greeting_endpoint = GreetingResource()
weekday_calculator_endpoint = WeekdayCalculatorResource()
login_endpoint = LoginResource()
employee_endpoint = EmployeeResource()

api.add_route('/lucky_number', lucky_number_endpoint)
api.add_route('/greetings', greeting_endpoint)
api.add_route('/weekday_calculator', weekday_calculator_endpoint)
api.add_route('/login', login_endpoint)
api.add_route('/employee', employee_endpoint)
