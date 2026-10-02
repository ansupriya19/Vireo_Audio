import pandas as pd
from pathlib import Path

def generate_summaries(tickets_cleaned, agents_df, output_dir='outputs'):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Monthly refunds by reason code
    refunds = tickets_cleaned[tickets_cleaned['refund_amount_inr'].notna() & (tickets_cleaned['refund_amount_inr'] > 0)].copy()
    refunds['month_str'] = refunds['created_at'].dt.strftime('%Y-%m') if 'created_at' in refunds else ''
    
    # By reason code monthly
    by_reason_month = refunds.groupby(['month_str', 'refund_reason_code'])['refund_amount_inr'].agg(['sum', 'count']).reset_index()
    by_reason_month = by_reason_month.rename(columns={'sum': 'refund_amount_inr', 'count': 'ticket_count'})
    by_reason_month.to_csv(output_dir / 'refunds_by_reason_monthly.csv', index=False)
    
    # By agent monthly
    by_agent_month = refunds.groupby(['month_str', 'agent_id'])['refund_amount_inr'].agg(['sum', 'count']).reset_index()
    by_agent_month = by_agent_month.rename(columns={'sum': 'refund_amount_inr', 'count': 'ticket_count'})
    by_agent_month.to_csv(output_dir / 'refunds_by_agent_monthly.csv', index=False)
    
    # Overall by reason
    by_reason = refunds.groupby('refund_reason_code')['refund_amount_inr'].agg(['sum', 'count']).reset_index()
    by_reason.to_csv(output_dir / 'refunds_by_reason.csv', index=False)
    
    # Overall by agent
    by_agent = refunds.groupby('agent_id')['refund_amount_inr'].agg(['sum', 'count']).reset_index()
    by_agent.to_csv(output_dir / 'refunds_by_agent.csv', index=False)
    
    # Enrich with agent names
    if not agents_df.empty:
        agents_enriched = agents_df[['agent_id', 'name', 'team', 'site']].drop_duplicates(subset=['agent_id'])
        by_agent_named = by_agent.merge(agents_enriched, on='agent_id', how='left')
        by_agent_named.to_csv(output_dir / 'refunds_by_agent_named.csv', index=False)
        by_agent_month_named = by_agent_month.merge(agents_enriched, on='agent_id', how='left')
        by_agent_month_named.to_csv(output_dir / 'refunds_by_agent_monthly_named.csv', index=False)
    
    return refunds
