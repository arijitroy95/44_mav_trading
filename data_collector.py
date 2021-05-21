import yfinance as yf
import requests
from bs4 import BeautifulSoup
import mplfinance as plt
import constants


def get_name(table_row_obj):
    data_in_row = table_row_obj.find_all("td")
    if data_in_row:
        stock_name = data_in_row[0].text
        if stock_name.endswith("NS"):
            return stock_name
    return ""


def read_stock_from_html(text):
    soup_obj = BeautifulSoup(text, features="lxml")
    all_table_rows = soup_obj.find_all("tr")
    stock_names = list(filter(lambda x: x if x else None, map(lambda x: get_name(x), all_table_rows)))
    return stock_names


def stock_name_collector():
    stock_names = list()
    name_page_url = constants.stock_name_page_url
    response = requests.get(name_page_url)
    if response.status_code == 200:
        stock_names = read_stock_from_html(response.text)
    return stock_names


def get_stock_data(stock_names):
    if not stock_names:
        return None
    data = yf.download(
        tickers=stock_names,
        period=constants.stock_data_period,
        interval=constants.stock_data_interval,
        group_by="ticker",
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None
    )
    return data


def make_candle_plot(all_stock_data, stock_names):
    for stock_name in stock_names:
        stock_data = all_stock_data[stock_name]
        if stock_data.isnull().values.any():
            print(f"{stock_name} has nan value skipping this.")
            continue
        name = f'{stock_name.replace(".NS", "")}'
        plt.plot(
            stock_data,
            type="candle",
            style='charles',
            title=name,
            ylabel='Price',
            mav=constants.moving_averages,
            savefig=f"{constants.image_files_dir}/{name}.png"
        )


def collected_data_validator(stock_data):
    if isinstance(stock_data, list):
        raise TypeError("Data Collection Failed")


def main():
    retry_flag, retry_count = True, 10
    stock_names = list()
    stock_data = list()
    while retry_flag and retry_count:
        stock_names = stock_name_collector()  # get top 30 NSE stock names from yahoo finance
        stock_data = get_stock_data(stock_names)
        try:
            collected_data_validator(stock_data)
            retry_flag = False
        except TypeError:
            pass
        finally:
            retry_count -= 1
    if retry_flag:
        exit(1)
    make_candle_plot(stock_data, stock_names)


if __name__ == '__main__':
    main()
