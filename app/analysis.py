import pandas as pd

def coverage_matrix(assets_df):
    pivot = pd.crosstab(assets_df['persona'].fillna('Unknown'),
                        assets_df['funnel_stage'].fillna('Unknown'))
    return pivot

def find_gaps(pivot):
    empties = []
    for p in pivot.index:
        for f in pivot.columns:
            if pivot.loc[p,f] == 0:
                empties.append({"persona":p,"funnel_stage":f})
    return empties

