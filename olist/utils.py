import re
import pandas as pd

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
    group_by= either "state" or "zip_code"

    '''
    new_df = df[features]\
                        .groupby(by= features[0])\
                        .count()\
                        .sort_values(by= features[1], ascending= False)\
                        .reset_index()

    # new column names:
    new_column_names = {feature : feature.replace(remove_prefix(feature),"")
                        for feature in features}
    new_df.rename(columns= new_column_names, inplace = True)

    if group_by == "state":
        # Create percentage column for annotation on barplot
        new_df['Percentage'] = new_df.iloc[:,1]/sum(new_df.iloc[:,1]) * 100
        new_df['Percentage'] = new_df['Percentage'].map('{:,.1f}%'.format)

    if group_by == "zip_code":
        geo_by_zip_code = geolocation.groupby('geolocation_zip_code_prefix')\
                                .agg({'geolocation_lat':'mean', 'geolocation_lng': 'mean'})
        new_df = new_df.merge(geo_by_zip_code,
                          how = 'left',
                          left_on = 'zip_code_prefix',
                          right_on='geolocation_zip_code_prefix')
    return new_df
