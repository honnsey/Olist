import seaborn as sns
import pandas as pd
import folium
import folium.plugins as plugins


def plot_by_state(df, **kwargs):
    '''
    Return seaborn barplot of number of sellers/customers in each state,
    with annotation in percentage.
    Input = processed df containing zip code lat long and number of sellers or customers
    kwargs for seaborn barplot
    '''
    sns.set(rc={'figure.figsize':(16,8)})
    plot = sns.barplot(x= df.iloc[:,1], y = df.iloc[:,0],
                       data= df,
                       **kwargs
                       )

    y = 0
    for patch, percentage in zip(plot.patches, df.iloc[:,2]):
        x = patch.get_width() + 20
        plot.annotate(percentage,(x,y), verticalalignment= 'center')
        y += 1
    return plot

def plot_map(df,**kwargs):
    '''
    Return map with locations of sellers or customer by zip_code
    kwargs = options for folium.Icon
    '''
    defaultKwargs = { 'color': "red", 'icon': "flag"}
    kwargs = { **defaultKwargs, **kwargs }

    # Initiate blank map
    map = folium.Map(location=[df['geolocation_lat'].mean(),
                               df['geolocation_lng'].mean()],
                     zoom_start=5,
                     control_scale=True)

    # Plot locations using markers
    for i, row in df.iterrows():
        folium.Marker(location=[row.geolocation_lat, row.geolocation_lng],
                        popup=row.zip_code_prefix,
                        icon=folium.Icon(**kwargs)
                        ).add_to(map)
    return map

def plot_cluster(df):
    map = folium.Map(location=[df['geolocation_lat'].mean(),
                                df['geolocation_lng'].mean()],
                        zoom_start=5,
                        control_scale=True)
    locations = list(zip(df['geolocation_lat'],
                            df['geolocation_lng']))

    plugins.FastMarkerCluster(data=locations).add_to(map)
    return map

if __name__ == '__main__':
    print('visualisation')
