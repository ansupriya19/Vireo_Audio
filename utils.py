import pandas as pd
import os
from datetime import datetime
from pathlib import Path

REASON_CODES = {
    'GW-OTHER': 'Goodwill / Other',
    'DOA-REPL': 'Dead on arrival, refund chosen',
    'LOST-TRANSIT': 'Lost or undelivered',
    'DUP-PAYMENT': 'Duplicate or failed payment',
    'CANCEL': 'Cancellation before dispatch',
    'PRICE-ADJ': 'Price or coupon adjustment',
    'RETURN-QC-OK': 'Return received and passed QC',
    'WTY-BUYBACK': 'Warranty buy-back'
}
