# services/users/project/tests/test_users.py


import json
import unittest
from project import db 
from project.api.models import Customer 
from project.tests.base import BaseTestCase


def add_customer(name):
    customer = Customer(name=name)
    db.session.add(customer)
    db.session.commit()
    return customer


class TestOdersService(BaseTestCase):
    """Tests for the Orders Service."""

    def test_orders(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/orders/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    # para la tabla de customers
    def test_add_customer(self):
        """ Agregando un nuevo cliente"""
        with self.client:
            response = self.client.post(
                '/customers',
                data = json.dumps({
                    'name ':'lilianaclaribel'
                }),
                content_type = 'application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('carga Invalida', data['message'])
            self.assertIn('fallo', data['status'])

    def test_add_customer_invalid_json(self):
        """Asegurando que se produzca un error si el objeto json esta vacio"""
        with self.client:
            response = self.client.post(
                '/customers',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('carga Invalida', data['message'])
            self.assertIn('fallo', data['status'])

    def test_add_customer_duplicate_name(self):
        """Asegurando que se produce un error si el name ya existe."""
        with self.client:
            response = self.client.post(
                '/customers',
                data=json.dumps({
                    'name': 'liliana',
                    
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/customers',
                data=json.dumps({
                    'name': 'liliana',
                    
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Disculpa. El name ya existe.', data['message'])
            self.assertIn('falló', data['status'])

    def test_add_customer_json_keys(self):
        """Asegurando que se produzca un error si el objeto json
        no tiene una clave name"""
        with self.client:
            response = self.client.post(
                '/customers',
                data=json.dumps({'name': 'lilianaclaribel'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('lilianaclaribel was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_single_customer(self):
        """Asegurando que obtenga un customer de forma correcta"""
        customer = add_customer(name='lilianaclaribel')
        with self.client:
            response = self.client.get(f'/customers/{customer.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('lilianaclaribel', data['data']['name'])
            self.assertIn('success', data['status'])

    def test_single_customer_no_id(self):
        """Asegúrese de que se arroje un error si no se proporciona una identificación."""
        with self.client:
            response = self.client.get('/customers/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['message'])
            self.assertIn('fallo', data['status'])
 
    def test_single_customer_incorrect_id(self):
        """Asegurando de que se arroje un error si la identificación no existe."""
        with self.client:
            response = self.client.get('/customers/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El usuario no existe', data['message'])
            self.assertIn('fallo', data['status'])

    def test_all_customer(self):
        """ Asegurando de que todos los usuarios se comporten correctamente."""
        add_customer('liliana')
        add_customer('claribel')
        with self.client:
            response = self.client.get('/customers')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['customer']), 2)
            self.assertIn('liliana', data['data']['customer'][0]['name'])
            self.assertIn('claribel', data['data']['customer'][1]['name'])   
            self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()