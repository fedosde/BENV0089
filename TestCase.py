#!/usr/bin/env python
# coding: utf-8

# 
# # Module Code: BENV0089
# # Module Title: Dissertation: Smart Buildings and Digital Engineering
# # UCL Candidate Code: VRMZ4
# # Dissertation Title: A practical application of linked data technologies for thermal comfort and indoor air quality assessment: UCL Student Centre case study
# # TEST CASE: Evaluating IAQ and thermal comfort in selected rooms 

# To demonstrate the value of proposed data integration method, structurally measured and collected data are used to answer the competence questions related to thermal comfort and indoor air quality. 
# 
# -	In which rooms are people more likely to experience thermal discomfort?
# -	In which rooms should the humidity level be regulated using humidifiers / dehumidifiers?
# -	What is quality of the indoor air in study spaces? 
# -	What are the variations of indoor air quality between the spaces? 
# 
# Additionally, in order to evaluate building performance in accordance with the benchmarks from published standards, this data are used to contrast with the requirements of health and well-being-oriented certification tools. 
# These criteria are based on the WELL Building certification standard, since it is a generally accepted prestigious standard focused on creating more thoughtful and comfortable indoor environment that enhance human health and wellbeing. 
# 
# In this study, the data from three study rooms located on different floors are selected for analysis: Social study room “4.01” - on the 4th floor; Café “3.01” – on the 3rd floor; and Group study space “M.02.A” – on the Mezzanine floor. 
# 

# ## Linking timeseries data with metadata

# #### Import libraries required for this task

# In[1]:


import pandas as pd # https://pandas.pydata.org/
import matplotlib.pyplot as plt # https://matplotlib.org/stable/index.html


# #### Criteria used in this study
# This table shows the values of CO2 concentration, PM2.5, relative humidity and temperature, which are used as benchmarks in this study. 

# In[2]:


benchmarks =  pd.read_csv("benchmarks.csv", sep=',', encoding='unicode_escape', parse_dates=True, low_memory=False)
benchmarks


# #### Loading timeseries data from CSV file
# This gets all timeseries data available

# In[3]:


data =  pd.read_csv("CH_ALL_15min_HW.csv", sep=',', encoding='unicode_escape', parse_dates=True, low_memory=False)
data.head()


# The values can be rounded by using the `.round` function. Aditionally, the `Timestamp` comumn can be used as an index, and subsequently, convert in datetime format using `.to_datetime` function.

# In[4]:


data = data.round(2)
df=data.set_index(data['Timestamp']) # set Timestamp column to the index
df.index = pd.to_datetime(df.index) # covert index to datetime format
df # check


# #### Loading the metadata generated from query
# Since GraphDB allows to store the query results in different formats (e.g. JSON, CSV, XML, TSV), there are many ways to load the data in Python. In this particular study, the query results are stored in CSV format and subsequently loaded.

# In[5]:


labels = pd.read_csv("query-result.csv", sep=',', encoding='unicode_escape', parse_dates=True, low_memory=False)
labels


# The area values can be also rounded to display it correctly.

# In[6]:


labels['Area'] = labels['Area'].round(2)
labels.head() # check


# In order to establish the connection between the data from query with timeseries data correctly, the data is linked based on the IDs of devices that collect sensory data. In this study, the `MultiIndex` function is showed to demonstrate how metadata associated with timeseries values.

# In[7]:


# At first, put the data in both datasets in the same order according to the point IDs
order = labels['PointID']
df2 = df[order]
df2.columns = pd.MultiIndex.from_frame(labels)


# In[8]:


df2 # check


# This dataset structures the data in accordance with metadata classes exported from knowledge graph.

# In[9]:


df2.to_csv('linked.csv', index=True)


# These results demonstrate that diverse building data can be extracted and linked. Similar queries can be also used to extract other data from the graph to include additional informatiom about timeseries data, if it is requred. It demonstrates how the proposed data integration approach can be used to retrieve of data and potentially support evaluating IAQ and thermal comfort.

# ## Analysis of the data

# Since the measurements were taken at least once every 15 minutes, which corresponds to the WELL Certification standard, these data can be used for the analysis. 
# 
# At first, it is possible to get a brief description of the contents in the dataset using the `.describe()` function.

# In[10]:


perc =[.10, .20, .50, .80,.90] # The percentiles to include in the output.
df2.describe(percentiles = perc)


# In[11]:


df2.describe(percentiles = perc).to_csv('linked_describe.csv', index=True)


# #### In addition, based on the criteria used in this study, the measured data can be extracted and visualized from each space.

# In[12]:


# organize data for each parameter separately
temp = pd.DataFrame(data, columns = ['CH_418_Temperature', 'CH_416_Temperature', 'CH_413_Temperature'])
rh = pd.DataFrame(data, columns = ['CH_418_Humidity', 'CH_416_Humidity', 'CH_413_Humidity'])
co2 = pd.DataFrame(data, columns = ['CH_418_CO2', 'CH_416_CO2', 'CH_413_CO2'])
pm25 = pd.DataFrame(data, columns = ['CH_418_PM25', 'CH_416_PM25', 'CH_413_PM25'])


# In[13]:


# binding month names to the x axis
y = [0,1,2,3,4,5,6,7,8,9,10,11,12]
x = [int(i)*2920 for i in y] # convert X-axis from minutes to months
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan']


# In[14]:


# Plot temperature data
fig, ax = plt.subplots(figsize=(24, 16))
plt.axhline(y=21, xmin=0, xmax=1, color='k', linestyle=':', linewidth=3)
plt.axhline(y=25, xmin=0, xmax=1, color='k', linestyle=':', linewidth=3)
ax.plot(temp['CH_416_Temperature'], color='#F1C716', label="Room № 4.01")
ax.plot(temp['CH_418_Temperature'], color='#57B956', label="Room № 3.01")
ax.plot(temp['CH_413_Temperature'], color='#EB5757', label="Room № M.02.A")

plt.title("Indoor Air Temperature data", fontsize=30)
plt.xlabel("Dates (months)", fontsize=24)
plt.ylabel("Temperature ($^\circ$C)", fontsize=24)
plt.xticks(x, months, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=24, loc='upper right')
plt.savefig('Indoor Air Temperature data.png')
plt.show()


# In[15]:


# Plot humidity data
fig, ax = plt.subplots(figsize=(24, 16))
plt.axhline(y=30, xmin=0, xmax=1, color='k', linestyle=':', linewidth=3)
plt.axhline(y=60, xmin=0, xmax=1, color='k', linestyle=':', linewidth=3)
ax.plot(rh['CH_416_Humidity'], color='#F1C716', label="Room № 4.01")
ax.plot(rh['CH_418_Humidity'], color='#57B956', label="Room № 3.01")
ax.plot(rh['CH_413_Humidity'], color='#EB5757', label="Room № M.02.A")

plt.title("Relative Humidity data", fontsize=30)
plt.xlabel("Dates (months)", fontsize=24)
plt.ylabel("Relative Humidity (%)", fontsize=24)
plt.xticks(x, months, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=24, loc='upper right')
plt.savefig('Relative Humidity data.png')
plt.show()


# In[16]:


# Plot CO2 data
fig, ax = plt.subplots(figsize=(24, 16))
plt.axhline(y=800, xmin=0, xmax=1, color='k', linestyle=':', linewidth=3)
ax.plot(co2['CH_416_CO2'], color='#F1C716', label="Room № 4.01")
ax.plot(co2['CH_418_CO2'], color='#57B956', label="Room № 3.01")
ax.plot(co2['CH_413_CO2'], color='#EB5757', label="Room № M.02.A")

plt.title("CO2 Concentration data", fontsize=30)
plt.xlabel("Dates (months)", fontsize=24)
plt.ylabel("Concentration (ppm)", fontsize=24)
plt.xticks(x, months, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=24, loc='upper right')
plt.savefig('CO2 Concentration data.png')
plt.show()


# In[17]:


# Plot PM 2.5 data
fig, ax = plt.subplots(figsize=(24, 16))
plt.axhline(y=15, xmin=0, xmax=1, color='k', linestyle=':', linewidth=3)
ax.plot(pm25['CH_416_PM25'], color='#F1C716', label="Room № 4.01")
ax.plot(pm25['CH_418_PM25'], color='#57B956', label="Room № 3.01")
ax.plot(pm25['CH_413_PM25'], color='#EB5757', label="Room № M.02.A")

plt.title("PM2.5 Concentration data", fontsize=30)
plt.xlabel("Dates (months)", fontsize=24)
plt.ylabel("Concentration (µg/m3)", fontsize=24)
plt.xticks(x, months, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=24, loc='upper right')
plt.savefig('PM2.5 Concentration data.png')
plt.show()


# These linked data can be utilised in order to answer the competence questions related to thermal comfort and indoor air quality assessments:
# 
# #### -	In which rooms are people more likely to experience thermal discomfort?
# 
# Temperature fluctuations, as well as high and low air temperatures may create discomfort for occupants. Having reviewed the air temperature measured in three different rooms, it is possible to see that most of the time temperatures were within the acceptable range. However, according to the available data, temperature fluctuations in rooms No. 4.01 and 3.01 occured more often: the air temperature in 3.01 room periodically fell below the minimum acceptable value, while the air temperature in 4.01 room often exceeded 25 ⁰C and fell below 21 ⁰C in summer – autumn period. Furthermore, the temperature spectrum in room No. M.02.A was minimal and averaged 23.8 ⁰C, whereas the temperature in rooms 4.01 and 3.01 dropped to 16 ⁰C and increased to 29 – 33 ⁰C respectively.
# Based on the recommended comfort temperatures provided by the WELL standard and measurements taken in three study rooms, people were more likely to experience thermal discomfort in the room No. 4.01, since temperature flactuations in this space occured more often, reaching a maximum temperature of 33.29 ⁰C and minimum of 16 ⁰C.
# 
# 
# 
# #### -	In which rooms should the humidity level be regulated using humidifiers / dehumidifiers?
# 
# Comparing the humidity levels in these rooms, it can be seen that the humidity level was lower in the winter – spring months than during the summer. Particularly, the mean relative humidity value in rooms No. M.02.A and 3.01 was within the acceptable rate - 51.6 %, but in room No. 4.01 it exceeded the acceptable maximum value – 63.4 %. Furthermore, most of the time (~ 65 %) the relative humidity in the room 4.01 exceeded the WELL standard (60 %). In addition, the humidity levels in rooms No. 3.01 and M.02.A exceeded the recommended value in about 20 % of the measurements, mainly from July to September.
# Having considered the humidity measurements taken in three different study rooms, it is possible to see that dehumidifiers should be used in all three study rooms during the summer – autumn months to decrease the relative humidity rates. 
# 
# 
# 
# #### -	What is quality of the indoor air in study spaces? / What are the variations of indoor air quality between the spaces?
# To evaluate the IAQ in this study, the concentrations of CO2 and PM 2.5 were compared to the WELL Standard. In all rooms, the concentration of PM2.5 in 90% of measurements does not exceed the value recommended by the WELL standard (15 µg/m3). Furthermore, for the most of the time, the factual concentration of PM 2.5 does not exceed 5 µg/m3. 
# With regards to CO2 levels, it can be concluded that in less than 10% of measurments, the CO2 levels in rooms No. 4.01 and 3.01 exceed the recommended concentration. As shown in Figure 28, the CO2 concentration in all three rooms periodically exceeds 800 ppm throughout the year and increases more significantly in summer and in November - December. This may be caused by the high occupancy of the study areas before the official deadlines for student papers, since closer to the Christmas holidays, the level of CO2 and PM 2.5 becomes minimal. It is also possible to see in Table 5 that the maximum peak concentration of CO2 was in room 4.01, which accounted for 3942 ppm. 
# It can also be seen that fluctuations in the levels of CO2 and PM2.5 in different rooms have the same pattern, i.e. when the concentration of PM 2.5 increases in room 3.01, it is more likely that it is also increases in room M.02.A. However, there are several singular peaks in the concentration of PM 2.5, in particular in rooms No. 4.01 and 3.01, which have a large area, and are designed for a large number of students.
# Having observed the levels of CO2 and PM 2.5 in thee study spaces involved in this study, it is possible to see that both parameters are mostly within the acceptable range provided by the WELL standard: 
# -	For the most of the time, the factual concentration of PM 2.5 does not exceed 5 µg/m3;
# -	Although, the CO2 concentration in all three rooms periodically exceeds 800 ppm, the annual mean CO2 concentration does not exceed 590 ppm.
# 

# ### Variations of indoor air quality in study spaces during a typical day/ week/ year

# This linked data set also provides an oppotunity to evaluate variations of indoor air quality in study spaces during the typical days and weeks, the PM 2.5 and CO2 levels can be also examined for summer and winter typical weeks, which were selected based on availability of measured data in all three rooms:
# 
# Summer typical week: 17.07.2017 – 23.07.2017
# 
# Winter typical week: 18.12.2017 – 24.12.2017
# 

# In[18]:


df_stw = df.loc['2017-07-17 00:00':'2017-07-24 00:00'] 
df_wtw = df.loc['2017-12-18 00:00':'2017-12-25 00:00'] 


# #### PM 2.5 concentration (summer / winter typical weeks)

# In[19]:


# Plot PM 2.5 Concentration data (typical summer week)
fig, ax = plt.subplots(figsize=(24, 16))
plt.axhline(y=15, xmin=0, xmax=1, color='k', linestyle=':', linewidth=3)
ax.plot(df_stw['CH_416_PM25'], color='#F1C716', label="Room № 4.01")
ax.plot(df_stw['CH_418_PM25'], color='#57B956', label="Room № 3.01")
ax.plot(df_stw['CH_413_PM25'], color='#EB5757', label="Room № M.02.A")

plt.title("PM2.5 Concentration data (typical summer week)", fontsize=30)
plt.xlabel("Dates (days)", fontsize=24)
plt.ylabel("Concentration (µg/m3)", fontsize=24)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=24, loc='upper right')
#plt.savefig('PM2.5 Concentration data (typical summer week).png')
plt.show()


# In[20]:


# Plot PM 2.5 Concentration data (typical winter week)
fig, ax = plt.subplots(figsize=(24, 16))
plt.axhline(y=15, xmin=0, xmax=1, color='k', linestyle=':', linewidth=3)
ax.plot(df_wtw['CH_416_PM25'], color='#F1C716', label="Room № 4.01")
ax.plot(df_wtw['CH_418_PM25'], color='#57B956', label="Room № 3.01")
ax.plot(df_wtw['CH_413_PM25'], color='#EB5757', label="Room № M.02.A")

plt.title("PM2.5 Concentration data (typical winter week)", fontsize=30)
plt.xlabel("Dates (days)", fontsize=24)
plt.ylabel("Concentration (µg/m3)", fontsize=24)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=24, loc='upper right')
#plt.savefig('PM2.5 Concentration data (typical winter week).png')
plt.show()


# 
# 
# Based on the PM 2.5 concentration levels illustrated for typical summer and winter weeks, it is possible to see the the PM 2.5 level does not exceed the recommended value of 15 µg/m3. Despite that there is a peak of PM 2.5 level in room 4.01 in summer. In addition, based on the values on the graphs, it can be seen that for the most of the time fluctuations occur with the same behavior in all rooms.

# #### CO2 concentration (summer / winter typical weeks)

# In[21]:


# Plot CO2 Concentration data (typical summer week)
fig, ax = plt.subplots(figsize=(24, 16))
plt.axhline(y=800, xmin=0, xmax=1, color='k', linestyle=':', linewidth=3)
ax.plot(df_stw['CH_416_CO2'], color='#F1C716', label="Room № 4.01")
ax.plot(df_stw['CH_418_CO2'], color='#57B956', label="Room № 3.01")
ax.plot(df_stw['CH_413_CO2'], color='#EB5757', label="Room № M.02.A")

plt.title("CO2 Concentration data (typical summer week)", fontsize=30)
plt.xlabel("Dates (days)", fontsize=24)
plt.ylabel("Concentration (ppm)", fontsize=24)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=24, loc='upper right')
#plt.savefig('CO2 Concentration data (typical summer week).png')
plt.show()


# In[22]:


# Plot CO2 Concentration data (typical winter week
fig, ax = plt.subplots(figsize=(24, 16))
plt.axhline(y=800, xmin=0, xmax=1, color='k', linestyle=':', linewidth=3)
ax.plot(df_wtw['CH_416_CO2'], color='#F1C716', label="Room № 4.01")
ax.plot(df_wtw['CH_418_CO2'], color='#57B956', label="Room № 3.01")
ax.plot(df_wtw['CH_413_CO2'], color='#EB5757', label="Room № M.02.A")

plt.title("CO2 Concentration data (typical winter week)", fontsize=30)
plt.xlabel("Dates (days)", fontsize=24)
plt.ylabel("Concentration (ppm)", fontsize=24)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=24, loc='upper right')
#plt.savefig('CO2 Concentration data (typical winter week).png')
plt.show()


# 
# These figures illustrate the CO2 concentrations in three rooms during summer and winter typical weeks respectively. It is possible to see that during occupied hours the concentration significantly increases and often exceeds the recommended value:
# -	During the summer typical week, concentration of CO2 in room M.02.A is within the acceptable range;
# -	Concentration of CO2 in room 3.01 periodicaly goes above the benchmark during week days;
# -	Concentration of CO2 in room 4.01 drastically increases almost every day. 
# However, during the winter, concentration of CO2 in all rooms had approximatelly the same values and fluctuations occur with the same behavior.
# 

# ##### The analysis of the measured data performed in this study is demonstrative and takes into account measurements that were carried out at least once every 15 minutes only on an annual basis and for typical summer / winter weeks. In practice, the analysis of thermal comfort and IAQ can be performed in more detail.

# In[ ]:




