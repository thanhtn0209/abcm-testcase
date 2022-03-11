import unittest
from aolf_client.aofl_http import AoflClient
from config.constant import *
from config.logger import LOGGER
from itertools import product
import uuid
import time

# switch types for switch request
CHANGE_WITH_CHARGE = "change_with_charge"
DOWNGRADE = "downgrade"
UPGRADE = "upgrade"

aofl_client = AoflClient(
    url_prefix=AOFL_API_PREFIX,
    partner=PARTNER,
    aofl_jwt_secret=AOFL_JWT_SECRET,
    aofl_product=AOFL_PRODUCT
)


class TestAolfHttp(unittest.TestCase):
    def _test_for_switch_from_subs_to_longer_subs(self, current_subs, intended_subs):
        """
        This function helps to test the following scenario:
            1. create a subscription
            2. switch to other subscription

        :docs: https://documenter.getpostman.com/view/2064537/TzK15u8o#225e731a-c559-4639-b8dc-06f151eef944
        :param current_subs: the current subscription that consist
        of product_key and period of the one
        :param intended_subs: the subscription that we'd like to switch
        :return:
        """
        LOGGER.info({"message": "starting create subs"})
        galaxy_id = str(uuid.uuid4())
        created_result = aofl_client.aofl_create(
            galaxy_id=galaxy_id,
            product_key=current_subs["product_key"],
            period=current_subs["period"]
        ),
        self.assertEqual(created_result[0], "TRUE")

        time.sleep(3)
        LOGGER.info({"message": "starting switch subs"})
        switched_result = aofl_client.aolf_switch_product(
            galaxy_id=galaxy_id,
            product_key=intended_subs["product_key"],
            old_product_key=current_subs["product_key"],
            period=intended_subs["period"],
            old_period=current_subs["period"],
            switch_type=UPGRADE
        ),
        self.assertEqual(switched_result[0], "TRUE")
        time.sleep(3)

    def test_for_switch_from_subs_to_longer_subs(self):
        """
        This function helps to test the scenario described inside
        _test_for_switch_from_subs_to_longer_subs() function above. The scenario
        carry out on following different cases.
        :return:
        """
        LOGGER.info({"info": "test_for_switch_from_subs_to_longer_subs"})
        subscriptions = [ONE_MONTH_SUBS, HALF_YEAR_SUBS, ONE_YEAR_SUBS]
        cases = [
            pair for
            pair in list(product(subscriptions, subscriptions))
            if pair[0]["period"] < pair[1]["period"]
        ]

        for index, [current_subs, intended_subs] in enumerate(cases):
            with self.subTest(i=index):
                LOGGER.info({"case": index})
                self._test_for_switch_from_subs_to_longer_subs(
                    current_subs,
                    intended_subs
                )

    def _test_for_switch_to_other_package(self, current_package: dict, intended_package: dict):
        """
        This function helps to test the following scenario:
            1. create a package
            2. switch to other package

        :docs: https://documenter.getpostman.com/view/2064537/TzK15u8o#225e731a-c559-4639-b8dc-06f151eef944
        :param current_package: the current package that consist
        of product_key and period of the package
        :param intended_package: the package that we'd like to switch
        :return:
        """
        LOGGER.info({"message": "starting create package"})
        galaxy_id = str(uuid.uuid4())
        created_result = aofl_client.aofl_create(
            galaxy_id=galaxy_id,
            product_key=current_package.get("product_key"),
            period=current_package.get("period")
        ),
        self.assertEqual(created_result[0], "TRUE")
        time.sleep(3)

        LOGGER.info({"message": "starting switch package"})
        switched_result = aofl_client.aolf_switch_product(
            galaxy_id=galaxy_id,
            product_key=intended_package.get("product_key"),
            old_product_key=current_package.get("product_key"),
            period=intended_package.get("period"),
            old_period=current_package.get("period"),
            switch_type=CHANGE_WITH_CHARGE
        ),
        self.assertEqual(switched_result[0], "TRUE")
        time.sleep(3)

    def test_for_switch_to_other_package(self):
        """
        This function helps to test the scenario described inside
        _test_for_switch_other_package() function above. The scenario
        carry out on following different cases.
        :return:
        """
        LOGGER.info({"info": "test_for_switch_from_package_to_longer_package"})
        packages = [
            ONE_MONTH_PACKAGE,
            HALF_YEAR_PACKAGE,
            ONE_YEAR_PACKAGE
        ]
        # if packages = [a, b, c], cases will equal to
        # [[a, b], [b, a], [b, c], [c, b], [a, c], [c, a]]
        cases = [
            pair for
            pair in list(product(packages, packages))
            if pair[0]["period"] != pair[1]["period"]
        ]

        for index, [current_package, intended_package] in enumerate(cases):
            with self.subTest(i=index):
                LOGGER.info({"case": index})
                self._test_for_switch_to_other_package(
                    current_package,
                    intended_package,
                )

    def _test_for_switch_to_the_current_one_itself(self, current_package: dict, intended_package: dict):
        """
        This function helps to test the following scenario:
            1. create a package
            2. switch to itself

        :docs: https://documenter.getpostman.com/view/2064537/TzK15u8o#225e731a-c559-4639-b8dc-06f151eef944
        :param current_package: the current package that consist
        of product_key and period of the package
        :param intended_package: the current one itself.
        :return:
        """
        LOGGER.info({"message": "starting create package"})
        galaxy_id = str(uuid.uuid4())
        created_result = aofl_client.aofl_create(
            galaxy_id=galaxy_id,
            product_key=current_package.get("product_key"),
            period=current_package.get("period")
        ),
        self.assertEqual(created_result[0], "TRUE")
        time.sleep(3)

        LOGGER.info({"message": "starting switch package"})
        switched_result = aofl_client.aolf_switch_product(
            galaxy_id=galaxy_id,
            product_key=intended_package.get("product_key"),
            old_product_key=current_package.get("product_key"),
            period=intended_package.get("period"),
            old_period=current_package.get("period"),
            switch_type=CHANGE_WITH_CHARGE
        ),
        self.assertEqual(switched_result[0], "FALSE")
        time.sleep(3)

    def test_for_switch_to_the_current_one_itself(self):
        LOGGER.info({"info": "test_for_switch_to_the_current_one_itself"})
        packages = [
            ONE_MONTH_PACKAGE,
            HALF_YEAR_PACKAGE,
            ONE_YEAR_PACKAGE
        ]
        # if packages = [a, b, c] => cases = [[a, a], [b, b], [c, c]]
        cases = [[package, package] for package in packages]
        for index, [current_package, intended_package] in enumerate(cases):
            with self.subTest(i=index):
                LOGGER.info({"case": index})
                self._test_for_switch_to_the_current_one_itself(
                    current_package,
                    intended_package
                )


if __name__ == '__main__':
    unittest.main()
