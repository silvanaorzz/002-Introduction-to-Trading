import numpy as np

def calmar_ratio(portfolio_series):
    peak = portfolio_series.cummax()
    drawdown = (portfolio_series - peak) / peak
    max_drawdown = drawdown.min()
    start, end = portfolio_series.iloc[0], portfolio_series.iloc[-1]
    cagr = (end / start) - 1
    if max_drawdown == 0:
        return np.nan
    return cagr / abs(max_drawdown)

def calmar_by_year(portfolio_series):
    calmar_table = []
    for year, group in portfolio_series.groupby(portfolio_series.index.year):
        if len(group) < 10:
            continue
        peak = group.cummax()
        drawdown = (group - peak) / peak
        max_dd = drawdown.min()
        cagr = (group.iloc[-1]/group.iloc[0]) - 1
        calmar_table.append({'Year': year, 'Calmar Ratio': cagr/abs(max_dd) if max_dd !=0 else np.nan})
    import pandas as pd
    df = pd.DataFrame(calmar_table).set_index('Year')
    return df
