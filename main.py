from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# In-memory data store
employees_data = [
    {'id': 1, 'name': 'Abhilash Gaurav'},
    {'id': 2, 'name': 'Ramish Verma'}
]

class EmployeesResource(Resource):
    def get(self):
        """
        Get a list of all employees
        ---
        responses:
          200:
            description: A list of employees
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: John Doe
        """
        return employees_data, 200

    def post(self):
        """
        Add a new employee
        ---
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                  example: Alice Smith
        responses:
          201:
            description: The added employee
          400:
            description: Bad request
        """
        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Name is required'}, 400
        new_id = employees_data[-1]['id'] + 1 if employees_data else 1
        new_employee = {'id': new_id, 'name': data['name']}
        employees_data.append(new_employee)
        return new_employee, 201

class EmployeeResource(Resource):
    def put(self, employee_id):
        """
        Update an existing employee
        ---
        parameters:
          - in: path
            name: employee_id
            type: integer
            required: true
            description: ID of the employee to update
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: Updated Name
        responses:
          200:
            description: The updated employee
          404:
            description: Employee not found
        """
        data = request.get_json()
        for employee in employees_data:
            if employee['id'] == employee_id:
                employee['name'] = data.get('name', employee['name'])
                return employee, 200
        return {'message': 'Employee not found'}, 404

    def delete(self, employee_id):
        """
        Delete an existing employee
        ---
        parameters:
          - in: path
            name: employee_id
            type: integer
            required: true
            description: ID of the employee to delete
        responses:
          200:
            description: Employee deleted successfully
          404:
            description: Employee not found
        """
        for i, employee in enumerate(employees_data):
            if employee['id'] == employee_id:
                deleted_employee = employees_data.pop(i)
                return {'message': 'Employee deleted successfully', 'employee': deleted_employee}, 200
        return {'message': 'Employee not found'}, 404

api.add_resource(EmployeesResource, '/employees')
api.add_resource(EmployeeResource, '/employee/<int:employee_id>')

if __name__ == '__main__':
    app.run(debug=True)
