import os
import sys
from unittest.mock import patch

sys.path.append(os.path.abspath(''))

from tasks.customer import update_customer_location_data


@patch('tasks.customer.save_customer')
def test_post_route__success(save_customer_mock):

    response_mock = ('New Brunswick', 'NJ', 'Middlesex')

    response = update_customer_location_data(None, None, '08989')

    assert response == response_mock
