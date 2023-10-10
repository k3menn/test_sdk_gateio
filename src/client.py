from utils import logger
from decimal import Decimal as D


import gate_api
from gate_api import ApiClient, Configuration, Order, SpotApi
from gate_api.exceptions import ApiException, GateApiException


from data.config import GATEIO_KEY


class GateIoProfile:
    def __init__(self, configuration=None, api_key=None, api_secret=None,):

        self.api_key = GATEIO_KEY['api_key']
        self.api_secret = GATEIO_KEY['api_secret']
        self.configuration = gate_api.Configuration(
            key=self.api_key,
            secret=self.api_secret,
            host = "https://api.gateio.ws/api/v4"
        ) 
        self.api_client = gate_api.ApiClient(self.configuration)
        self.spot_api = gate_api.SpotApi(self.api_client)
        self.wallet_api = gate_api.WalletApi(self.api_client)


    def get_currency_rate(self, currency_pair: str) -> float:
        """
            Получение текущей стоимости определенной криптовалюты.
        """
        try:
            tickers = self.spot_api.list_tickers(currency_pair=currency_pair)
            assert len(tickers) == 1
            last_price = tickers[0].last
            logger.success(last_price)
            return last_price
        except GateApiException as ex:
            logger.error("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
        except ApiException as e:
            logger.error("Exception when calling SpotApi->list_currency_pairs: %s\n" % e)

    def get_balance(self, currency) -> str:
        """
            Получение информации о балансе на бирже
        """
        try:
            if currency is None:
                currency = 'USDT'
            balance = self.wallet_api.get_total_balance(currency=currency)
            logger.success(balance)
            return balance
        except GateApiException as ex:
            logger.error("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
        except ApiException as e:
            logger.error("Exception when calling SpotApi->list_currency_pairs: %s\n" % e)

    def get_list_of_orders (self) -> str:
        """
            Получение списка активных и последних ордеров 
        """
        page = 1 # int | Page number (optional) (default to 1)
        limit = 100 # int | Maximum number of records returned in one page in each currency pair (optional) (default to 100)

        try:    
            orders = self.spot_api.list_all_open_orders(page=page, limit=limit)
            logger.success(orders)
            return orders
        except GateApiException as ex:
            logger.error("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
        except ApiException as e:
            logger.error("Exception when calling SpotApi->list_currency_pairs: %s\n" % e)

    def place_limit_order(self, currency_pair: str, side: str, amount:str, price: str, ) -> str:
        """
            Размещение лимитного ордера на покупку или продажу определенной криптовалюты.
        """
    
        try:
            order = gate_api.Order(currency_pair=currency_pair, side=side, amount=amount, price=price)
            # Create an order
            create_order_response = self.spot_api.create_order(order)
            logger.success(create_order_response)
            return create_order_response
        except GateApiException as ex:
            logger.error("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
        except ApiException as e:
            logger.error("Exception when calling SpotApi->create_order: %s\n" % e)
        except Exception as er:
            logger.error(f'Error: {er}')


    def cancel_active_orders(self, currency_pair:str, side: str) -> str:
        """
            Отмена всех активных ордеров.
        """
        try:
            cancel_orders_response = self.spot_api.cancel_orders(currency_pair, side=side, account='spot')

            logger.success(cancel_orders_response)
            return cancel_orders_response
        except GateApiException as ex:
            logger.error("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
        except ApiException as e:
            logger.error("Exception when calling SpotApi->create_order: %s\n" % e)
        except Exception as er:
            logger.error(f'Error: {er}')