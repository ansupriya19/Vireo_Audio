import pandas as pd

def clean_tickets(tickets_df, prefer_helpdesk_only=True):
    df = tickets_df.copy()
    df['refund_amount_inr'] = pd.to_numeric(df['refund_amount_inr'], errors='coerce')
    
    if prefer_helpdesk_only:
        df = df[df['source_system'] == 'helpdesk'].copy()
        out = df.reset_index(drop=True)
    else:
        keep_rows = []
        for tid, group in df.groupby('ticket_id'):
            if len(group) == 1:
                keep_rows.append(group.iloc[0])
            else:
                hd = group[group['source_system'] == 'helpdesk']
                if len(hd) > 0:
                    keep_rows.append(hd.iloc[0])
                else:
                    keep_rows.append(group.iloc[0])
        out = pd.DataFrame(keep_rows).reset_index(drop=True)
    out['created_at'] = pd.to_datetime(out['created_at'], errors='coerce')
    out['resolved_at'] = pd.to_datetime(out['resolved_at'], errors='coerce')
    if 'created_at' in out.columns:
        out['month'] = out['created_at'].dt.to_period('M')
        out['month_str'] = out['created_at'].dt.strftime('%Y-%m')
        out['quarter'] = out['created_at'].dt.to_period('Q')
        out['quarter_str'] = out['quarter'].astype(str)
    return out
