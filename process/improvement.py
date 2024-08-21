# Improvement Python Library/improvement.py
# Version 0.2
# Updated bar chart function to conditionally display labels
# Added xchart_comparison and mrchart_comparison functions

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import warnings

def bar_chart(df, x_axis_data, y_axis_data, figsize=(15,5), title='', y_label='Value', x_label='', 
              color='tab:blue', x_tick_rotation=0, show_labels='On', show_percents='Off', 
              round_value=2, dpi=100, target=0, show_target='Off'):
    
    """
    Generate a bar chart with optional bar labels, percentage labels, and target lines.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the data to be plotted.
    x_axis_data : str
        Column name in df for x-axis values.
    y_axis_data : str
        Column name in df for y-axis values.
    figsize : tuple, optional
        Size of the figure in inches. Default is (15, 5).
    title : str, optional
        Title of the chart. Default is an empty string.
    y_label : str, optional
        Label for the y-axis. Default is 'Value'.
    x_label : str, optional
        Label for the x-axis. Default is an empty string.
    color : str, optional
        Color of the bars. Default is 'tab:blue'.
    x_tick_rotation : int, optional
        Rotation angle of x-axis tick labels. Default is 0.
    show_labels : str, optional
        If 'On', display values for each bar in bar chart. Default is 'On'.
    show_percents : str, optional
        If 'On', display percentage labels on bars. Default is 'Off'.
    round_value : int, optional
        Number of decimal places for bar labels. Default is 2.
    dpi : int, optional
        Dots per inch for the figure. Default is 100.
    target : float, optional
        Target value for a horizontal line on the chart. Default is 0.
    show_target : str, optional
        If 'On', display a horizontal target line. Default is 'Off'.

    Returns:
    --------
    None
        This function does not return any value. It displays a bar chart.

    """
    # Generate the bar chart
    fig,ax = plt.subplots(figsize=figsize, dpi=dpi)
    bar = sns.barplot(data=df, x=x_axis_data, y=y_axis_data, color=color)

    for spine in ['top','right']:
        ax.spines[spine].set_visible(False)
    
    # Show bar labels
    if (show_labels == 'On') | (show_labels == 'ON') | (show_labels == 'on'):
        for p in ax.patches:
            label = f'{p.get_height():.{round_value}f}'
            # Check condition and append '%' if needed
            if (show_percents == 'On') | (show_percents == 'ON') | (show_percents == 'on'):  # Replace 'condition' with your actual condition
                label += '%'

            ax.annotate(label, (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', fontsize=12, color='black',
                        bbox=dict(facecolor='white', alpha=1, edgecolor='black', boxstyle='round'))
    
    # Conditionally show target value
    if (show_target == 'On') | (show_target == 'ON'):
        ax.axhline(target, color='black', ls='--')
        # Set bbox properties
        bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1)
        ax.text(ax.get_xlim()[1] * 1.0, target, target, color='black', ha='center', va='center', bbox=bbox_props)
                    
    # Set horizontal grid color
    #ax.yaxis.grid(color='white',linewidth=1)

    # Set axis position
    ax.set_axisbelow(False)
    
    plt.xticks(rotation=x_tick_rotation)
    # Set title and axis labels
    ax.set_title(title, fontsize=14, y=1.05)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    plt.show()

# Create mean to target function
def delta_chart(df, x_axis_data, y_axis_data, figsize=(15,3), title='', y_label='Value', x_label='', color='tab:blue',
              x_tick_rotation=0, round_value=2, show_percents='Off', dpi=300):
    """
    Generate a delta bar chart with optional bar labels and percentage labels.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the data to be plotted.
    x_axis_data : str
        Column name in df for x-axis values.
    y_axis_data : str
        Column name in df for y-axis values.
    figsize : tuple, optional
        Size of the figure in inches. Default is (15, 3).
    title : str, optional
        Title of the chart. Default is an empty string.
    y_label : str, optional
        Label for the y-axis. Default is 'Value'.
    x_label : str, optional
        Label for the x-axis. Default is an empty string.
    color : str, optional
        Color of the bars. Default is 'tab:blue'.
    x_tick_rotation : int, optional
        Rotation angle of x-axis tick labels. Default is 0.
    round_value : int, optional
        Number of decimal places for bar labels. Default is 2.
    show_percents : str, optional
        If 'On', display percentage labels on bars. Default is 'Off'.
    dpi : int, optional
        Dots per inch for the figure. Default is 300.

    Returns:
    --------
    None
        This function does not return any value. It displays a delta bar chart.

    """
    # Generate the bar chart
    fig,ax = plt.subplots(figsize=figsize, dpi=dpi)
    bar = sns.barplot(data=df, x=x_axis_data, y=y_axis_data, color=color)

    # Plot horizontal line at zero
    ax.axhline(0, color='black', alpha=0.75)
    
    for spine in ['top','right']:
        ax.spines[spine].set_visible(False)
    
    # Add bar labels
    for p in ax.patches:
        label = f'{p.get_height():.{round_value}f}'
        # Check condition and append '%' if needed
        if (show_percents == 'On') | (show_percents == 'ON'):  # Replace 'condition' with your actual condition
            label += '%'

        ax.annotate(label, (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', fontsize=12, color='black',
                    bbox=dict(facecolor='white', alpha=1, edgecolor='black', boxstyle='round'))
    
    # Set xtick rotation
    plt.xticks(rotation=x_tick_rotation)
    
    # Set title and axis labels
    ax.set_title(title, fontsize=14, y=1.05)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    plt.show()

    # Create limit chart function
def limit_chart(df, values, x_labels, target, USL, LSL, title='Limit Chart', y_label='Value', 
                     x_label='', figsize=(15,3), round_value=4, dpi=300):
    
    """
    Generate a specifcation limit chart plot and calculate relevant parameters.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe containing the data.
    values : str or list of str
        Column name(s) in `df` that contain the values to be plotted.
    x_labels : str or list of str
        Column name(s) in `df` that provide labels for the x-axis.
    target : float
        Target value for the process.
    USL : float
        Upper Specification Limit.
    LSL : float
        Lower Specification Limit.
    title : str, optional
        Title of the plot (default is 'Limit Chart').
    y_label : str, optional
        Label for the y-axis (default is 'Value').
    x_label : str, optional
        Label for the x-axis (default is '').
    figsize : tuple, optional
        Figure size in inches (width, height) (default is (15, 3)).
    round_value : int, optional
        Number of decimal places to round mean and PBC parameters (default is 4).
    dpi : int, optional
        Dots per inch for figure resolution (default is 300).

    Returns:
    --------
    pandas.DataFrame
        DataFrame summarizing the calculated PBC parameters including Mean, Target, Mean to Target Delta,
        Upper Specification Limit (USL), Lower Specification Limit (LSL), Specification Limit Range (SLR),
        Number of Values, Number of Values Outside Specification Limits (# Outside Spec), and
        Percentage of Values Outside Specification Limits (% Outside Spec).
    """
    
    # Disaggregate the dataframe 
    data = df[values]
    labels = df[x_labels]
    
    # Values in dataset
    num_of_values = len(data)
    
    # Calculate the mean
    mean = round(data.mean(),round_value)
    mean_to_target_delta = target - mean
    
    # Calculate specification limit range (SLR)
    SLR = USL - LSL
    
    # Masking parameters for values outside process limits
    outside_USL = np.sum(data > USL)
    outside_LSL = np.sum(data < LSL)
    outside_spec = round(outside_USL + outside_LSL,2)
    percent_outside_spec = round((outside_spec/num_of_values)*100,2)
    
    # Create masking parameters for values greater than and less than the process limits on X-chart
    upper_lim = np.ma.masked_where(data < USL, data)
    lower_lim = np.ma.masked_where(data > LSL, data)
    # Create masking parameters for values greater than URL on mR-chart
    usl_greater = np.ma.masked_where(data < USL, data)
    usl_less = np.ma.masked_where(data > USL, data)
    
    # Create list of tuples that specify value and color for mean, AmR, UPL, LPL, and URL
    chart_lines = [(mean,'black'), (USL,'grey'), (LSL,'grey')]
    # Create list of tuples with y-coordinate and labels for x-chart process limits and centerline 
    chart_labels = [(USL,USL),(LSL,LSL),(mean,mean)]
    
    # Generate the X-chart
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Plot data 
    ax.plot(labels, data, marker='o')

    # Add masking parameters to color values outside process limits
    ax.plot(labels, lower_lim, marker='o', ls='none', color='tab:red',
            markeredgecolor='black', markersize=9)
    ax.plot(labels, upper_lim, marker='o', ls='none', color='tab:red',
            markeredgecolor='black', markersize=9)

    # Add text labels for limits and centerline
    bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="grey", lw=1)
    bbox_props_centerlines = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1)
    ax.text(ax.get_xlim()[1] * 1.0, USL, USL, color='grey', ha='center', va='center', bbox=bbox_props)
    ax.text(ax.get_xlim()[1] * 1.0, LSL, LSL, color='tab:grey', ha='center', va='center', bbox=bbox_props)
    ax.text(ax.get_xlim()[1] * 1.0, mean, mean, color='black', ha='center', va='center', bbox=bbox_props_centerlines)

    # Add centerline and process limits 
    for value, color in chart_lines:
        plt.axhline(value, ls='--', c=color)

    # Specify spine visibility 
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_alpha(0.5)

    # Specify axis labels and title
    plt.xlabel(x_label,fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=14)

    # Show plot
    plt.show()
    
    # Create list of PBC paramters
    chart_params = ['Mean','Target','Mean to Tar. Delta','USL','LSL',
                    'Spec Limit Range','# of Values','# Outside Spec', '% Outside Spec']
    chart_type = ['Limit Chart']*len(chart_params)
    chart_values = [mean, target, mean_to_target_delta, USL, LSL, SLR, 
                    num_of_values, outside_spec, percent_outside_spec]
    # Create df for PBC parameters
    results_df = pd.DataFrame()
    results_df['Chart'] = pd.Series(chart_type)
    results_df['Parameters'] = pd.Series(chart_params)
    results_df['Values'] = pd.Series(chart_values)
    
    return results_df

# Create X-chart function
def xchart(df, values, x_labels, title='X-chart', y_label='Individual Values', x_label='', fig_size=(15,3), 
            round_value=1, dpi=300):
    
    """
    Generate an X-chart (Individual Values Chart) from the provided DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing the data.
    values : str
        Column name in `df` representing the individual values.
    x_labels : str
        Column name in `df` for the x-axis labels.
    title : str, optional
        Title for the plot, default is 'X-chart'.
    y_label : str, optional
        Label for the y-axis, default is 'Individual Values'.
    x_label : str, optional
        Label for the x-axis, default is an empty string.
    fig_size : tuple, optional
        Figure size in inches (width, height), default is (15, 3).
    round_value : int, optional
        Number of decimal places to round calculations, default is 2.
    dpi : int, optional
        Dots per inch (resolution) of the figure, default is 300.

    Returns:
    --------
    dict
        A dictionary containing DataFrames with calculated parameters and causes:
        - 'PBC Params': DataFrame with calculated parameters 'Mean', 'UPL' (Upper Process Limit), 'LPL' (Lower Process Limit), and 'PLR' (Process Limit Range).
        - 'X-Chart DataFrame': DataFrame with added column 'X-Chart Variation' categorizing causes as 'Routine Cause' or 'Assignable Cause'.

    Notes:
    ------
    - The function plots the X-chart using matplotlib.
    - Calculates the Mean, Upper Process Limit (UPL), Lower Process Limit (LPL), and Process Limit Range (PLR) based on the provided data.
    - Identifies and categorizes routine and assignable causes based on the UPL and LPL.

    Example:
    --------
    x_chart(df, 'Values', 'Observation', title='Example X-chart')

    """
    
    # Disaggregate the dataframe 
    data = df[values]
    moving_ranges = round(abs(data.diff()),round_value)
    labels = df[x_labels]

    # Add moving ranges to df as column
    df['Moving Ranges'] = pd.Series(moving_ranges)
    
    # Calculate the mean
    mean = round(data.mean(),round_value)
    # Calculate the average moving range 
    AmR = round(moving_ranges.mean(),round_value)
    
    # Define the value of C1 and C2and calculate the UPL and LPL
    C1 = 2.660
    C2 = 3.268
    # Calculate the process limits
    UPL = round(mean + (C1*AmR),round_value)
    LPL = round(mean - (C1*AmR),round_value)
    # Calculate process limit range (PLR)
    PLR = UPL - LPL
    # Conditionally determine LPL if LPL is less than zero
    LPL = max(LPL,0)
    # Calculate the Upper Range Limit
    URL = round(C2*AmR,round_value)
    
    # Create masking parameters for values greater than and less than the process limits on X-chart
    upper_lim = np.ma.masked_where(data < UPL, data)
    lower_lim = np.ma.masked_where(data > LPL, data)
    # Create masking parameters for values greater than URL on mR-chart
    url_greater = np.ma.masked_where(moving_ranges <= URL, moving_ranges)
    url_less = np.ma.masked_where(moving_ranges > URL, moving_ranges)
    
    # Create list of tuples that specify value and color for mean, AmR, UPL, LPL, and URL
    xchart_lines = [(mean,'black'), (UPL,'red'), (LPL,'red')]
    mrchart_lines = [(AmR,'black'), (URL,'red')]
    # Create list of tuples with y-coordinate and labels for x-chart process limits and centerline 
    xchart_labels = [(UPL,UPL),(LPL,LPL),(mean,mean)]
    # Create list of tuples with y-coordinate and labels for mR-chart process limit and centerline
    mrchart_labels = [(URL,URL),(AmR,AmR)]
    
    # Generate the X-chart
    fig, ax = plt.subplots(figsize=fig_size, dpi=dpi)

    # Plot data 
    ax.plot(labels, data, marker='o')

    # Add masking parameters to color values outside process limits
    ax.plot(labels, lower_lim, marker='o', ls='none', color='tab:red',
            markeredgecolor='black', markersize=9)
    ax.plot(labels, upper_lim, marker='o', ls='none', color='tab:red',
            markeredgecolor='black', markersize=9)

    # Add text labels for limits and centerline
    bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="red", lw=1)
    bbox_props_centerlines = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1)
    ax.text(ax.get_xlim()[1] * 1.0, UPL, UPL, color='red', ha='center', va='center', bbox=bbox_props)
    ax.text(ax.get_xlim()[1] * 1.0, LPL, LPL, color='red', ha='center', va='center', bbox=bbox_props)
    ax.text(ax.get_xlim()[1] * 1.0, mean, mean, color='black', ha='center', va='center', bbox=bbox_props_centerlines)

    # Add centerline and process limits 
    for value, color in xchart_lines:
        plt.axhline(value, ls='--', c=color)

    # Specify spine visibility 
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_alpha(0.5)

    # Specify axis labels and title
    plt.xlabel(x_label,fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=14)
    
    # Show plot
    plt.show()
    
    # Create functions for labeling types of variation 
    def xchart_variation(value):
        if (value > UPL) | (value < LPL):
            return 'Assignable Cause'
        else:
            return 'Routine Cause'
    
    # Apply variation_conditions
    df['X-Chart Variation'] = df[values].apply(xchart_variation)
    
    # Create list of PBC paramters
    chart_type = ['X-Chart']*4
    xchart_params = ['Mean','UPL','LPL','PLR']
    xchart_values = [mean,UPL,LPL,PLR]
    # Create df for PBC parameters
    PBC_params_df = pd.DataFrame()
    PBC_params_df['Chart'] = pd.Series(chart_type)
    PBC_params_df['Parameters'] = pd.Series(xchart_params)
    PBC_params_df['Values'] = pd.Series(xchart_values)
    
    # Create dictionary of dfs
    result_dfs = {'PBC Params':PBC_params_df, 
                  'X-Chart Dataframe':df
                 }
    
    return result_dfs

# Create mR-chart function
def mrchart(df, moving_ranges, x_labels, fig_size=(15,3), y_label='Moving Ranges', x_label='', title='mR-chart', 
             round_value=2, dpi=300):
    
    """
    Generate an mR-chart (Moving Range Chart) from the provided DataFrame. 

    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing the data.
    moving_ranges : str
        Column name in `df` representing the moving ranges.
    x_labels : str
        Column name in `df` for the x-axis labels.
    fig_size : tuple, optional
        Figure size in inches (width, height), default is (15, 3).
    y_label : str, optional
        Label for the y-axis, default is 'Moving Ranges'.
    x_label : str, optional
        Label for the x-axis, default is an empty string.
    title : str, optional
        Title for the plot, default is 'mR-chart'.
    round_value : int, optional
        Number of decimal places to round calculations, default is 2.
    dpi : int, optional
        Dots per inch (resolution) of the figure, default is 300.

    Returns:
    --------
    dict
        A dictionary containing DataFrames with calculated parameters and causes:
        - 'PBC Params': DataFrame with calculated parameters 'AmR' (Average Moving Range) and 'URL' (Upper Range Limit).
        - 'mR-Chart DataFrame': DataFrame with added column 'mR-Chart Variation' categorizing causes as 'Routine Cause' or 'Assignable Cause'.

    Notes:
    ------
    - The function plots the mR-chart using matplotlib.
    - Calculates the Average Moving Range (AmR) and Upper Range Limit (URL) based on the provided data.
    - Identifies and categorizes routine and assignable causes based on the URL.

    Example:
    --------
    mr_chart(df, 'Moving Ranges', 'Observation', title='Example mR-chart')

    """
    
    mRs = df[moving_ranges]
    labels = df[x_labels]
    
    # Calculate the average moving range 
    AmR = round(mRs.mean(),2)

    # Define the value of C2
    C2 = 3.27
    # Calculate the Upper Range Limit
    URL = round(C2*AmR,round_value)
    
    # Create masking parameters for values greater than URL on mR-chart
    url_greater = np.ma.masked_where(mRs <= URL, mRs)
    url_less = np.ma.masked_where(mRs > URL, mRs)
    
    # Create list of tuples that specify value and color for mean, AmR, UPL, LPL, and URL
    mRchart_lines = [(AmR,'black'), (URL,'red')]
    # Create list of tuples with y-coordinate and labels for mR-chart process limit and centerline
    mRchart_labels = [(URL,URL),(AmR,AmR)]
    
    # Generate the mR-chart
    fig,ax = plt.subplots(figsize=fig_size, dpi=dpi)

    # Plot data 
    ax.plot(labels , mRs, marker='o')
    #ax.plot(mRs)
    # # Add masking parameters to show values greater than the URL
    ax.plot(labels, url_greater, marker='o', ls='none', color='tab:red', 
            markeredgecolor='black', markersize=9)

    # Add centerline and process limits 
    for value, color in mRchart_lines:
        plt.axhline(value, ls='--', c=color)

    # Add text labels for limits and centerline
    bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="red", lw=1)
    bbox_props_centerlines = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1)
    ax.text(ax.get_xlim()[1] * 1.0, URL, URL, color='red', ha='center', va='center', bbox=bbox_props)
    ax.text(ax.get_xlim()[1] * 1.0, AmR, AmR, color='black', ha='center', va='center', bbox=bbox_props_centerlines)


    # Specify spine visibility 
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_alpha(0.5)

    # Specify axis labels and title
    plt.xlabel(x_label,fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=14)

    # Show plot
    plt.show()
    
    # Create functions for labeling types of variation 
    def mrchart_variation(value):
        if value > URL:
            return 'Assignable Cause'
        else:
            return 'Routine Cause'
    
    # Apply variation_conditions
    df['mR-Chart Variation'] = df['Moving Ranges'].apply(mrchart_variation)
    
    # Create list of PBC paramters
    chart_type = ['mR-Chart']*2
    param_names = ['AmR','URL']
    param_values = [AmR,URL]
    # Create df for PBC parameters
    mrchart_params_df = pd.DataFrame()
    mrchart_params_df['Chart'] = pd.Series(chart_type)
    mrchart_params_df['Parameters'] = pd.Series(param_names)
    mrchart_params_df['Values'] = pd.Series(param_values)
    
    # Create dictionary of dfs
    result_dfs = {'PBC Params':mrchart_params_df, 
                  'mR-Chart Dataframe':df
                 }
    
    return result_dfs

# Process behavior chart (pbc) function
def pbc(df, values, x_labels, xchart_title='X-chart', mrchart_title='mR-chart', fig_size=(15,6), round_value=2, dpi=300):
    
    """
    Generate an XmR-chart (X and mR-chart) from the provided DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing the data.
    values : str
        Column name in `df` representing the individual values for X-chart.
    x_labels : str
        Column name in `df` for the x-axis labels.
    xchart_title : str, optional
        Title for the X-chart plot, default is 'X-chart'.
    mrchart_title : str, optional
        Title for the mR-chart plot, default is 'mR-chart'.
    fig_size : tuple, optional
        Figure size in inches (width, height), default is (15, 6).
    round_value : int, optional
        Number of decimal places to round calculations, default is 2.
    dpi : int, optional
        Dots per inch (resolution) of the figure, default is 300.

    Returns:
    --------
    dict
        A dictionary containing DataFrames with calculated parameters and causes:
        - 'PBC Params': DataFrame with calculated parameters including 'Mean', 'UPL' (Upper Process Limit), 'LPL' (Lower Process Limit) for X-chart,
                        'PLR' (Process Limit Range), 'AmR' (Average Moving Range), and 'URL' (Upper Range Limit) for mR-chart.
        - 'XmR-Chart Dataframe': DataFrame with added columns 'X-Chart Variation' and 'mR-Chart Variation' categorizing causes as 'Routine Cause' or 'Assignable Cause'.

    Notes:
    ------
    - The function plots both X-chart (Individual Values Chart) and mR-chart (Moving Range Chart) using matplotlib.
    - Calculates statistical parameters and identifies routine and assignable causes based on process limits.

    Example:
    --------
    PBC(df, 'Values', 'Observation', xchart_title='Example X-chart', mrchart_title='Example mR-chart')

    """
    
    # Disaggregate the dataframe 
    data = df[values]
    moving_ranges = round(abs(data.diff()),round_value)
    labels = df[x_labels]

    # Add moving ranges to df as column
    df['Moving Ranges'] = pd.Series(moving_ranges)
    
    # Calculate the mean
    mean = round(data.mean(),round_value)
    # Calculate the average moving range 
    AmR = round(moving_ranges.mean(),round_value)
    
    # Define the value of C1 and C2and calculate the UPL and LPL
    C1 = 2.660
    C2 = 3.268
    # Calculate the process limits
    UPL = round(mean + (C1*AmR),round_value)
    LPL = round(mean - (C1*AmR),round_value)
    # Calculate process limit range (PLR)
    PLR = UPL - LPL
    # Conditionally determine LPL if LPL is less than zero
    LPL = max(LPL,0)
    # Calculate the Upper Range Limit
    URL = round(C2*AmR,round_value)
    
    # Create masking parameters for values greater than and less than the process limits on X-chart
    upper_lim = np.ma.masked_where(data < UPL, data)
    lower_lim = np.ma.masked_where(data > LPL, data)
    # Create masking parameters for values greater than URL on mR-chart
    url_greater = np.ma.masked_where(moving_ranges <= URL, moving_ranges)
    url_less = np.ma.masked_where(moving_ranges > URL, moving_ranges)
    
    # Create list of tuples that specify value and color for mean, AmR, UPL, LPL, and URL
    xchart_lines = [(mean,'black'), (UPL,'red'), (LPL,'red')]
    mrchart_lines = [(AmR,'black'), (URL,'red')]
    # Create list of tuples with y-coordinate and labels for x-chart process limits and centerline 
    xchart_labels = [(UPL,UPL),(LPL,LPL),(mean,mean)]
    # Create list of tuples with y-coordinate and labels for mR-chart process limit and centerline
    mrchart_labels = [(URL,URL),(AmR,AmR)]
    
    # Generate the XmR-chart
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=fig_size, dpi=dpi)
    fig.subplots_adjust(hspace=0.3)
    
    # Plot data for x-chart
    axs[0].plot(labels, data, marker='o')
    # Plot data for mR-chart
    axs[1].plot(labels , moving_ranges, marker='o')
    
    # Add masking parameters to color values outside process limits
    axs[0].plot(labels, lower_lim, marker='o', ls='none', color='tab:red',
            markeredgecolor='black', markersize=9)
    axs[0].plot(labels, upper_lim, marker='o', ls='none', color='tab:red',
            markeredgecolor='black', markersize=9)
    axs[1].plot(labels, url_greater, marker='o', ls='none', color='tab:red', 
            markeredgecolor='black', markersize=9)

    # Add text labels for limits and centerline
    bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="red", lw=1)
    bbox_props_centerline = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1)
    axs[0].text(axs[0].get_xlim()[1] * 1.0, UPL, UPL, color='red', ha='center', va='center', bbox=bbox_props)
    axs[0].text(axs[0].get_xlim()[1] * 1.0, LPL, LPL, color='red', ha='center', va='center', bbox=bbox_props)
    axs[0].text(axs[0].get_xlim()[1] * 1.0, mean, mean, color='black', ha='center', va='center', bbox=bbox_props_centerline)
    
    axs[1].text(axs[1].get_xlim()[1] * 1.0, URL, URL, color='red', ha='center', va='center', bbox=bbox_props)
    axs[1].text(axs[1].get_xlim()[1] * 1.0, AmR, AmR, color='black', ha='center', va='center', bbox=bbox_props_centerline)

    # Add centerline and process limits 
    for value, color in xchart_lines:
        axs[0].axhline(value, ls='--', c=color)

    for value, color in mrchart_lines:
        axs[1].axhline(value, ls='--', color=color)

    # Specify spine visibility 
    for value in range(0,2):
        axs[value].spines[['top','right']].set_visible(False)
        axs[value].spines[['left','bottom']].set_alpha(0.5)

    # Specify axis labels and title for x-chart
    axs[0].set_ylabel('Individual values', fontsize=12)
    axs[0].set_title(xchart_title, fontsize=14)
    
    # Specify axis labels and title for mR-chart
    axs[1].set_xlabel('Observation',fontsize=0)
    axs[1].set_ylabel('Moving ranges', fontsize=12)
    axs[1].set_title(mrchart_title, fontsize=14)
    
    # Show PBC figure
    plt.show()
    
    # Create functions for labeling types of variation 
    def xchart_variation(value):
        if (value > UPL) | (value < LPL):
            return 'Assignable Cause'
        else:
            return 'Routine Cause'
    
    def mrchart_variation(value):
        if value > URL:
            return 'Assignable Cause'
        else:
            return 'Routine Cause'
    
    # Apply variation_conditions
    df['X-Chart Variation'] = df[values].apply(xchart_variation)
    df['mR-Chart Variation'] = df['Moving Ranges'].apply(mrchart_variation)
    
    # Create list of PBC paramters
    chart_type = ['X-Chart']*4
    chart_type.extend(['mR-Chart'] * 2)
    param_names = ['Mean','UPL','LPL','PLR','AmR','URL']
    param_values = [mean,UPL,LPL,PLR,AmR,URL]
    # Create df for PBC parameters
    PBC_params_df = pd.DataFrame()
    PBC_params_df['Chart'] = pd.Series(chart_type)
    PBC_params_df['PBC Params'] = pd.Series(param_names)
    PBC_params_df['Param Values'] = pd.Series(param_values)
    
    # Create dictionary of dfs
    result_dfs = {'PBC Params':PBC_params_df, 
                  'XmR-Chart Dataframe':df
                 }
    
    return result_dfs

# Improved network analysis function
def network_analysis(df_list, condition, label_list, title='Network Analysis', rows=1, 
                     cols=2, linestyle='-', xticks=False, hide_last='Off', color=None,
                     round_value=3, figsize=(15,10), dpi=300):
    
    """
    Perform network analysis on a list of DataFrames, plotting control charts and returning statistical summaries.

    Parameters:
    -----------
    df_list : list of pandas.DataFrame
        List of DataFrames containing the data to be analyzed.
    condition : str
        Column name in the DataFrames to be used for analysis.
    label_list : list of str
        List of labels corresponding to each DataFrame for plot titles.
    title : str, optional (default='Network Analysis')
        Title for the overall figure.
    rows : int, optional (default=1)
        Number of rows in the subplot grid.
    cols : int, optional (default=2)
        Number of columns in the subplot grid.
    linestyle : str, optional (default='-')
        Line style for the data plots.
    xticks : bool, optional (default=False)
        Whether to display x-axis ticks.
    hide_last : str, optional (default='Off')
        Whether to hide the last subplot. Options are 'On' or 'Off'.
    color : list of str, optional
        List of colors for the data plots. If not provided, defaults to ['tab:blue'].
    figsize : tuple, optional (default=(15, 10))
        Size of the overall figure.
    dpi : int, optional (default=300)
        Dots per inch for the figure resolution.

    Returns:
    --------
    results_df : pandas.DataFrame
        DataFrame containing the calculated statistics and predictability characterization for each DataFrame.

    Raises:
    -------
    ValueError
        If `condition` is not a column in any of the DataFrames in `df_list`.
        If the length of `label_list` does not match the length of `df_list`.

    Notes:
    ------
    - The function calculates the mean, average moving range (AmR), upper control limit (UPL),
      lower control limit (LPL), and upper range limit (URL) for each DataFrame.
    - It generates control charts for the data and masks values exceeding the control limits.
    - It determines if the data is 'Predictable' or 'Unpredictable' based on control limits.

    Example:
    --------
    >>> data1 = pd.Series([80, 90, 85, 95, 100])
    >>> data2 = pd.Series([120, 125, 130, 135, 140])
    >>> df_list = [pd.DataFrame({'value': data1}), pd.DataFrame({'value': data2})]
    >>> condition = 'value'
    >>> label_list = ['Data 1', 'Data 2']
    >>> results = network_analysis(df_list, condition, label_list)
    >>> print(results)
    """
    
    if color is None:
        color = ['tab:blue']
    
    # Ensure the color list is long enough for the number of plots
    if len(color) < len(df_list):
        color = (color * (len(df_list) // len(color) + 1))[:len(df_list)]
    
    # Validate inputs
    if not all(condition in df.columns for df in df_list):
        raise ValueError("Condition must be a column in all dataframes.")
    if len(label_list) != len(df_list):
        raise ValueError("Label list must have the same length as the dataframe list.")
    
    # Constants for control limits
    C1 = 2.660
    C2 = 3.268
    
    # Calculate statistics
    stats = [
        (
            df[condition].mean(),
            abs(df[condition].diff()).mean(),
            max(df[condition].mean() + C1 * abs(df[condition].diff()).mean(),0),
            max(df[condition].mean() - C1 * abs(df[condition].diff()).mean(),0),
            C2 * abs(df[condition].diff()).mean()
        )
        for df in df_list
    ]
    
    # Create results dataframe
    parameters_df = pd.DataFrame(stats, columns=['Mean', 'AmR', 'UPL', 'LPL', 'URL'])
    parameters_df['Labels'] = label_list
    parameters_df['PLR'] = parameters_df['UPL'] - parameters_df['LPL']
    parameters_df['data'] = [df[condition] for df in df_list]
    parameters_df['mR'] = [df[condition].diff() for df in df_list]
    
    # Determine characterization
    parameters_df['Characterization'] = parameters_df.apply(
        lambda row: 'Predictable' if all(row['LPL'] <= x <= row['UPL'] for x in row['data']) else 'Unpredictable',
        axis=1
    )
    
    # Plotting
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=figsize, sharey=True, dpi=dpi)
    plt.subplots_adjust(wspace=0)
    plt.suptitle(title, fontsize=14, y=1.05)

    axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

    for idx, (data, UPL, LPL, label, ax) in enumerate(zip(
            parameters_df['data'], parameters_df['UPL'], parameters_df['LPL'], parameters_df['Labels'], axes)):
        
        # Plot data
        ax.plot(data, marker='o', ls=linestyle, color=color[idx % len(color)])

        # Masking and plotting limits
        ax.plot(np.ma.masked_where(data < UPL, data), marker='o', ls='none', color='red', markeredgecolor='black', markersize=9)
        ax.plot(np.ma.masked_where(data > LPL, data), marker='o', ls='none', color='red', markeredgecolor='black', markersize=9)
#         ax.plot(np.ma.masked_where(data == 0, data), marker='o', ls='none', color='red', markeredgecolor='black', markersize=9)
        
        # Highlight points where the data is zero in red
        zero_indices = (data == 0)
        ax.plot(np.where(zero_indices)[0], data[zero_indices], marker='o', ls='none', color='red', markeredgecolor='black', markersize=9)
    
        # Plotting lines for mean, UPL, and LPL
        mean = np.mean(data)
        ax.axhline(mean, ls='--', color='black')
        ax.axhline(UPL, ls='--', color='red')
        ax.axhline(LPL, ls='--', color='red')
        
        # Styling axes
        ax.grid(False)
        ax.set_title(label, fontsize=12)
        for spine in ['top', 'right', 'bottom']:
            ax.spines[spine].set_visible(False)
        ax.spines['left'].set_alpha(0.5)
        ax.tick_params(axis='both', which='both', length=0)
        
        if not xticks:
            ax.set_xticks([])

    # Hide the last subplot by removing its axis
    if hide_last.lower() == 'on':
        axes[-1].axis('off')
    
    # Show figure 
    plt.show()
    
    # Reorder and return the results dataframe
    new_order = ['Labels', 'Mean', 'UPL', 'LPL', 'PLR', 'AmR', 'URL', 'Characterization']
    results_df = parameters_df[new_order]
    
    return results_df

def xchart_comparison(df_list, condition, x_labels, list_of_plot_labels, title='',
                      linestyle='-', y_label='Individual Values', tickinterval=5,
                      colors=['tab:blue','tab:blue'], figsize=(12,4), 
                      dpi=300):
    
    """
    Compare X-charts for multiple datasets and plot the results with specified x-axis labels.

    Parameters:
    -----------
    df_list : list of pandas.DataFrame
        A list of DataFrames containing the data to be plotted. Each DataFrame represents a different dataset.
        
    condition : str
        The column name in each DataFrame to be analyzed and plotted on the X-chart.
        
    x_labels : str
        The column name in each DataFrame to be used for x-axis labels (e.g., time or index).
        
    list_of_plot_labels : list of str
        A list of labels for each individual plot, used as titles for the subplots. 
        The list should be the same length as df_list.
        
    title : str, optional
        The overall title of the entire plot. Default is an empty string.
        
    linestyle : str, optional
        The line style for the plot lines (e.g., '-', '--', '-.', ':'). Default is '-' (solid line).
        
    y_label : str, optional
        The label for the y-axis. Default is 'Individual Values'.
        
    tickinterval : int, optional
        The interval at which x-ticks are placed on the x-axis. Default is 5.
        
    colors : list of str, optional
        A list of colors for the plot lines. Default is ['tab:blue', 'tab:blue'].
        
    figsize : tuple of int, optional
        The size of the figure in inches. Default is (12, 4).
        
    dpi : int, optional
        The resolution of the figure in dots per inch. Default is 300.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing calculated statistics and characterizations for each input DataFrame, 
        including the mean, average moving range (AmR), upper and lower control limits (UPL, LPL), 
        process limit range (PLR), upper range limit (URL), and whether the data is predictable or unpredictable.

    Notes:
    ------
    - This function generates X-charts (control charts) for each DataFrame in df_list, 
      displaying individual values with their respective control limits.
    - The function automatically determines whether the process is predictable or unpredictable 
      based on whether all data points fall within the control limits.
    - The x-ticks are customized based on the provided tick interval, which controls the spacing between ticks.

    Example Usage:
    --------------
    # Assuming df_list and label_list are predefined
    results = xchart_comparison(
        df_list=df_list, 
        condition='data_column', 
        x_labels='x_column', 
        list_of_plot_labels=label_list, 
        title='Comparison of X Control Charts'
    )
    """
    
    # Constants for control limits
    C1 = 2.660
    C2 = 3.268
    
    color = colors
    
    # Calculate statistics
    stats = [
        (
            df[condition].mean(),
            abs(df[condition].diff()).mean(),
            df[condition].mean() + C1 * abs(df[condition].diff()).mean(),
            max(df[condition].mean() - C1 * abs(df[condition].diff()).mean(),0),
            C2 * abs(df[condition].diff()).mean()
        )
        for df in df_list
    ]
    
    # Isolate column to be used for x_labels
    x_labels_for_plots = [df[x_labels] for df in df_list]
    
    # Create results dataframe
    parameters_df = pd.DataFrame(stats, columns=['Mean', 'AmR', 'UPL', 'LPL', 'URL'])
    parameters_df['Labels'] = list_of_plot_labels
    parameters_df['PLR'] = parameters_df['UPL'] - parameters_df['LPL']
    parameters_df['data'] = [df[condition] for df in df_list]
    parameters_df['mR'] = [abs(df[condition].diff()) for df in df_list]
    
    # Determine predictability
    parameters_df['Characterization'] = parameters_df.apply(
        lambda row: 'Predictable' if all(row['LPL'] <= x <= row['UPL'] for x in row['data']) else 'Unpredictable',
        axis=1
    )
    
    # Plotting
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize, sharey=True, dpi=dpi)
    plt.subplots_adjust(wspace=0)
    plt.suptitle(title, fontsize=14, y=1.05)

    axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

    for idx, (data, UPL, LPL, label, ax, x_labels) in enumerate(zip(
        parameters_df['data'], 
        parameters_df['UPL'], 
        parameters_df['LPL'], 
        parameters_df['Labels'], 
        axes,
        x_labels_for_plots)):
    
        # Plot data
        ax.plot(data, marker='o', ls=linestyle, color=color[idx % len(color)])

        # Masking and plotting limits
        ax.plot(np.ma.masked_where(data < UPL, data), marker='o', ls='none', color='red', markeredgecolor='black', markersize=9)
        ax.plot(np.ma.masked_where(data > LPL, data), marker='o', ls='none', color='red', markeredgecolor='black', markersize=9)

        # Plotting lines for mean, UPL, and LPL
        mean = np.mean(data)
        ax.axhline(mean, ls='--', color='black')
        ax.axhline(UPL, ls='--', color='red')
        ax.axhline(LPL, ls='--', color='red')

        # Styling axes
        ax.grid(False)
        ax.set_title(label, fontsize=12)
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        ax.spines[['left','bottom']].set_alpha(0.5)
        ax.tick_params(axis='y', which='both', length=0)
        ax.tick_params(axis='x', which='both')

        # Add y-label only to the first plot
        if idx == 0:
            ax.set_ylabel(y_label, fontsize=12)

        # Set the x-tick labels with increased intervals
        tick_interval = tickinterval  # Increase this value to increase the spacing between ticks
        tick_positions = np.arange(0, len(data), tick_interval)
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(x_labels[tick_positions], rotation=0, ha='center')

    # Show figure 
    plt.show()
    
    # Reorder and return the results dataframe
    new_order = ['Labels', 'Mean', 'UPL', 'LPL', 'PLR', 'AmR', 'URL', 'Characterization']
    results_df = parameters_df[new_order]
    
    return results_df

def mrchart_comparison(df_list, condition, x_labels, list_of_plot_labels, 
                       title='mR-Chart Comparison', linestyle='-',
                       colors=['tab:blue','tab:blue'], figsize=(15,3), 
                       dpi=300):
    
    """
    Generate and compare mR (moving range) control charts for multiple datasets.

    Parameters:
    -----------
    df_list : list of pandas DataFrames
        List of DataFrames containing data for comparison.
    condition : str
        Column name in the DataFrames representing the data to be analyzed.
    x_labels : str
        Column name in the DataFrames representing the labels for the x-axis.
    list_of_plot_labels : list of str
        List of labels corresponding to each DataFrame in df_list.
    title : str, optional
        Title for the plot (default is 'mR-Chart Comparison').
    linestyle : str, optional
        Linestyle for plotting data (default is '-').
    colors : list of str, optional
        List of colors for plotting data, alternating for different datasets (default is ['tab:blue', 'tab:blue']).
    figsize : tuple, optional
        Figure size (width, height) in inches (default is (15,3)).
    dpi : int, optional
        Dots per inch for figure resolution (default is 300).

    Returns:
    --------
    results_df : pandas DataFrame
        DataFrame containing the statistical parameters and characterization results for each dataset.

    Notes:
    ------
    - Constants C1 and C2 are predefined for control limits calculation.
    - Calculates statistical parameters like Mean moving range (AmR), Upper Range Limit (URL) for each dataset.
    - Determines predictability of each dataset based on control limits.
    - Plots moving range values, mean moving range, and control limits for each dataset on separate subplots.
    - Adjusts subplot spacing and styling for better visualization.

    Example Usage:
    --------------
    # Assuming df_list and label_list are predefined
    results = mrchart_comparison(df_list, 'data_column', 'x_column', label_list, title='Comparison of mR Control Charts')
    """

    # Constants for control limits
    C1 = 2.660
    C2 = 3.268
    
    color = colors
    
    # Calculate statistics
    stats = [
        (
            df[condition].mean(),
            abs(df[condition].diff()).mean(),
            df[condition].mean() + C1 * abs(df[condition].diff()).mean(),
            df[condition].mean() - C1 * abs(df[condition].diff()).mean(),
            C2 * abs(df[condition].diff()).mean()
        )
        for df in df_list
    ]
    
    # Isolate column to be used for x_labels
    x_labels_for_plots = [df[x_labels] for df in df_list]
    
    # Create results dataframe
    parameters_df = pd.DataFrame(stats, columns=['Mean', 'AmR', 'UPL', 'LPL', 'URL'])
    parameters_df['Labels'] = list_of_plot_labels
    parameters_df['PLR'] = parameters_df['UPL'] - parameters_df['LPL']
    parameters_df['data'] = [df[condition] for df in df_list]
    parameters_df['mRs'] = [abs(df[condition].diff()) for df in df_list]
    
    # Determine predictability
    parameters_df['Characterization'] = parameters_df.apply(
        lambda row: 'Predictable' if all(row['URL'] < x  for x in row['mRs']) else 'Unpredictable',
        axis=1
    )
    
    # Plotting
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize, sharey=True, dpi=dpi)
    plt.subplots_adjust(wspace=0)
    plt.suptitle(title, fontsize=14, y=1.05)

    axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

    for idx, (mRs, URL, label, ax, x_labels) in enumerate(zip(
            parameters_df['mRs'], 
            parameters_df['URL'], 
            parameters_df['Labels'], 
            axes,
            x_labels_for_plots)):
        
        # Plot data
        ax.plot(mRs, marker='o', ls=linestyle, color=color[idx % len(color)])

        # Masking and plotting limits correctly
        ax.plot(np.ma.masked_where(mRs < URL, mRs), marker='o', ls='none', color='red', markeredgecolor='black', markersize=9)
        
        # Plotting lines for average moving range and URL 
        AmR = np.mean(mRs)
        ax.axhline(AmR, ls='--', color='black')
        ax.axhline(URL, ls='--', color='red')
        
        # Styling axes
        ax.grid(False)
        # Set title
        ax.set_title(label, fontsize=12)
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        ax.spines[['left','bottom']].set_alpha(0.5)
        ax.tick_params(axis='y', which='both', length=0)
        ax.tick_params(axis='x', which='both')#, length=1)
        
        # Add y-label only to the first plot
        if idx == 0:
            ax.set_ylabel('Moving Range', fontsize=12)
        
        # Suppress the FixedFormatter warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tick_positions = np.arange(0, len(mRs), 10)
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(x_labels[tick_positions], rotation=0, ha='center')
            
    # Show figure 
    plt.show()
    
    # Reorder and return the results dataframe
    new_order = ['Labels', 'AmR', 'URL', 'Characterization']
    results_df = parameters_df[new_order]
    
    return results_df

# Function for calculating box plot features (5-number summary and outliers)
def boxplotfeatures(df, column, round_value=2):
    
    """
    Calculate key features of a box plot for a specific column in a DataFrame.

    This function calculates the median, first quartile (Q1), third quartile (Q3), 
    interquartile range (IQR), and the upper and lower bounds of a specified column 
    in a DataFrame. It also identifies outliers based on the calculated bounds.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the data.
        
    column : str
        The name of the column in `df` for which to calculate the box plot features.
        
    round_value : int, optional (default=2)
        The number of decimal places to round the calculated values to.

    Returns:
    --------
    results_df : pandas.DataFrame
        A DataFrame containing the calculated box plot features:
        - 'Median': The median of the data.
        - 'Q1': The 25th percentile of the data.
        - 'Q3': The 75th percentile of the data.
        - 'IQR': The interquartile range (Q3 - Q1).
        - 'Lower bound': The largest value that is greater than or equal to Q1 - 1.5*IQR.
        - 'Upper bound': The largest value in the data that is less than Q3 + 1.5*IQR.
    
    outliers : pandas.DataFrame
        A DataFrame containing the rows in `df` where the values in the specified column 
        are considered outliers, i.e., values below the lower bound or above the upper bound.
    """
    
    # Specify multiplier to 1.5
    multiplier = 1.5
    
    # Calculate median
    median = df[column].median()
    
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    
    # Calculate the IQR
    IQR = Q3 - Q1
    
    # Calculate the upper and lower bounds
    lower_bound = max(Q1 - multiplier*IQR, min(df[column]))
    upper_bound = max(df[column][df[column] < Q3 + multiplier * IQR])
    
    # Identify outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        'Feature': ['Median', 'Q1', 'Q3', 'IQR', 'Lower bound', 'Upper bound'],
        'Value': [median, Q1, Q3, IQR, lower_bound, upper_bound]
    }).round(round_value)
    
    # Return "No outliers" if outliers DataFrame is empty
    if outliers.empty:
        return results_df, "No outliers"
    else:
        return results_df, outliers
