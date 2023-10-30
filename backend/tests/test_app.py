import unittest
import sys
sys.path.append('../')
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign in to Blue Surf', response.data)

# Made by Kirti Mehra
# Unit test for the Date-Based landing page event filter in order to test event filtering between specific dates
# Backend to filter by date is not fully completed; may need to amend this test with appropriate class/methods later
# This code assumes the existence of a DateFilter class with a method filter_events_by_date that filters events based on a date range
# Must replace the placeholder DateFilter with the actual class name, and implement the filter_events_by_date method
        
    def test_filter_events_between_dates(self):
        # Create an instance of EventFilter
        date_filter = DateFilter()

        # Test data examples
        # We can add more event dates
        test_events = [
            {'date': '2023-12-20'},
            {'date': '2023-12-21'},
            {'date': '2023-12-22'},
        ]

        # Date range for filtering
        start_date = '2023-12-20'
        end_date = '2023-12-22'

        # Call the filter_events method with the test data
        filteredbydate = date_filter.filter_events_by_date(start_date, end_date, test_events)

        # Assertion for events falling within the specified date range
        self.assertEqual(len(filteredbydate), 2, "Expected number of events between the specified dates")

if __name__ == '__main__':
    unittest.main()





