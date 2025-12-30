"""
Tests for the FoodTruck API endpoints.

There are three endpoints, which are all gets.
 - /api/MobileFoodTrucks/searchByName
    - name: required (does a partial match)
    - status: not required
 - /api/MobileFoodTrucks/searchByStreet
    - street: required (does a partial match)
 - /api/MobileFoodTrucks/nearestFoodTrucks
 - name: required (does a partial match)
    - latitude: not required (defaults to 0)
    - longitude: not required (defaults to 0)
    - status: not required

Swagger documentation: http://localhost:5000/swagger/index.html
"""
import logging

import pytest

from tests.utils import get_search_by_name, get_search_by_street, get_nearest_food_trucks, log_header, ApplicantStatus


# Test case notes
#   - Probably pick better test data examples with more time
#   - Plenty more test cases could be thought of
#       - special character processing in applicant name
#       - any limit to the length of the strings in the payload provided
#   - Did not confirm all the responses were correct

# Verification notes
#   - Would also want to verify error messages on expected non-200 responses
#   - Would also want to have verification of the Applicant data that is returned

# Function notes
#   - May be able to reuse code in the 3 test methods, though they should be expanded which may differentiate them more


@pytest.fixture(autouse=True, scope="function")
def test_function_header(request):
    """
    An auto-use fixture that runs before every test.
    """
    log_header(f'START TEST CASE: {request.node.nodeid}')
    yield
    log_header(f'FINISHED TEST CASE: {request.node.nodeid}')


search_by_name_tests = [
    (
        {'payload': {'name': 'Geez', 'status': ApplicantStatus.APPROVED.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 1}},
        {'test_description': 'Partial name match'}
    ),
    (
        {'payload': {'name': 'Casita Vegana', 'status': ApplicantStatus.APPROVED.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 1}},
        {'test_description': 'Full name match'},
    ),
    (
        {'payload': {'name': 'Tacos Rodriguez'}},
        {'expected_results': {'status_code': 200, 'applicants_found': 4}},
        {'test_description': 'Full name match with multiple applications'},
    ),
    (
        {'payload': {'name': 'Casita Vegana'}},
        {'expected_results': {'status_code': 200, 'applicants_found': 1}},
        {'test_description': 'No status supplied'},
    ),
    (
        {'payload': {'name': 'Tacos Rodriguez', 'status': ApplicantStatus.REQUESTED.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 4}},
        {'test_description': f'{ApplicantStatus.REQUESTED.value} status supplied'},
    ),
    (
        {'payload': {'name': 'Liang Bai Ping', 'status': ApplicantStatus.EXPIRED.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 33}},
        {'test_description': f'{ApplicantStatus.EXPIRED.value} status supplied'},
    ),
    (
        {'payload': {'name': 'Serendipity SF', 'status': ApplicantStatus.ISSUED.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 1}},
        {'test_description': f'{ApplicantStatus.ISSUED.value} status supplied'},
    ),
    (
        {'payload': {'name': 'Flavors of Africa', 'status': ApplicantStatus.SUSPEND.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 3}},
        {'test_description': f'{ApplicantStatus.SUSPEND.value} status supplied'},
    ),
    (
        {'payload': {'name': 'Does not exist', }},
        {'expected_results': {'status_code': 200, 'applicants_found': 0}},
        {'test_description': 'No applicant found'},
    ),
    (
        {'payload': {}},
        {'expected_results': {'status_code': 400, 'applicants_found': 0}},
        {'test_description': 'No name supplied in payload'},
    ),
    (
        # Should consider if status should be validated by Food Trucks API
        {'payload': {'name': 'Flavors of Africa', 'status': 'Does not exist'}},
        {'expected_results': {'status_code': 200, 'applicants_found': 0}},
        {'test_description': 'Invalid status supplied'},
    )
]


# Note: Should use a method to pull test IDs from the list of test data rather than needing to manually update the ids list when test cases are added and removed
@pytest.mark.parametrize('test_data', search_by_name_tests,
                         ids=[search_by_name_tests[0][2]['test_description'], search_by_name_tests[1][2]['test_description'], search_by_name_tests[2][2]['test_description'],
                              search_by_name_tests[3][2]['test_description'], search_by_name_tests[4][2]['test_description'], search_by_name_tests[5][2]['test_description'],
                              search_by_name_tests[6][2]['test_description'], search_by_name_tests[7][2]['test_description'], search_by_name_tests[8][2]['test_description'],
                              search_by_name_tests[9][2]['test_description'], search_by_name_tests[10][2]['test_description']])
def test_search_by_name(test_data: list):
    payload = test_data[0]['payload']
    expected_status_code = test_data[1]['expected_results']['status_code']
    expected_applicants_found = test_data[1]['expected_results']['applicants_found']

    response = get_search_by_name(payload)
    actual_status_code = response.status_code
    actual_applicants_found = len(response.json())

    status_code_validation = f'Expected status code: {expected_status_code} | Actual status code: {actual_status_code}'
    if actual_status_code != expected_status_code:
        logging.error(status_code_validation)
    else:
        logging.info(status_code_validation)

    assert actual_status_code == expected_status_code, status_code_validation

    if actual_status_code == 200:
        applicants_found_validation = f'Expected applicants found: {expected_applicants_found} | Actual applications found: {actual_applicants_found}'
        if actual_applicants_found != expected_applicants_found:
            logging.error(applicants_found_validation)
        else:
            logging.info(applicants_found_validation)

        assert actual_applicants_found == expected_applicants_found, applicants_found_validation
    else:
        logging.info('No additional verification done for a non-200 status code')


search_by_street_tests = [
    (
        {'payload': {'street': 'Taylor'}},
        {'expected_results': {'status_code': 200, 'applicants_found': 1}},
        {'test_description': 'Partial street match'}
    ),
    (
        {'payload': {'street': '101 CALIFORNIA ST'}},
        {'expected_results': {'status_code': 200, 'applicants_found': 2}},
        {'test_description': 'Full street match'},
    ),
    (
        {'payload': {'street': 'California'}},
        {'expected_results': {'status_code': 200, 'applicants_found': 17}},
        {'test_description': 'Partial name match with multiple applications'},
    ),
    (
        {'payload': {'street': 'Does not exist', }},
        {'expected_results': {'status_code': 200, 'applicants_found': 0}},
        {'test_description': 'No applicant found'},
    ),
    (
        {'payload': {}},
        {'expected_results': {'status_code': 400, 'applicants_found': 0}},
        {'test_description': 'No street supplied in payload'},
    )
]


@pytest.mark.parametrize('test_data', search_by_street_tests,
                         ids=[search_by_street_tests[0][2]['test_description'], search_by_street_tests[1][2]['test_description'], search_by_street_tests[2][2]['test_description'],
                              search_by_street_tests[3][2]['test_description'], search_by_street_tests[4][2]['test_description']])
def test_search_by_street(test_data: list):
    payload = test_data[0]['payload']
    expected_status_code = test_data[1]['expected_results']['status_code']
    expected_applicants_found = test_data[1]['expected_results']['applicants_found']

    response = get_search_by_street(payload)
    actual_status_code = response.status_code
    actual_applicants_found = len(response.json())

    status_code_validation = f'Expected status code: {expected_status_code} | Actual status code: {actual_status_code}'
    if actual_status_code != expected_status_code:
        logging.error(status_code_validation)
    else:
        logging.info(status_code_validation)

    assert actual_status_code == expected_status_code, status_code_validation

    if actual_status_code == 200:
        applicants_found_validation = f'Expected applicants found: {expected_applicants_found} | Actual applications found: {actual_applicants_found}'
        if actual_applicants_found != expected_applicants_found:
            logging.error(applicants_found_validation)
        else:
            logging.info(applicants_found_validation)

        assert actual_applicants_found == expected_applicants_found, applicants_found_validation
    else:
        logging.info('No additional verification done for a non-200 status code')


# Note: The number of returned applicants is always 5 (line 51 in MobileFoodFacilitiesController.cs), unless there are < 5 Applicants with a matching status
# Extra important to verify the actual Applicants returned since the number of items returned is usually the same
nearest_food_trucks_tests = [
    (
        {'payload': {'latitude': 37, 'longitude': -122}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': 'Coordinates to 0 decimals'}
    ),
    (
        {'payload': {'latitude': 37.7, 'longitude': -122.4}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': 'Coordinates to 1 decimals'}
    ),
    (
        {'payload': {'latitude': 37.762, 'longitude': -122.427}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': 'Coordinates to 3 decimals'}
    ),
    (
        {'payload': {'latitude': 37.805885350100986, 'longitude': -122.41594524663745}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': 'Coordinates to 15 decimals'}
    ),
    (
        {'payload': {'longitude': -122.427}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': 'No latitude specified'}
    ),
    (
        {'payload': {'latitude': 37.762}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': 'No longitude specified'}
    ),
    (
        {'payload': {}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': 'No latitude or longitude specified'}
    ),
    (
        # Should consider if status should be validated by Food Trucks API
        {'payload': {'latitude': 37.762, 'longitude': -122.427, 'status': ApplicantStatus.APPROVED.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': f'{ApplicantStatus.APPROVED.value} status explicitly set'},
    ),
    (
        # Should consider if status should be validated by Food Trucks API
        {'payload': {'latitude': 37.762, 'longitude': -122.427, 'status': ApplicantStatus.REQUESTED.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': f'{ApplicantStatus.REQUESTED.value} status explicitly set'},
    ),
    (
        # Should consider if status should be validated by Food Trucks API
        {'payload': {'latitude': 37.762, 'longitude': -122.427, 'status': ApplicantStatus.EXPIRED.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': f'{ApplicantStatus.EXPIRED.value} status explicitly set'},
    )
    ,
    (
        # Should consider if status should be validated by Food Trucks API
        {'payload': {'latitude': 37.762, 'longitude': -122.427, 'status': ApplicantStatus.ISSUED.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 2}},
        {'test_description': f'{ApplicantStatus.ISSUED.value} status explicitly set'},
    ),
    (
        # Should consider if status should be validated by Food Trucks API
        {'payload': {'latitude': 37.762, 'longitude': -122.427, 'status': ApplicantStatus.SUSPEND.value}},
        {'expected_results': {'status_code': 200, 'applicants_found': 5}},
        {'test_description': f'{ApplicantStatus.SUSPEND.value} status explicitly set'},
    ),
    (
        # Should consider if status should be validated by Food Trucks API
        {'payload': {'latitude': 37.762, 'longitude': -122.427, 'status': 'Does not exist'}},
        {'expected_results': {'status_code': 200, 'applicants_found': 0}},
        {'test_description': 'Invalid status supplied'},
    )
]


@pytest.mark.parametrize('test_data', nearest_food_trucks_tests,
                         ids=[nearest_food_trucks_tests[0][2]['test_description'], nearest_food_trucks_tests[1][2]['test_description'],
                              nearest_food_trucks_tests[2][2]['test_description'], nearest_food_trucks_tests[3][2]['test_description'],
                              nearest_food_trucks_tests[4][2]['test_description'], nearest_food_trucks_tests[5][2]['test_description'],
                              nearest_food_trucks_tests[6][2]['test_description'], nearest_food_trucks_tests[7][2]['test_description'],
                              nearest_food_trucks_tests[8][2]['test_description'], nearest_food_trucks_tests[9][2]['test_description'],
                              nearest_food_trucks_tests[10][2]['test_description'], nearest_food_trucks_tests[11][2]['test_description'],
                              nearest_food_trucks_tests[12][2]['test_description']])
def test_nearest_food_trucks(test_data: list):
    payload = test_data[0]['payload']
    expected_status_code = test_data[1]['expected_results']['status_code']
    expected_applicants_found = test_data[1]['expected_results']['applicants_found']

    response = get_nearest_food_trucks(payload)
    actual_status_code = response.status_code
    actual_applicants_found = len(response.json())

    status_code_validation = f'Expected status code: {expected_status_code} | Actual status code: {actual_status_code}'
    if actual_status_code != expected_status_code:
        logging.error(status_code_validation)
    else:
        logging.info(status_code_validation)

    assert actual_status_code == expected_status_code, status_code_validation

    if actual_status_code == 200:
        applicants_found_validation = f'Expected applicants found: {expected_applicants_found} | Actual applications found: {actual_applicants_found}'
        if actual_applicants_found != expected_applicants_found:
            logging.error(applicants_found_validation)
        else:
            logging.info(applicants_found_validation)

        assert actual_applicants_found == expected_applicants_found, applicants_found_validation
    else:
        logging.info('No additional verification done for a non-200 status code')
