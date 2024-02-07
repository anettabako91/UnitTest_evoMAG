import unittest

import HtmlTestRunner

from unit_test.test_cart import TestCart
from unit_test.test_filter_and_order import TestFilterandOrder
from unit_test.test_login import TestLogin
from unit_test.test_page_and_title_check import TestPageandTitleCheck
from unit_test.test_search_product import TestSearch


class TestSuite(unittest.TestCase):

        def test_suite(self):
            test_de_rulat = unittest.TestSuite()
            test_de_rulat.addTests([
                unittest.defaultTestLoader.loadTestsFromTestCase(TestCart),
                unittest.defaultTestLoader.loadTestsFromTestCase(TestFilterandOrder),
                unittest.defaultTestLoader.loadTestsFromTestCase(TestLogin),
                unittest.defaultTestLoader.loadTestsFromTestCase(TestPageandTitleCheck),
                unittest.defaultTestLoader.loadTestsFromTestCase(TestSearch)
            ])

            runner = HtmlTestRunner.HTMLTestRunner(
                combine_reports=True,
                report_title='TestReport',
                report_name='Smoke Test Result'
            )

            runner.run(test_de_rulat)