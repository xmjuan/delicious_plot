# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 21:52:33 2021

@author: juanx
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import matplotlib.ticker as mtick
plt.style.context('fivethirtyeight')
sb.set_style('white')

class delicious_stacked_plot():
    
    """ Delicious_plot class for creating stacked bar plot, 
    for visualizing relationship between categorical variables, feature categorical variables, 
    target categorical variables。
    
    Attributes:
    feature_x (string) representing categorical x variables
    target_y (string) representing categorical y variables
    plot_tile (string) representing the customized title of plot
    data (pandas dataframe) representing dataframe passed to plot
    
    """
    
    
    def __init__(self, feature_x, target_y, plot_title, data):
        
        self.feature_x = feature_x
        self.target_y = target_y
        self.title = plot_title
        self.df = pd.DataFrame(data = data)
        
        
    def data_preparation(self):
        
        """ Method to prepare the dataset ready for stacked_plot by using pandas
        
        Args: 
            None
        
        Returns:
            dataframe with calculated proportion of target y in each feature x
        
        """
        # pass attributes
        dframe = self.df
        cat_x = self.feature_x
        cat_y = self.target_y
        
        # aggregate data
        data = dframe.groupby([cat_x, cat_y])[cat_x].count()
        
        # calculate percent and swap index level
        perc_df = pd.DataFrame(data.div(data.sum()).T).swaplevel().unstack().round(decimals=2)
        
        return perc_df
        

    def delicious_stacked(self, annotate = True):
        
        """ Method to visualize data as stacked plot by using matplotlib pyplot library
        
        Args:
            annotate: binary
            
        Returns:
            None
        """
        
        # pass prepared dataset
        prepared_df = self.data_preparation()
        
        # create figure object
        fig, ax = plt.subplots(figsize = (8, 5))
        
        # stacked plot
        prepared_df.plot(kind = 'bar', stacked = True, ax = ax, width = 0.8, alpha = 0.5)
        
        # set legend
        ax.legend(title = self.feature_x,  framealpha = 1,
                  bbox_to_anchor = (1, 0.5), loc = 6)
        
        # set y label
        ax.set_ylabel('Proportion')
        
        # pass title attributes to title
        fig.suptitle(self.title)
        
        # format y ticks
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        # annotate by using ax patches
        if annotate == True:
            for patch in ax.patches:
                width, height = patch.get_width(), patch.get_height()
                x, y = patch.get_xy()
                ax.text(x+width/2, y+height/2,
                        '{:.1%}'.format(height),fontsize=12,
                        horizontalalignment='center',
                        verticalalignment='center')   
        
        plt.show()
        
    def __repr__(self):
        """Function to return introduction of dataset
        """
            
        results = self.data_preparation()
        return 'Data between {} and {}.\n\n{}'.format(self.feature_x, self.target_y, results)
        