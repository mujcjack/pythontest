import pandas as pd
from datetime import datetime

input_path='C:/Working/python_Test/DS Assigment/DS Assigment/corp_pfd.dif'
reference_field='C:/Working/python_Test/DS Assigment/DS Assigment/reference_fileds.csv'
reference_securities='C:/Working/python_Test/DS Assigment/DS Assigment/reference_securities.csv'


def read_file(file_path):
    with open(file_path,'rb') as f:
        corp_pfd=f.read().decode()
    cols_names=corp_pfd.split('START-OF-FIELDS')[1].split('END-OF-FIELDS')[0].split('\r\n')
    cols=[]
    for c in cols_names:
        if (c =='') or ('#' in c):
            continue
        else:
            cols.append(c)

    data=corp_pfd.split('START-OF-DATA')[1].split('END-OF-DATA')[0].strip().split('\r\n')
    for i in range(len(data)):
        data[i]=data[i].split('|')[:-1]

    df=pd.DataFrame(data,columns=cols)
    return df


def col_filter(df,refer):
    reference_field=pd.read_csv(refer)
    target_cols=reference_field['field'].tolist()
    new_cols=[]
    for c in df.columns:
        if c in target_cols:
            new_cols.append(c)
    output=df[new_cols]
    return output

def get_new_securities (df, refer):
    reference_file=pd.read_csv(refer)
    output=pd.merge(left=df,right=reference_file['id_bb_global'],how='outer',
                    left_on='ID_BB_GLOBAL',right_on='id_bb_global')
    output=output.loc[(output['id_bb_global'].isna())&(~output['ID_BB_GLOBAL'].isnull())]
    
    output_cols=[c.upper() for c in reference_file.columns]
    output=output[output_cols]
    output.dropna(inplace=True)
    output.to_csv('new_securities.csv',index=False)
    #print(output)

def get_securities_data(df):
    output=df.melt(id_vars='ID_BB_GLOBAL',var_name='FIELD',value_name='VALUE')
    output['SOURCE']='corp_pfd.dif'
    now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output['TSTAMP']=now
    output.to_csv('security_data.csv',index=False,sep=',')
    #print(output)

file=read_file(file_path=input_path)
file_df=pd.DataFrame(file)

references=col_filter(df=file_df, refer=reference_field)
references_df=pd.DataFrame(references)

new_securities=get_new_securities(df=references_df,refer=reference_securities) 
securities_data=get_securities_data(df=references_df)





