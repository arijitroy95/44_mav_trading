import os


stock_name_page_url = "https://in.finance.yahoo.com/quote/%5ENSEI/components/"
stock_data_interval = "1d"
stock_data_period = "6mo"
plot_type = "charles"
image_files_dir = "images"
os.makedirs(image_files_dir, exist_ok=True)
moving_averages = (30, 44)
