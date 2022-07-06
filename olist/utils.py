import re
import pandas as pd
from olist.data import Olist

def remove_prefix(text):
    '''
    Remove prefix to return a generic column name
    '''
    pattern = '^\w*?_' # ^ = start of string; ? = match the first one only
    return re.findall(pattern, text)[0]


def count_p_location(df,features,group_by):
    '''
    Return number of sellers or customers sorted by either state or zip code
    features= list of columns of interest
    group_by= either "state" or "zip_code".
    '''
    new_df = df[features]\
                        .groupby(by= features[0])\
                        .count()\
                        .sort_values(by= features[1], ascending= False)

    # new column names:
    new_column_names = {feature : feature.replace(remove_prefix(feature),"")
                        for feature in features}
    new_df.rename(columns= new_column_names, inplace = True)

    if group_by == "state":
        # Create percentage column for annotation on barplot
        new_df['Percentage'] = new_df.iloc[:,0]/sum(new_df.iloc[:,0]) * 100
        new_df['Percentage'] = new_df['Percentage'].map('{:,.1f}%'.format)

    if group_by == "zip_code":
        geolocation= Olist().get_data()['geolocation']
        geo_by_zip_code = geolocation.groupby('geolocation_zip_code_prefix')\
                                .agg({'geolocation_lat':'mean', 'geolocation_lng': 'mean'})
        new_df = new_df.merge(geo_by_zip_code,
                          how = 'left',
                          left_on = new_df.index,
                          right_on='geolocation_zip_code_prefix')
        new_df.dropna(inplace= True)

    return new_df

def delay_encoder(row):
    '''
    Return 0 if order delivered prior to estimated delivery date
    Return 1 if order was delayed
    '''
    return 0 if row['estimated_delivery_date'] >= row['delivered_date'] else 1
