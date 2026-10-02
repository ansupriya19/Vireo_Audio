import pandas as pd
from pathlib import Path

def load_all_data(data_dir='.'):
    data_dir = Path(data_dir)
    tickets = pd.read_csv(data_dir / 'tickets.csv', low_memory=False)
    agents = pd.read_csv(data_dir / 'agents.csv', low_memory=False)
    orders = pd.read_csv(data_dir / 'orders.csv', low_memory=False)
    customers = pd.read_csv(data_dir / 'customers.csv', low_memory=False)
    products = pd.read_csv(data_dir / 'products.csv', low_memory=False)
    return tickets, agents, orders, customers, products
