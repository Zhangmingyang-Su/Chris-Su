# Databricks notebook source
# MAGIC %md
# MAGIC ## Baltimore crime data analysis and modeling 

# COMMAND ----------

# MAGIC %md #### (https://query.data.world/s/axat2ortbtqqehhtmfwuaz4hffkujp). 

# COMMAND ----------

# DBTITLE 1,Import package 
from csv import reader
from pyspark.sql import Row 
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import warnings

import os
os.environ["PYSPARK_PYTHON"] = "python3"


# COMMAND ----------

# download dataset 
import urllib.request
urllib.request.urlretrieve("https://query.data.world/s/uwn5462sauinmmmg3kkmalm2expvnx", "/tmp/my123.csv")
dbutils.fs.mv("file:/tmp/my123.csv", "dbfs:/chris/spark_hw1/data/Baltimore_03_18.csv")
display(dbutils.fs.ls("dbfs:/chris/spark_hw1/data/"))


# COMMAND ----------

data_path = "dbfs:/chris/spark_hw1/data/Baltimore_03_18.csv"
# use this file name later

# COMMAND ----------

# DBTITLE 1,Get dataframe and sql

from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("crime analysis") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

df_opt1 = spark.read.format("csv").option("header", "true").load(data_path)
display(df_opt1)
df_opt1.createOrReplaceTempView("Baltimore_crime")

 
# from pyspark.sql.functions import to_date, to_timestamp, hour
# df_opt1 = df_opt1.withColumn('Date', to_date(df_opt1.OccurredOn, "MM/dd/yy"))
# df_opt1 = df_opt1.withColumn('Time', to_timestamp(df_opt1.OccurredOn, "MM/dd/yy HH:mm"))
# df_opt1 = df_opt1.withColumn('Hour', hour(df_opt1['Time']))
# df_opt1 = df_opt1.withColumn("DayOfWeek", date_format(df_opt1.Date, "EEEE"))

#from pyspark.sql.functions import col, udf
#from pyspark.sql.functions import expr
#from pyspark.sql.functions import from_unixtime

#date_func =  udf (lambda x: datetime.strptime(x, '%m/%d/%Y'), DateType())
#month_func = udf (lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%Y/%m'), StringType())

#df = df_opt1.withColumn('month_year', month_func(col('Date')))\
#           .withColumn('Date_time', date_func(col('Date')))
# select Date, substring(Date,7) as Year, substring(Date,1,2) as Month from sf_crime

from pyspark.sql.functions import *
df_update = df_opt1.withColumn("CrimeDate", to_date(col("CrimeDate"), "MM/dd/yyyy")) ##change datetype from string to date
df_update.createOrReplaceTempView("Baltimore_crime")
crimeYearMonth = spark.sql("SELECT Year(Date) AS Year, Month(Date) AS Month, FROM Baltimore_crime")

# COMMAND ----------

# MAGIC %md ### 1. Data Cleaning and Exploration

# COMMAND ----------

# transfer from spark sql into pandas Dataframe
Baltimore_crime= df_opt1.toPandas()
Baltimore_crime.head(10)


# COMMAND ----------

# Data information
Baltimore_crime.info()

# COMMAND ----------

# check data dimension information
print ("Num of rows: " + str(Baltimore_crime.shape[0])) 
print ("Num of columns: " + str(Baltimore_crime.shape[1]))

# COMMAND ----------

# check all the missing value
Baltimore_crime.isnull().sum()

# COMMAND ----------

Baltimore_crime.nunique()

# COMMAND ----------

# becasue in the Weapon column, the missing value more than 60% of the sample numbers, then drop it.
drop_columns = ['Weapon']
X = Baltimore_crime.drop(drop_columns, axis=1)
X.head(10)

# COMMAND ----------

# drop missing value
X_new = X.dropna()
X_new.head(10)

# COMMAND ----------

# data shape after drop missing value
print ("Num of rows after drop missing value: " + str(X_new.shape[0])) 
print ("Num of columns after drop missing value: " + str(X_new.shape[1]))

# COMMAND ----------

# from the opration below, we find there are some uncommon data type in the CrimeTime column
column = X_new["CrimeTime"]
new_column = column.to_list()
for i in range(len(new_column)):
  if len(new_column[i]) != 8:
    new_column[i] = None
Crime_Time = pd.Series(new_column)
X_new['Crime_Time'] = Crime_Time
X_new.head()


# COMMAND ----------

# becasue in the previous CrimeTime column, there are many uncommon data type, so we need to drop it.
drop_columns = ['CrimeTime']
X = X_new.drop(drop_columns, axis=1)
X.head(10)

# COMMAND ----------

# drop missing value
X = X.dropna()
X.head(10)

# COMMAND ----------

# get the shape after drop uncommon data type
print ("Num of rows after drop uncommon data type: " + str(X.shape[0])) 
print ("Num of columns after drop uncommon data type: " + str(X.shape[1]))

# COMMAND ----------

# transfer from pandas dataframe into spark dataframe
spark_df = sqlContext.createDataFrame(X)
spark_df.show()

# COMMAND ----------

# create sql envrionment 
spark_df.createOrReplaceTempView("Baltimore_crime_table")

# COMMAND ----------

# change date type because of the transformation
from pyspark.sql.functions import *
df_update = spark_df.withColumn("CrimeDate", to_date(col("CrimeDate"), "MM/dd/yyyy")) ##change datetype from string to date
df_update.createOrReplaceTempView("Baltimore_crime_table")

# COMMAND ----------

# MAGIC %md ### 2. Data Analysis

# COMMAND ----------

# MAGIC %md ##### Write a Spark program that counts the number of crimes for different category. 

# COMMAND ----------

# DBTITLE 1,Spark dataframe based solution 
q1_result = spark_df.groupBy('Description').count().orderBy('count', ascending=False)
display(q1_result)

# COMMAND ----------

# DBTITLE 1,Spark SQL based solution
#Spark SQL based
crimeCategory = spark.sql("SELECT  Description, COUNT(*) AS Count FROM Baltimore_crime_table GROUP BY 1 ORDER BY 2 DESC")
display(crimeCategory)

# COMMAND ----------

# MAGIC %md #### Counts the number of crimes for different district, and visualize your results

# COMMAND ----------

crime_nums = spark.sql("SELECT District, count(*) as count from Baltimore_crime_table group by 1 order by 2 DESC")
display(crime_nums)

# COMMAND ----------

# MAGIC %md Count the number of crimes at "Baltimore downtown".   
# MAGIC  

# COMMAND ----------

# check the google map, we find that downtwon area of Baltimore located between(39.28, -76.62) to (39.32, -76.58)
down_town = X["Location 1"]
count = 0
for data in down_town:
    x1 = float(data[1:14])
    y1 = float(data[16:29])
    if 39.28 <= x1 <= 39.32 and -76.62 <= y1 <= -76.58:
      count += 1
print("the total numbers of crime in downtown Baltimore: " + str(count))

# COMMAND ----------

# MAGIC %md #### Analysis the number of crime in each month of year (2011-2016). Then, give your insights for the output results. What is the business impact for your result?  

# COMMAND ----------

crimeYearMonth = spark.sql("SELECT Year(CrimeDate) as year, Month(CrimeDate) as month, count(*) as nums FROM Baltimore_crime_table GROUP BY 1, 2 ORDER BY 1, 2")
display(crimeYearMonth)

# COMMAND ----------

# from this table, the crime numbers are lowerst in December of each year, it means that criminal may stay at home more frequently than any other month because of the incoming Christmars Day. So for many Brick-and-mortar store, the owner can open store longer than usual before Christmars Day to get more profit.  

# COMMAND ----------

# MAGIC %md #### Analysis the number of crime w.r.t the hour in certian day like 2013/12/15, 2014/12/15, 2015/12/15. Then, give your travel suggestion to visit Baltimore. 

# COMMAND ----------

crime_nums_2013= spark.sql("SELECT Crime_Time, count (*) as nums FROM Baltimore_crime_table where CrimeDate in (to_date('12/15/2013','MM/dd/yyyy')) group by 1 order by 1")
display(crime_nums_2013)

# COMMAND ----------

crime_nums_2014= spark.sql("SELECT Crime_Time, count (*) as nums FROM Baltimore_crime_table where CrimeDate in (to_date('12/15/2014','MM/dd/yyyy')) group by 1 order by 1")
display(crime_nums_2014)

# COMMAND ----------

crime_nums_2015= spark.sql("SELECT Crime_Time, count (*) as nums FROM Baltimore_crime_table where CrimeDate in (to_date('12/15/2015','MM/dd/yyyy')) group by 1 order by 1")
display(crime_nums_2015)

# COMMAND ----------

# from the visualization analysis, we can see that crime numbers are higher than any other time from 19:00 to 22:00. So visitors should avoid of being there from 19:00 to 22.00, and the total crime numbers increase from 2013-2015.

# COMMAND ----------

# MAGIC %md #### Find out the top-3 danger disrict

# COMMAND ----------

top3_crime_number = spark.sql("SELECT District, count(*) as count From Baltimore_crime_table Group by 1 order by 2 DESC limit 3")
display(top3_crime_number)

# COMMAND ----------

# MAGIC %md #### For different category of crime, find the percentage of crime type. Based on the output, give your hints to adjust the policy.

# COMMAND ----------

crime_type = X["Inside/Outside"]
count = 0
for cnt in crime_type:
  if cnt == "I":
    count += 1
print("The percentage of Inside crime type:" + str(count/len(crime_type)))
print("The percentage of Outside crime type:" + str(1 - count/len(crime_type)))

# COMMAND ----------

# based on this output, the inside crime rate and outside crime rate almost the same, so the policy should balance the number of police between community and public place.

# COMMAND ----------

# MAGIC %md #### Conclusion. 

# COMMAND ----------

# 1. This is a crime analysis project, which focus on analyzing crime trend and factors which influence the crime rate in Baltimore.
# 2. This data set comes from public resources in Washington DC, which records the crime information from 2011-2016.
# 3. This is an unstructured data set, so i need to deal with it by building data pipeline to further analyze.
# 4. I set up 3 main steps for data cleaning and exploration, data analysis, data modeling and visualization.
# 5. First of all, i use spark datasframe to create table and set up environment, and then transfer to Pandas dataframe to understand data information, slove missing value and uncommon data type information. Secondly, i use Spark SQL to analyze crime numbers with respect to different features and get some significant insights. Finally, i use Spark ML to build clustering model to visualize the results by clustering the data set.
# 6. By analyzing the data set, i draw a conclusion that visitors need to choose suitable time to go to Baltimore avoid time from 19:00 to 22:00. At the same time, i don't suggest visitors to go to the northeastern, southeastern, central street and some adjacent locations from clustering result. But for the owners of the stores, i suggset that they can open longer to make more money, and people can invite their family members to their house to a enjoy good time in December. Additionally, downtown is safer than any other places in Baltimore. 

# COMMAND ----------

# MAGIC %md ### 3. Modeling

# COMMAND ----------

from pyspark.sql.types import DoubleType
changedTypedf = spark_df.withColumn("Post", spark_df["Post"].cast(DoubleType()))
changedTypedf.show()

# COMMAND ----------

from pyspark.ml.feature import VectorAssembler
vecAssembler = VectorAssembler(inputCols=["Post"], outputCol="features")
new_df = vecAssembler.transform(changedTypedf)
new_df.show()

# COMMAND ----------

from pyspark.ml.clustering import KMeans

kmeans = KMeans(k=3, seed=1)  # 3 clusters here
model = kmeans.fit(new_df.select('features'))

# COMMAND ----------

transformed = model.transform(new_df)
transformed.show() 

# COMMAND ----------

# Shows the result.
centers = model.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)

# COMMAND ----------

transformed.createOrReplaceTempView("New_Baltimore_crime_table")

# COMMAND ----------

# data visualization for the crime numbers in diffrent post (adjacent location) clusters.
clustering_group = spark.sql("SELECT prediction as cluster, count(*) as count from New_Baltimore_crime_table group by prediction")
display(clustering_group)
