import pandas as pd

def extract_features(df):
    df['date'] = pd.to_datetime(df['date'])

    total_credit = df[df['type'] == 'CREDIT']['amount'].sum()
    total_debit = df[df['type'] == 'DEBIT']['amount'].sum()

    inflow_count = df[df['type'] == 'CREDIT'].shape[0]
    outflow_count = df[df['type'] == 'DEBIT'].shape[0]

    avg_ticket_size = total_credit / inflow_count if inflow_count > 0 else 0

    cashflow_stability = inflow_count / max(outflow_count, 1)

    return {
        "total_credit": total_credit,
        "total_debit": total_debit,
        "inflow_count": inflow_count,
        "outflow_count": outflow_count,
        "avg_ticket_size": avg_ticket_size,
        "cashflow_stability": cashflow_stability
    }