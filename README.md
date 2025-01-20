# improvement.py (version-0.2)
`improvement.py` is a collection of functions designed to facilitate the understanding and elimination of `routine` and `assignable` causes of variation in business and industrial processes. The primary tool to facilitate this understanding is the process behavior chart, otherwise known as the control chart.  

Visit [BrokenQuality.com](https://www.brokenquality.com/bookshelf) for resources and more details regarding the application and use of `process behavior charts`. 

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation) 
- [Usage](#usage) 
- [Contributing](#contributing) 
- [Contact](#contact) 
- [License](#license)
- [Additional Information](#additional-information)

## Prerequisites
Before you begin, ensure you have met the following requirements: 
- You have installed [Python](https://www.python.org/) 3.6 or higher. 
- You have a working knowledge of Python and data analysis libraries such as pandas and matplotlib. 
- You have a working knowledge of `Process Behavior Charts` and `Statistical Process Control`. 

## Installation
To install  `improvement.py`  directly from GitHub without cloning the repository, enter the following command using the  `command prompt`:

`pip install git+https://github.com/jimlehner/improvement`

## Usage
To use `improvement.py`, follow these steps:
1. Import process.improvement as pi
```import process.improvement as pi```
2. Prepare you data as a pandas DataFrame.
3. Call the functions with your DataFrame and relevant parameters:
```x_chart(df, 'Values', 'Observations', title='Example X-chart')```

## Functions
```bar_chart```
Generate a bar chart with optional bar labels, percentage labels, and target lines. To be used in conjunction with the results from the ```network_analysis``` function. In the context of ```network_analysis``` the function should be used to display the means and process limit ranges (PLRs) from the ```results_df``` of ```network_analysis```.

- **Required Parameters**: `df`, `x_axis_data`, `y_axis_data`
- **Returns**: None. This function does not return any value. It displays a bar chart.
- **Example**: ```bar_chart(network_analysis_results_df, 'LineNum', 'LineValues')```

```delta_chart```
Generate a bar chart that shows the delta (difference) between two sets of values. In the context of DDI this function is to be used specifically to show the delta between the mean and a target value. For best results ```sort_values(by='column_to_sort', ascending=False)```.

- **Required Parameters**: `df`, `x_axis_data`, `y_axis_data`
- **Returns**: None. This function does not return any value. It displays a bar chart.``
- **Example**: ```delta_chart(delta_sorted_results, 'Labels', 'Mean to Tar. Delta')```

```limit_chart```
Generates a time series that displays the values of a data set with the upper and lower specification limits. Values that fall outside the specification limits are highlighted in red. The mean of the data set is also displayed.

- **Required Parameters**: `df`, `values`, `x_labels`, `target`, `USL`, `LSL`
- **Returns**: DataFrame summarizing the parameters associated with the `limit_chart`. Parameters include Mean, Target, Mean to Target Delta, Upper Specification Limit (USL), Lower Specification Limit (LSL), Specification Limit Range (SLR), Number of Values, Number of Values Outside Specification Limits (# Outside Spec), and Percentage of Values Outside Specification Limits (% Outside Spec).
- **Example**: ```limit_chart(socket_df, 'InnerDiameter', 'MeasurementNumber', '5.4','5.6','5.2')```

```x_chart```
Generate an X-chart (Individual Values Chart) from the provided DataFrame. The X-chart is used to characterize a process as either predictable or unpredictable. A predictable process will have all values fall inside the upper and lower process limits. An unpredictable process will have one or more values fall outside the process limits. An unpredictable process is under the influence of assignable causes of variation. To facilitate improvement assignable causes must be identified, understood, and eliminated. Assignble causes of variation are highlighted in red on the X-chart. The function assumes the DataFrame is composed of individual values with an order that is sequential. Scaling factor of C1 = 2.660 is used to calculate the process limits (UPL and LPL). 

- **Required Parameters**: `df`, `values`, `x_labels`
- **Returns**: A dictionary containing DataFrames with calculated parameters and causes:
	-  `PBC Params`: DataFrame with calculated parameters `Mean`, `UPL` (Upper Process Limit), `LPL` (Lower Process Limit), and `PLR` (Process Limit Range).
	- `X-Chart DataFrame`: DataFrame with added column `X-Chart Variation` categorizing causes as `Routine Cause` or `Assignable Cause`.
- **Notes**: 
	 -   For those unfamiliar with process behavior charts (control charts) visit  [CreateHolisticSolutions.com](https://www.createholisticsolutions.com/portfolio). 
- **Example**: ```x_chart(OnTimeDelivery_df, 'OTD Values', 'Month')```

```mr_chart```
Generate an mR-chart (Moving Range Chart) from the provided DataFrame. The mR-chart is the other half of the process behavior chart (control chart). Where the X-chart bounds variation of the individual values, the mR-chart bounds the value-to-value variation. When all values are less than the upper range limit on the mR-chart the process is characterized as predictable. When one or more values is greater than the upper range limit on the mR-chart the process is characterized as unpredictable. When a process is characterized as unpredictable time and attention should work to identify, understand, and eliminate the assignable causes of variation. Assignable causes are values highlighted in red on the mR-chart. Scaling factor of C2 = 3.278 is used to calculate the upper range limit (URL). 

- **Required Parameters**: `df`, `values`, `x_labels`
- **Returns**: A dictionary containing DataFrames with calculated parameters and causes:
	- `PBC Params`: DataFrame with calculated parameters `AmR` (Average Moving Range) and `URL` (Upper Range Limit).
	- `mR-Chart DataFrame`: DataFrame with added column `mR-Chart Variation` categorizing causes as `Routine Cause` or `Assignable Cause`.
- **Notes**: 
	- Function assumes that a column containing the moving range values is present in the provided DataFrame. Moving ranges can be calculated using this code: 
```mRs = abs(df['Values].diff())```. 
	- For those unfamiliar with process behavior charts (control charts) visit [CreateHolisticSolutions.com](https://www.createholisticsolutions.com/portfolio).
- **Example**: ```mr_chart(OnTimeDelivery_df, 'Moving Ranges', 'Month')```

```PBC```
Generates a Process Behavior Chart (control chart) for the provided DataFrame. The XmR-chart, also called an individual values chart, is used to characterize process behavior as either predictable or unpredictable. When one or more values falls outside the upper or lower process limits on the X-chart or is greater than the upper range limit on the mR-chart the process is characterized as unpredictable. When all values fall within the upper and lower process limit and are less than the upper range limit the process is characterized as predictable. Values that fall outside the limits on the X or mR-chart are highlighted red. An unpredictable process is influenced by both routine causes of variation and assignable causes of variation. 

- **Required Parameters**: `df`, `values`, `x_labels`
- **Returns**: A dictionary containing DataFrames with calculated parameters and causes:
	- `PBC Params`: DataFrame with calculated parameters including `Mean`, `UPL` (Upper Process Limit), `LPL` (Lower Process Limit) for X-chart, `PLR` (Process Limit Range), `AmR` (Average Moving Range), and `URL` (Upper Range Limit) for mR-chart.
	- `XmR-Chart Dataframe`: DataFrame with added columns `X-Chart Variation` and `mR-Chart Variation` categorizing causes as `Routine Cause` or `Assignable Cause`.
- **Notes**: 
	- For those unfamiliar with process behavior charts (control charts) visit [CreateHolisticSolutions.com](https://www.createholisticsolutions.com/portfolio).
- **Example**: ```PBC(df, 'Values', 'Observation')```

```network_analysis```
Generates a figure composed of a grid of `process behavior charts` using a list of DataFrames. Each DataFrame is a unique system that performs the same task. As an example, 15 machines making the same part on a manufacturing floor is a good candidate for `network analysis`. Facilitates direct visual comparison of all components in the `network analysis` grid through a shared y-axis. `Network analysis` localizes broad swaths of time and space into a single field of view.

- **Required Parameters**: `df_list`, `condition`, `label_list`
- **Returns**: 
	- `results_df` : DataFrame containing the calculated statistics and predictability characterization for each component (DataFrame) used in the network analysis.
- **Notes**: 
	- The function calculates the `mean`, `average moving range (AmR)`, `upper control limit (UPL)`, `lower control limit (LPL)`, and `upper range limit (URL)` for each DataFrame used in the `network analysis`.
	- The function generates a grid of `PBCs` with a common `y-axis` allowing for direct visual comparison. It also masks values exceeding the process limits.
	- The function determines if the data is `Predictable` or `Unpredictable` based on process limits.
	- For those unfamiliar with process behavior charts (control charts) visit [CreateHolisticSolutions.com](https://www.createholisticsolutions.com/portfolio).
- **Example**: ```network_analysis(list_of_dfs, 'Values', list_of_labels)```

```xchart_comparison```
Generates a figure composed of two `X-charts` using a list of two DataFrames. Each DataFrame represents a unique process state i.e. the baseline process state (before improvement) and the process state after efforts have been made to improve it. Figure facilitates direct visual comparison of process states through the shared y-axis.

 - **Required Parameters**: `df_list`,`condition`,`label_list`
 - **Returns**: `results_df` : DataFrame containing the statistical parameters and characterization results for the two DataFrames that populate the figure.
 - **Notes**: 
	 - Constants C1 and C2 are predefined for control limits calculation.
	- Calculates statistical parameters like Mean moving range (AmR), Upper Range Limit (URL) for each dataset.
	- Determines predictability of each dataset based on control limits.
	- Plots moving range values, mean moving range, and control limits for each dataset on separate subplots.
	- Adjusts subplot spacing and styling for better visualization.
 - **Example**: `xchart_comparison(list_of_dfs, 'Widths', list_of_labels)`

```mrchart_comparison```
Generates a figure composed of two `mR-charts` using a list of two DataFrames. Each DataFrame represents a unique process state i.e. the baseline process state (before improvement) and the process state after efforts have been made to improve it. Figure facilitates direct visual comparison of process states through the shared y-axis.
- **Required Parameters**: `df_list`,`condition`,`label_list`
 **Returns**: `results_df` : DataFrame containing the statistical parameters and characterization results for the two DataFrames that populate the figure.
 - **Notes**: 
	 - Constants C1 and C2 are predefined for control limits calculation.
	- Calculates statistical parameters like Mean moving range (AmR), Upper Range Limit (URL) for each dataset.
	- Determines predictability of each dataset based on control limits.
	- Plots moving range values, mean moving range, and control limits for each dataset on separate subplots.
	- Adjusts subplot spacing and styling for better visualization.
 - **Example**: `mrchart_comparison(list_of_dfs, 'Lengths', list_of_labels)`

## Contributing
To contribute to DataDrivenImprovement, follow these steps:
1. Fork this repository.
2. Create a branch: ```git checkout -b <branch_name>```. 
3. Make your changes and commit them:  ```git commit -m '<commit_message>'```
4. Push to the original branch: ```git push origin <DataDrivenImprovement>/<location>```.
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request). 
## Contact
If you want to contact me you can reach me at [James.Lehner@gmail.com](James.Lehner@gmail.com).
## License
This project uses the following license: MIT License.
## Additional Information
- **Parts of a Process Behavior Chart**: Invented by Dr. Walter Shewhart in the mid-1920s at Bell Laboratories, PBCs are composed of two charts: the `X-chart` and the `mR-chart`. Where the `X-chart` bounds the variation associated with individual values the `mR-chart` bounds the value-to-value variation. This is made possible through the calculation of a trio of limits known as process limits. The `upper process limit (UPL)` and `lower process limit (LPL)` are used on the `X-chart`. The `upper range limit (URL)` is used on the `mR-chart`. 
- **Two types of variation**: Inherent in the characterizations of `predictable` and `unpredictable` is the tyoe of variation action a process. A predictable process is influenced by only `routine` causes of variation. An `unpredictable` process is influenced by both `routine causes of variation` and `assignable` causes of variation.  
- **Improvement**: 
	- **Predictable**: To improve a predictable process `routine` causes of variation must be `identified`, `understood`, and `mitigated`.  This requires fundamental changes to the process must be made. These include, but are not limited to, changes to raw materials, adjustment to system settings, redesign of stations, redesign of software, calibration of measurement systems. 
	- **Unpredictable**: To improve an unpredictable process  `assignable` causes of variation must be `identifed`, `understood`, and `eliminated`. To begin this process, an investigation into values that fall outside the process limits on the `PBC` must be performed. 
- For those unfamiliar with process behavior charts (control charts) that are interested in learning more visit [CreateHolisticSolutions.com](https://www.createholisticsolutions.com/portfolio).
