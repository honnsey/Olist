import seaborn as sns
import matplotlib.pyplot as plt
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
    for patch, percentage in zip(plot.patches, df.iloc[:,2]):   # for each patch/bar
        x = patch.get_width() + 20                              # offset 20 from end of bar
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

def double_plot(df,**kwargs):
    '''
    Return number of orders in barplot and order value by the chosen category (day of week or month) on the same plot
    Input dataframe includes three columns in the order of [Month/Day of Week as index, 'order_id', 'payment_value']
    kwargs are key word arguments for barplot
    '''
    # ###########################
    # "number of orders" barplot
    #############################
    plot = sns.barplot(x= df.index,
                   y = 'order_id',
                   data = df,
                   **kwargs)
    # plot2.set(title='Sales Over Time')
    plot.set_ylabel("Number of Orders")
    plot.set_ylim(0,df['order_id'].max()*2)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45);

    # ###########################
    # "Order Value" Line Plot
    #############################
    ax2 = plt.twinx()
    sns.lineplot(data=df.payment_value,
                 color="grey", linestyle= '-.', marker= "o", # use "marker =" not "markers = "
                 ax=ax2)
    ax2.grid(False)
    ax2.set_ylim(0e6,df['payment_value'].max()*1.1)
    ax2.set_ylabel('Order Value ($)');

if __name__ == '__main__':
    print('visualisation')
