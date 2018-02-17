from ...storage.storage import Storage
from ...storage.backend import BackendBase
from ..fixture import TestClassBase, testmethod
from ..mock import Mock

class StorageTests(TestClassBase):

    @testmethod
    def T_store_price_points_WhenNoPrices_NeverCallBackend(self):
        mock_backend = Mock(BackendBase)
        mock_backend.setup("insert").returns(None)
        storage = Storage(mock_backend.object())

        # act
        storage.store_price_points([])

        # assert
        assert not mock_backend.verify("insert").was_called()

    @testmethod
    def T_store_price_points_WhenMalformedPrices_CallBackendOnce(self):
        mock_backend = Mock(BackendBase)
        mock_backend.setup("insert").returns(None)
        storage = Storage(mock_backend.object())
        malformed_items = [{"malformed": 1}, {"malformed": 2}]
        malformed_table = "price_point_error"

        # act
        storage.store_price_points(malformed_items)

        # assert
        assert mock_backend.verify("insert").was_called(
                arguments={"table_name": malformed_table,
                    "items": malformed_items},
                times=1)

    @testmethod
    def T_store_price_points_WhenWellFormedPrices_CallBackendOnce(self):
        mock_backend = Mock(BackendBase)
        mock_backend.setup("insert").returns(None)
        storage = Storage(mock_backend.object())
        well_formed_items = [{
            "id": 86905,
            "whitelisted": False,
            "buys": {
              "quantity": 80,
              "unit_price": 2090009
            },
            "sells": {
              "quantity": 10,
              "unit_price": 2980000
            }
        }]
        well_formed_table = "price_point"

        # act
        storage.store_price_points(well_formed_items)

        # assert
        assert mock_backend.verify("insert").was_called(
                arguments={"table_name": well_formed_table,
                    "items": well_formed_items},
                times=1)

    @testmethod
    def T_store_price_points_WhenMalWellPrices_CallBackendOnceEach(self):
        mock_backend = Mock(BackendBase)
        mock_backend.setup("insert").returns(None)
        storage = Storage(mock_backend.object())
        well_formed_item = {
            "id": 86905,
            "whitelisted": False,
            "buys": {
              "quantity": 80,
              "unit_price": 2090009
            },
            "sells": {
              "quantity": 10,
              "unit_price": 2980000
            }
        }
        malformed_item = {"another_malformed_price": "malformed"}
        well_formed_table = "price_point"
        malformed_table = "price_point_error"

        # act
        storage.store_price_points([well_formed_item, malformed_item])

        # assert
        assert mock_backend.verify("insert").was_called(
                arguments={"table_name": well_formed_table,
                    "items": [well_formed_item]},
                times=1)

        assert mock_backend.verify("insert").was_called(
                arguments={"table_name": malformed_table,
                    "items": [malformed_item]},
                times=1)
