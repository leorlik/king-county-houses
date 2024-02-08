## Data Analysis of the King County House Sales dataset

In the [notebook](https://github.com/leorlik/king-county-houses/blob/main/Notebooks/Data%20Analysis%20House%20Prices.ipynb) in this directory, it was maded a data analysis of the [King County House Sales Dataset](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction). The dataset contains 21576 data samples of house sales between May, 02, 2014 and May, 27, 2015 in King County, USA, with 175 houses appearing 2 times in the dataset (which means 2 sales of the same house) and one house appearing 3 times. The chart below shows how many sales happened per month.

[]() Chart of month sales

Even though May seems the strongest month for sales, with 2414 sales, there's an intersection between 2014 and 2015 sales in this month. When taking that under consideration, May, 2014 had 1768 sales, while May, 2015 had only 646 sales. Thats a average 1207 sales in may (with May, 1st, 2014 and after May 27th, 2015 not considered). The mean value of the house prices does not seems to vary significantly for the month the sale took place, as the chart below shows.

[]() Average Price of monthly sales

When talking about the year of the sale, comparing by years isn't fair since the 2014 year counts 8 months and the 2015 year has only 5 months in it's scope. However, a way of comparing those years is by average sales per month. As the bar chart below shows, 2014 has an average 1827,1 sales per month, while the next year got 1396.

[]() Chart Avg sales

While it could be seem like the house sales market had more sucess in 2014 than 2015, this could also mean that sales in the second half of the year happen more than in the first (since the 2014 samples mostly cover this half). A way of visually confirm this is looking at the seasons of the year.

[]() Seasonal sales chart

It's still worth to remind the spring intersection in May, still doesn't change the fact that part of the spring sales are in 2014. Besides that, it's hard to categorize Spring sales since the intersection and none of the year has a full spring time range. Mostly of the sales in a year actually seems to take place in summer (6231) while the autumn sales are stronger than the winter ones. Autumn and summer are both in the 2014 samples, and most of the winter and spring are in the 2015 year samples, making the idea of mostly sales happening in the summer a stronger hunch. Lets take a look at the average and middle prices of the sales by season.

[]() Mean and median

The mean and median of the sales are bigger in spring, followed by the summer. This could either means that real state brokers can reach bigger saler values in hot seasons or the profile of the houses that sells in these seasons are more expensive than the other ones.  

### Excluded Data

The data samples that were excluded from the analysis are:

- A sample that has 33 bedrooms and 1620 square feet;
- Samples with 0 bathrooms;

Its weird a house with that many bedrooms, specially with the low square feet, and also houses with 0 bathrooms. With that in mind, 11 rows were excluded. 

### Correlation of the variables

The top 10 variables correlation matrix shows us that price has high or average direct correlation with sqft\_living, grade, sqft\_above, sqft\_living15, bathrooms and view (the last one rounded from 0.397). Not only that, but this matrix also shows that the top 5 correlated variables has some correlation between then. Taken this into account, probably the variable creation process shouldn't been focused between these variables.

### House prices

[]() House Prices Histogram

The histogram shows that mostly houses has prices between 75 and 1142 thousand dollars, with a bigger concentration between 227.5 and 532 thousand dollars. Since the distribution isn't clear, couldn't fit a statistical distribution like norm or such. 

The prices of the sales vary between 75 and 7700 thousand dollars, with a mean of 5400.9 thousands and a median of 4500 thousand (similar with what whas shown in the month and seasons bar plots). The standard deviation is very high (3671.28), meaning the data is very sparse, specially because of the outliers. 

### Analysing the variables

#### Condition and View

Below, the pie charts show the percentage distribution of both condition and view variables.

[]() Pie Chart View and condition

Mostly data samples has a 0 view value, which means the view of mostly houses isn't great, but could also means that the majority of the views weren't rated, so the default value was 0. Maybe that variable should'nt be taken into account. Below, the scatter plot of those variables show that their possible correlation with the price isn't direct.

[]() Scatter plot view and condition

#### Bedrooms and Grade

Below, the histograms shows the distribution of the variables bedrooms and grade.

[]()bedrooms and grade histogram



### Continuous Variables
