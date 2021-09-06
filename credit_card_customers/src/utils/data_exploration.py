import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OrdinalEncoder

def filter_df_by_value(dataframe, col, value, length):
    filtered_df = dataframe[dataframe[col] == value][:length]
    return filtered_df


def ordinal_encode(dataframe):
    
    for i in dataframe.columns:
        if type(dataframe[i][0]) == str:
            col_values = [x for x in dataframe[i].unique()]
            oe = OrdinalEncoder(categories= [col_values])
            dataframe[i] = oe.fit_transform(dataframe[[i]])

    return dataframe


def compare_categorical_data_percentages(df1, df2):
    
    for i in df1.columns:
        if type(df1[i][0])== str:
            df1_value = []
            df1_count = []
            df1_pct = []
            df2_value = []
            df2_count = []
            df2_pct = []
            for j in df1[i].unique():
                df1_value.append(j)
                df1_count.append(df1[df1[i] == j][i].value_counts()[0])
                df1_pct.append(df1[df1[i] == j][i].value_counts()[0] / len(df1) * 100)
            for k in df2[i].unique():
                df2_value.append(k)
                df2_count.append(df2[df2[i] == k][i].value_counts()[0])
                df2_pct.append(df2[df2[i] == k][i].value_counts()[0] / len(df2) * 100)
            to_plot1 = pd.DataFrame({'value' :df1_value, 'count': df1_count, 'percentage': df1_pct})
            to_plot2 = pd.DataFrame({'value' :df2_value, 'count': df2_count, 'percentage': df2_pct})

            print(f'{i} percentage comparison:')
            #print(to_plot1)
            #print(to_plot2)
            

            #plt.pie(to_plot1['count'], labels= to_plot1['value'])
            #plt.pie(to_plot2['count'], labels= to_plot2['value'])


            
            fig, (ax1, ax2) = plt.subplots(1, 2, sharey= True)
            plt.suptitle(f'{i} percentage comparison')
            ax1.pie(to_plot1['count'], labels= to_plot1['value'])
            ax2.pie(to_plot2['count'], labels = to_plot2['value'])
            plt.show()
            
        else:
            print(f'{i} is not a string column')
    print('all done')
    return

