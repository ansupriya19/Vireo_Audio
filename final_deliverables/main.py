from loaders import load_all_data
from cleaning import clean_tickets
from analysis import generate_summaries
from pathlib import Path

def main():
    data_dir = Path('.')
    tickets, agents, orders, customers, products = load_all_data(data_dir)
    cleaned = clean_tickets(tickets, prefer_helpdesk_only=True)
    refunds = generate_summaries(cleaned, agents, output_dir='outputs')
    out = Path('outputs/summary.txt')
    lines = []
    lines.append(f'Total tickets (helpdesk-cleaned): {len(cleaned)}')
    lines.append(f'Refund tickets: {len(refunds)}')
    lines.append(f'Total refund amount: Rs {refunds["refund_amount_inr"].sum():,.2f}')
    if 'quarter_str' in refunds.columns:
        q = refunds.groupby('quarter_str')['refund_amount_inr'].sum().sort_index()
        for k,v in q.items():
            lines.append(f'{k}: Rs {v:,.2f}')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')

if __name__ == '__main__':
    main()
