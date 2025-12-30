"""
This module provides utility functions for the food truck tests.
"""
import json
import logging
from enum import Enum

import requests

BASE_URL = 'http://localhost:5000/api/MobileFoodTrucks/'


class EndPoints(Enum):
    """Food Truck Endpoints"""
    SEARCH_BY_NAME = 'searchByName'
    SEARCH_BY_STREET = 'searchByStreet'
    NEAREST_FOOD_TRUCK = 'nearestFoodTrucks'


class ApplicantStatus(Enum):
    """Food Truck Application Statuses"""
    APPROVED = 'APPROVED'
    REQUESTED = 'REQUESTED'
    EXPIRED = 'EXPIRED'
    ISSUED = 'ISSUED'
    SUSPEND = 'SUSPEND'


def api_request(url: str, payload: dict) -> requests.Response:
    """Lowest level get call to a FoodTruck API endpoint."""
    full_url = BASE_URL + url
    logging.debug(f'Making get request to "{full_url}" with payload" {payload}')
    # Might want to have additional retry functionality
    api_response = requests.get(full_url, params=payload)
    logging.debug(api_response.text)
    logging.debug(api_response.status_code)

    if api_response.status_code == 200:
        results = api_response.json()
        logging.debug(f'Formatted payload response:\n{json.dumps(results, indent=4)}')
        food_trucks = len(results)
        if food_trucks == 1:
            description = 'Food Truck was'
        else:
            description = 'Food Trucks were'
        logging.debug(f'{len(results)} {description} returned from the call to "{full_url}"')
    return api_response


def get_search_by_name(payload: dict) -> requests.Response:
    """Make a GET request to the FoodTruck searchByName endpoint."""
    return api_request(EndPoints.SEARCH_BY_NAME.value, payload)


def get_search_by_street(payload: dict) -> requests.Response:
    """Make a GET request to the FoodTruck searchByStreet endpoint."""
    return api_request(EndPoints.SEARCH_BY_STREET.value, payload)


def get_nearest_food_trucks(payload: dict) -> requests.Response:
    """Make a GET request to the FoodTruck nearestFoodTrucks endpoint."""
    return api_request(EndPoints.NEAREST_FOOD_TRUCK.value, payload)


def log_header(header: str):
    """Standard header formatting"""
    header_length = len(header)
    logging.info('')
    logging.info('*' * header_length)
    logging.info(header)
    logging.info('*' * header_length)
    logging.info('')
