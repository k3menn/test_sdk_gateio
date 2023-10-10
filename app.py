from utils import logger


from src.client import GateIoProfile
from static.text import currency_balance_text, currency_pair_text, currency_pair_order_text, amount_order_text, price_order_text, order_side_text


def start_module(profile: GateIoProfile, module: int):
    if module == 1:
        logger.info('start : get_currency_rate')
        currency_pair = str(input(currency_pair_text))
        result = profile.get_currency_rate(currency_pair=currency_pair)


    elif module == 2:
        logger.info('start : get_balance')
        currency = str(input(currency_balance_text))
        result = profile.get_balance(currency=currency)

    elif module == 3:
        logger.info('start : get_list_of_orders')
        result = profile.get_list_of_orders()

    elif module == 4:
        logger.info('start : place_limit_order')
        currency_pair = str(input(currency_pair_order_text))
        amount = str(input(amount_order_text))
        side = str(input(order_side_text))
        price = str(input(price_order_text))
        result = profile.place_limit_order(currency_pair, side, amount, price)

    elif module == 5:
        logger.info('start : cancel_active_order')
        currency_pair = str(input(currency_pair_order_text))
        side = str(input(order_side_text))
        result = profile.cancel_active_orders(currency_pair, side)

    




if __name__ == "__main__":

    MODULE = int(input('''
MODULE:
1.  get_currency_rate
2.  get_balance
3.  get_list_of_orders
4.  place_limit_order
5.  cancel_active_orders

Выберите модуль (1 - 5) : '''))

    if MODULE in [1, 2, 3, 4, 5]:
        start_module(GateIoProfile(), MODULE)
    else:
        logger.warning('Вы ввели модуль, которого не существует. Перезапустите и попробуйте снова.')

    