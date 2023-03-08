"""Function(s) for cleaning the data set(s)."""

import pandas as pd
import numpy as np
from final_project_yingyu.data_management.function import naics_2_digit

# def clean_data(data, data_info):
#     """Clean data set.

#     Information on data columns is stored in ``data_management/data_info.yaml``.

#     Args:
#         data (pandas.DataFrame): The data set.
#         data_info (dict): Information on data set stored in data_info.yaml. The
#             following keys can be accessed:
#             - 'outcome': Name of dependent variable column in data
#             - 'outcome_numerical': Name to be given to the numerical version of outcome
#             - 'columns_to_drop': Names of columns that are dropped in data cleaning step
#             - 'categorical_columns': Names of columns that are converted to categorical
#             - 'column_rename_mapping': Old and new names of columns to be renamend,
#                 stored in a dictionary with design: {'old_name': 'new_name'}
#             - 'url': URL to data set

#     Returns:
#         pandas.DataFrame: The cleaned data set.

#     """
#     data = data.drop(columns=data_info["columns_to_drop"])
#     data = data.dropna()
#     for cat_col in data_info["categorical_columns"]:
#         data[cat_col] = data[cat_col].astype("category")
#     data = data.rename(columns=data_info["column_rename_mapping"])

#     numerical_outcome = pd.Categorical(data[data_info["outcome"]]).codes
#     data[data_info["outcome_numerical"]] = numerical_outcome

#     return data

def clean_data(sic_naics, data, io_naics,bds, io):
    """Clean datasets."""
    naics_sic_share = clean_emp(sic_naics, data)
    io_naics = clean_io_naics(io_naics)
    IO_naics_2_digit = io_2_digit(naics_2_digit,io_naics)
    naics_sic_io = merge_io_naics(naics_sic_share,IO_naics_2_digit)
    bds_naics = merge_bds(bds,naics_sic_io)
    select_col=clean_io(io)
    weights = cons_inv_shares()
    weights = merge_io(io,select_col,bds_naics,weights)
    return IO_naics_2_digit, naics_sic_io, weights
    
    
    

# clean emp data to get naics_sic 
def clean_emp(sic_naics, data):
    """_summary_

    Args:
        sic_naics (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    sic_naics.set_index(['naics super','Measure'],inplace=True)
    sic_naics = sic_naics.applymap(lambda x: x if x>= 0 else 0)
    sic_naics_shares = sic_naics.xs('Percent',level=1)
    sic_naics_shares = sic_naics_shares.reset_index().rename(columns={'index':'naics super'})
    cols = sic_naics_shares.columns.values[1:]
    sic_naics_shares=pd.melt(sic_naics_shares,id_vars=['naics super'],value_vars=cols,var_name='sic',value_name='share')
    sic_naics_shares['naics super'].unique()
    naics_2_digit_super = {'Education and health services':'Education and health services' , 
            'Leisure and hospitality': 'Leisure and hospitality',
            'Mining and logging':'Mining and logging',
            'Utilities' : 'Trade, transportation, and utilities',
            'Construction' :  'Construction',
            'Wholesale Trade': 'Trade, transportation, and utilities',
            'Information':'Information',
            'Other services, except Public Administration':'Other services',
            'Other services':'Other services',          
            'Manufacturing':'Manufacturing',
            'Retail Trade': 'Trade, transportation, and utilities',
            'Transportation and Warehousing':'Trade, transportation, and utilities',
            'Trade, transportation, and utilities':'Trade, transportation, and utilities',           
            'Financial activities':'Financial activities',
            'Professional and business services':'Professional and business services',
            'Government':'Government'}
    data['naics super'] = data.naics.map(naics_2_digit_super)
    g = lambda x: data[data.naics==x]['emp'].values[0]
    naics_super_emp = data['naics super'].map(g)
    data['naics super emp'] = naics_super_emp
    data['emp share'] = data['emp']/data['naics super emp']
    sic_naics_shares = sic_naics_shares.merge(data,on='naics super',how='left')
    sic_naics_share = sic_naics_shares.rename(columns={'share':'sic share', 'emp share': 'naics share'}).drop(
    ['emp','naics super emp'],axis=1)
    sic_naics_share['share'] = sic_naics_share['sic share']/100*sic_naics_share['naics share']
    naics_sic_share  = sic_naics_share.groupby(['sic','naics'])['share'].sum().reset_index()
    naics_sic_share.groupby('naics').sum(numeric_only=True)
    return naics_sic_share
    
# clean io_nacis

def clean_io_naics(io_naics):
    """_summary_

    Args:
        io_naics (_type_): _description_

    Returns:
        _type_: _description_
    """
    io_naics = io_naics.drop('notes',axis=1)
    io_naics = io_naics.dropna(how='all')
    io_index = io_naics.index.values
    for i in range(len(io_index)):
        if pd.isna(io_naics.loc[io_index[i]]['2-digit-IO']):
            io_naics.loc[io_index[i]]['2-digit-IO'] = io_naics.loc[io_index[i-1]]['2-digit-IO']  
    io_naics_index = io_naics.index.values
    m = [io_naics.loc[io_naics_index[0]]['2-digit-name']]
    for i in range(1,len(io_naics_index)):
        if io_naics.loc[io_naics_index[i]]['2-digit-IO'] == io_naics.loc[io_naics_index[i-1]]['2-digit-IO']:
            m.append(m[i-1])
    else:
        m.append(io_naics.loc[io_naics_index[i]]['2-digit-name'])
    io_naics['2-digit-name']=pd.DataFrame(index=io_naics_index,data=m)
    io_naics = io_naics.dropna(subset=['Mult-digit-name','naics'])
    return io_naics

  

  
def io_2_digit(naics_2_digit,io_naics):
    """_summary_

    Args:
        naics_2_digit (_type_): _description_
        io_naics (_type_): _description_

    Returns:
        _type_: _description_
    """
    IO_naics_2_digit = io_naics.groupby('2-digit-IO').apply(naics_2_digit)
    IO_naics_2_digit = IO_naics_2_digit.reset_index().rename(columns={'2-digit-IO':'IOCode',0:'Naics code'})
    IO_naics_2_digit['IOCode'] = IO_naics_2_digit['IOCode'].astype('str')
    io_naics_dict = {'6':'Education and health services',
                '7': 'Leisure and hospitality',
                '11':'Agriculture','21':'Mining and logging',
                '22': 'Utilities','23':'Construction', '42':'Wholesale Trade',
                '51':'Information','81':'Other services',
                '31G':'Manufacturing','44RT':'Retail Trade',
                '48TW':'Transportation and Warehousing',
                'FIRE':'Financial activities','G':'Government',
                'PROF':'Professional and business services'}
    io_naics_2_digit_names = IO_naics_2_digit['IOCode'].map(io_naics_dict)
    IO_naics_2_digit['naics'] = io_naics_2_digit_names
    return IO_naics_2_digit

    
# merge io_naics with naics_sic to naics_sic_io
def merge_io_naics(naics_sic_share,IO_naics_2_digit):
    """_summary_

    Args:
        naics_sic_share (_type_): _description_
        IO_naics_2_digit (_type_): _description_

    Returns:
        _type_: _description_
    """
    naics_sic_io = naics_sic_share.merge(IO_naics_2_digit,on='naics',how='inner')
    return naics_sic_io

# merge bds to naics-io-sic
def merge_bds(bds,naics_sic_io):
    """_summary_

    Args:
        bds (_type_): _description_
        naics_sic_io (_type_): _description_

    Returns:
        _type_: _description_
    """
    select_on = ((bds.fage4=='Economy Wide') & (bds.ifsize=='m') & (bds.fsize=='Economy Wide'))
    bds_try = bds[select_on].merge(naics_sic_io,on='sic',how='left')
    cols = ['emp', 'estabs', 'estabs_entry','estabs_entry_rate','estabs_exit','estabs_exit_rate',
       'firmdeath_emp', 'firmdeath_estabs',
       'firmdeath_firms', 'firms', 'job_creation',
       'job_creation_births', 'job_creation_continuers',
        'job_destruction',
       'job_destruction_continuer', 'job_destruction_deaths']
    bds_try[cols] = bds_try[cols].astype(float).multiply(bds_try.share,axis=0)
    bds_naics = bds_try.groupby(['IOCode','naics','time'])[cols].sum().reset_index()
    bds_naics.rename(columns={'time':'year'},inplace=True)
    return bds_naics

# clean io
def clean_io(io,bds_try):
    """_summary_

    Args:
        io (_type_): _description_
        bds_try (_type_): _description_

    Returns:
        _type_: _description_
    """
    io.rename(columns={'RowCode':'IOCode','Year':'year'},inplace=True)
    industries = list(bds_try.IOCode.unique()[1:])+['V001','TOTINDOUT']
    industries_extended = list(industries)+['F010','F020','F030','TOTCOMOUT']
    select_col = io.ColCode.map(lambda x: x in industries_extended)
    return select_col

def cons_inv_shares(group):
    """_summary_

    Args:
        group (_type_): _description_

    Returns:
        _type_: _description_
    """
    industries = np.setdiff1d(group.IOCode.unique(),['TOTINDOUT','V001'])
    group.set_index('IOCode',inplace=True)
    B = group.div(group.loc['TOTINDOUT']).loc[industries][industries]
    omega = np.linalg.inv((np.identity(len(B))-B))
    C =group.loc[industries]['F010']/group.loc['TOTINDOUT']['F010']
    X =group.loc[industries]['F020']/group.loc['TOTINDOUT']['F010']
    labor = group.loc[industries]['emp'].values/group.loc['TOTINDOUT'][industries].values
    # calculate consumption weights
    consumption_weights = np.diag(labor).dot(omega).dot(C)
    # normalize weights to sum to 1
    consumption_weights = consumption_weights/consumption_weights.sum() 
    # calcuate the investment weights
    investment_weights = np.diag(labor).dot(omega).dot(X)
    # normalize weights to sum to 1
    investment_weights=investment_weights/investment_weights.sum()
    # return calculations
    weights = pd.DataFrame({'IOCode':industries,
                            'consumption weights':consumption_weights,
                            'investment weights':investment_weights})
    return weights  

# merge bds and io, and calculate weights
def merge_io(io,select,select_col,bds_naics,weights):
    """_summary_

    Args:
        io (_type_): _description_
        select (_type_): _description_
        select_col (_type_): _description_
        bds_naics (_type_): _description_
        weights (_type_): _description_

    Returns:
        _type_: _description_
    """
    io = io[select & select_col].pivot_table(index=['year','IOCode'],columns='ColCode',values='DataValue').fillna(0).reset_index()
    bds_io =io.merge(bds_naics[['IOCode','year','emp']],on=['IOCode','year'],how='left')
    weights = bds_io.groupby('year').apply(cons_inv_shares).reset_index().drop('level_1',axis=1)
    return weights
