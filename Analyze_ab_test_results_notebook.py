#!/usr/bin/env python
# coding: utf-8

# # Analyze A/B Test Results 
# 
# This project will assure you have mastered the subjects covered in the statistics lessons. We have organized the current notebook into the following sections: 
# 
# - [Introduction](#intro)
# - [Part I - Probability](#probability)
# - [Part II - A/B Test](#ab_test)
# - [Part III - Regression](#regression)
# - [Final Check](#finalcheck)
# - [Submission](#submission)
# 
# 
# 
# <a id='intro'></a>
# ## Introduction
# 
# A/B tests are very commonly performed by data analysts and data scientists. For this project, you will be working to understand the results of an A/B test run by an e-commerce website.  Your goal is to work through this notebook to help the company understand if they should:
# - Implement the new webpage, 
# - Keep the old webpage, or 
# - Perhaps run the experiment longer to make their decision.
# 
# <a id='probability'></a>
# ## Part I - Probability
# 
# To get started, let's import our libraries.

# In[1]:


import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
#We are setting the seed to assure you get the same answers on quizzes as we set up
random.seed(42)


# ### ToDo 1.1
# Now, read in the `ab_data.csv` data. Store it in `df`. Below is the description of the data, there are a total of 5 columns:
# 
# <center>
# 
# |Data columns|Purpose|Valid values|
# | ------------- |:-------------| -----:|
# |user_id|Unique ID|Int64 values|
# |timestamp|Time stamp when the user visited the webpage|-|
# |group|In the current A/B experiment, the users are categorized into two broad groups. <br>The `control` group users are expected to be served with `old_page`; and `treatment` group users are matched with the `new_page`. <br>However, **some inaccurate rows** are present in the initial data, such as a `control` group user is matched with a `new_page`. |`['control', 'treatment']`|
# |landing_page|It denotes whether the user visited the old or new webpage.|`['old_page', 'new_page']`|
# |converted|It denotes whether the user decided to pay for the company's product. Here, `1` means yes, the user bought the product.|`[0, 1]`|
# </center>
# Use your dataframe to answer the questions in Quiz 1 of the classroom.
# 
# 
# 
# **a.** Read in the dataset from the `ab_data.csv` file and take a look at the top few rows here:

# In[2]:


df =pd.read_csv("ab_data.csv")
df.head()


# **b.** Use the cell below to find the number of rows in the dataset.

# In[3]:


df.shape[0]


# **c.** The number of unique users in the dataset.

# In[4]:


unique = df["user_id"].unique()
unique.shape


# **d.** The proportion of users converted.

# In[5]:


df["converted"].mean()


# **e.** The number of times when the "group" is `treatment` but "landing_page" is not a `new_page`.

# In[6]:


a = df[df["group"] == "treatment"]
b = a[a["landing_page"] == "old_page"]
b.shape[0]


# **f.** Do any of the rows have missing values?

# In[7]:


df.isnull().sum()
# No missing values


# ### ToDo 1.2  
# In a particular row, the **group** and **landing_page** columns should have either of the following acceptable values:
# 
# |user_id| timestamp|group|landing_page|converted|
# |---|---|---|---|---|
# |XXXX|XXXX|`control`| `old_page`|X |
# |XXXX|XXXX|`treatment`|`new_page`|X |
# 
# 
# It means, the `control` group users should match with `old_page`; and `treatment` group users should matched with the `new_page`. 
# 
# However, for the rows where `treatment` does not match with `new_page` or `control` does not match with `old_page`, we cannot be sure if such rows truly received the new or old wepage.  
# 
# 
# 
# **a.** Now use the answer to the quiz to create a new dataset that meets the specifications from the quiz.  Store your new dataframe in **df2**.

# In[8]:


# Remove the inaccurate rows, and store the result in a new dataframe df2
df2 = df[((df["group"] == "treatment") & (df["landing_page"] == "new_page")) | 
        ((df["group"] == "control") & (df["landing_page"] == "old_page"))]


# In[9]:


# Double Check all of the incorrect rows were removed from df2 - 
# Output of the statement below should be 0
df2[((df2['group'] == 'treatment') == (df2['landing_page'] == 'new_page')) == False].shape[0]


# ### ToDo 1.3  
# Use **df2** and the cells below to answer questions for **Quiz 3** in the classroom.

# **a.** How many unique **user_id**s are in **df2**?

# In[10]:


df2["user_id"].nunique()


# **b.** There is one **user_id** repeated in **df2**.  What is it?

# In[11]:


df2[df2["user_id"].duplicated()]


# **c.** Display the rows for the duplicate **user_id**? 

# In[12]:


df2[df2["user_id"] == 773192 ]


# **d.** Remove **one** of the rows with a duplicate **user_id**, from the **df2** dataframe.

# In[13]:


# Remove one of the rows with a duplicate user_id..
# Hint: The dataframe.drop_duplicates() may not work in this case because the rows with duplicate user_id are not entirely identical. 
df2.drop(labels=2893, axis=0, inplace= True )
# Check again if the row with a duplicate user_id is deleted or not


# In[14]:


df2[df2["user_id"].duplicated()]


# ### ToDo 1.4  
# Use **df2** in the cells below to answer the quiz questions related to **Quiz 4** in the classroom.
# 
# **a.** What is the probability of an individual converting regardless of the page they receive?<br><br>
# 
# 
# 

# In[15]:


df2["converted"].mean()


# **b.** Given that an individual was in the `control` group, what is the probability they converted?

# In[16]:


# the probability that user converted if he he was in conrol group

conv1 =df2[df2["group"] == "control"]["converted"].mean()
conv1


# **c.** Given that an individual was in the `treatment` group, what is the probability they converted?

# In[17]:


conv2 =df2[df2["group"] == "treatment"]["converted"].mean()
conv2


# In[18]:


# Calculate the actual difference (obs_diff) between the conversion rates for the two groups.
# differnce between treatmeny group and control group
obs_diff = conv2-conv1
print(obs_diff)


# **d.** What is the probability that an individual received the new page?

# In[19]:


# the probability that the user recevied the new page 
(df2.landing_page == "new_page").mean()


# **e.** Consider your results from parts (a) through (d) above, and explain below whether the new `treatment` group users lead to more conversions.

# **conclusion**
# 
# **the probability that a user in control converted is at higher probability about .12**
# 
# **and the probability a user in treatment group convert is about .11**
# 
# **the obs_difference between them is -0.00157823898536**
# 
# **the probability that the user recevied the new page is 0.5 which mean half of users will recieve the new page**

# <a id='ab_test'></a>
# ## Part II - A/B Test
# 
# Since a timestamp is associated with each event, you could run a hypothesis test continuously as long as you observe the events. 
# 
# However, then the hard questions would be: 
# - Do you stop as soon as one page is considered significantly better than another or does it need to happen consistently for a certain amount of time?  
# - How long do you run to render a decision that neither page is better than another?  
# 
# These questions are the difficult parts associated with A/B tests in general.  
# 
# 
# ### ToDo 2.1
# For now, consider you need to make the decision just based on all the data provided.  
# 
# > Recall that you just calculated that the "converted" probability (or rate) for the old page is *slightly* higher than that of the new page (ToDo 1.4.c). 
# 
# If you want to assume that the old page is better unless the new page proves to be definitely better at a Type I error rate of 5%, what should be your null and alternative hypotheses (**$H_0$** and **$H_1$**)?  
# 
# You can state your hypothesis in terms of words or in terms of **$p_{old}$** and **$p_{new}$**, which are the "converted" probability (or rate) for the old and new pages respectively.

# $$
# H_0 : p_{new} - p_{old} \leq 0 \\
# H_1 : p_{new} - p_{old} > 0
# $$
# 
# **$H_0$** is the null hypothesis **the old page better than the new page**
# 
# **$H_1$** is the alternativee hypothesis **the new page is better than the old page**

# ### ToDo 2.2 - Null Hypothesis $H_0$ Testing
# Under the null hypothesis $H_0$, assume that $p_{new}$ and $p_{old}$ are equal. Furthermore, assume that $p_{new}$ and $p_{old}$ both are equal to the **converted** success rate in the `df2` data regardless of the page. So, our assumption is: <br><br>
# <center>
# $p_{new}$ = $p_{old}$ = $p_{population}$
# </center>
# 
# In this section, you will: 
# 
# - Simulate (bootstrap) sample data set for both groups, and compute the  "converted" probability $p$ for those samples. 
# 
# 
# - Use a sample size for each group equal to the ones in the `df2` data.
# 
# 
# - Compute the difference in the "converted" probability for the two samples above. 
# 
# 
# - Perform the sampling distribution for the "difference in the converted probability" between the two simulated-samples over 10,000 iterations; and calculate an estimate. 
# 
# 
# 
# Use the cells below to provide the necessary parts of this simulation.  You can use **Quiz 5** in the classroom to make sure you are on the right track.

# **a.** What is the **conversion rate** for $p_{new}$ under the null hypothesis? 

# In[20]:


# the conversion rate for p_new under the null hypothesis that says p_old = p_new = p_population
p_new = df2["converted"].mean()
p_new


# **b.** What is the **conversion rate** for $p_{old}$ under the null hypothesis? 

# In[21]:


p_old = df2["converted"].mean()
p_old


# **c.** What is $n_{new}$, the number of individuals in the treatment group? <br><br>
# 

# In[22]:


# number of users in treatment group landing the new page
n_new = df2.query('group == "treatment"')["user_id"].count()
n_new


# **d.** What is $n_{old}$, the number of individuals in the control group?

# In[23]:


# number of users in control group having old page
n_old = df2.query('group == "control"')["user_id"].count()
n_old


# **e. Simulate Sample for the `treatment` Group**<br> 
# Simulate $n_{new}$ transactions with a conversion rate of $p_{new}$ under the null hypothesis.  <br><br>
# 

# In[24]:


# Simulate a Sample for the treatment Group
new_page_converted = np.random.choice([0,1], n_new, p = [1-p_new, p_new])
new_page_converted.mean()


# **f. Simulate Sample for the `control` Group** <br>
# Simulate $n_{old}$ transactions with a conversion rate of $p_{old}$ under the null hypothesis. <br> Store these $n_{old}$ 1's and 0's in the `old_page_converted` numpy array.

# In[25]:


# Simulate a Sample for the control Group
old_page_converted = np.random.choice([0,1], n_old, p = [1-p_old, p_old])
old_page_converted.mean()


# **g.** Find the difference in the "converted" probability $(p{'}_{new}$ - $p{'}_{old})$ for your simulated samples from the parts (e) and (f) above. 

# In[26]:


# to dind the difference between converted prob new and old
differnce = new_page_converted.mean()- old_page_converted.mean()
differnce


# 
# **h. Sampling distribution** <br>
# Re-create `new_page_converted` and `old_page_converted` and find the $(p{'}_{new}$ - $p{'}_{old})$ value 10,000 times using the same simulation process you used in parts (a) through (g) above. 
# 
# <br>
# Store all  $(p{'}_{new}$ - $p{'}_{old})$  values in a NumPy array called `p_diffs`.

# In[27]:


# Sampling distribution 
p_diffs = []
for i in range (10000):
    new_page_converted = np.random.choice([0,1], n_new, p = [1-p_new, p_new])
    old_page_converted = np.random.choice([0,1], n_old, p = [1- p_old, p_old])
    p_diffs.append(new_page_converted.mean() - old_page_converted.mean())


# **i. Histogram**<br> 
# Plot a histogram of the **p_diffs**.  Does this plot look like what you expected?  Use the matching problem in the classroom to assure you fully understand what was computed here.<br><br>
# 
# Also, use `plt.axvline()` method to mark the actual difference observed  in the `df2` data (recall `obs_diff`), in the chart.  
# 

# In[28]:


plt.hist(p_diffs)
plt.axvline(x = obs_diff, color = "r")
plt.title("P_differnece")
plt.xlabel("differnce in pages")
plt.ylabel("count")


# **j.** What proportion of the **p_diffs** are greater than the actual difference observed in the `df2` data?

# In[29]:


(p_diffs >= obs_diff).mean()


# **k.** Please explain in words what you have just computed in part **j** above.  
#  - What is this value called in scientific studies?  
#  - What does this value signify in terms of whether or not there is a difference between the new and old pages? *Hint*: Compare the value above with the "Type I error rate (0.05)". 

# **Answer:** .
# **we call this value in scientific studies as p value.**
# 
# **The lower the p-value (below the Type I error rate threshold of 0.05), the greater the statistical significance of the observed difference, and the more likely we are to reject the null hypothesis in favor of the alternative hypothesis.
# The statistical significance of the observed difference decreases as the p-value rises (beyond the threshold Type I error rate; = 0.05), and the null hypothesis is not rejected.**
# 
# 
#  the probability of not observing any difference between convertion rates of control and treatment groups if the null hypothesis is true. 
#  The p-value must be less than 0.05 in order to reject the null hypothesis (agreed level of 5 percent chance of committing a Type I error if the null is true). In our example, the determined p-value is 0.90339999999999998, which is too high for us to reject the null hypothesis
# 
#    **There is insufficient information to claim that the new and old pages are converted differently.**

# 
# 
# **l. Using Built-in Methods for Hypothesis Testing**<br>
# We could also use a built-in to achieve similar results.  Though using the built-in might be easier to code, the above portions are a walkthrough of the ideas that are critical to correctly thinking about statistical significance. 
# 
# Fill in the statements below to calculate the:
# - `convert_old`: number of conversions with the old_page
# - `convert_new`: number of conversions with the new_page
# - `n_old`: number of individuals who were shown the old_page
# - `n_new`: number of individuals who were shown the new_page
# 

# In[30]:


import statsmodels.api as sm

# number of conversions with the old_page
convert_old = df2[(df2.landing_page == 'old_page') & (df2.converted == 1)].shape[0]

# number of conversions with the new_page
convert_new = df2[(df2.landing_page == 'new_page') & (df2.converted == 1)].shape[0]

# number of individuals who were shown the old_page
n_old = df2[df2.landing_page == 'old_page'].shape[0]

# number of individuals who received new_page
n_new = df2[df2.landing_page == 'new_page'].shape[0]


# **m.** Now use `sm.stats.proportions_ztest()` to compute your test statistic and p-value.  [Here](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportions_ztest.html) is a helpful link on using the built in.
# 
# The syntax is: 
# ```bash
# proportions_ztest(count_array, nobs_array, alternative='larger')
# ```
# where, 
# - `count_array` = represents the number of "converted" for each group
# - `nobs_array` = represents the total number of observations (rows) in each group
# - `alternative` = choose one of the values from `[‘two-sided’, ‘smaller’, ‘larger’]` depending upon two-tailed, left-tailed, or right-tailed respectively. 
# 
# 
# The built-in function above will return the z_score, p_value. 
# 
# ---
# ### About the two-sample z-test
# Recall that you have plotted a distribution `p_diffs` representing the
# difference in the "converted" probability  $(p{'}_{new}-p{'}_{old})$  for your two simulated samples 10,000 times. 
# 
# Another way for comparing the mean of two independent and normal distribution is a **two-sample z-test**. You can perform the Z-test to calculate the Z_score, as shown in the equation below:
# 
# $$
# Z_{score} = \frac{ (p{'}_{new}-p{'}_{old}) - (p_{new}  -  p_{old})}{ \sqrt{ \frac{\sigma^{2}_{new} }{n_{new}} + \frac{\sigma^{2}_{old} }{n_{old}}  } }
# $$
# 
# where
# - $p{'}$ is the "converted" success rate in the sample
# - $p_{new}$ and $p_{old}$ are the "converted" success rate for the two groups in the population. 
# - $\sigma_{new}$ and $\sigma_{new}$ are the standard deviation for the two groups in the population. 
# - $n_{new}$ and $n_{old}$ represent the size of the two groups or samples (it's same in our case)
# 
# 
# >Z-test is performed when the sample size is large, and the population variance is known. The z-score represents the distance between the two "converted" success rates in terms of the standard error. 
# 
# Next step is to make a decision to reject or fail to reject the null hypothesis based on comparing these two values: 
# - $Z_{score}$
# - $Z_{\alpha}$ or $Z_{0.05}$, also known as critical value at 95% confidence interval.  $Z_{0.05}$ is 1.645 for one-tailed tests,  and 1.960 for two-tailed test. You can determine the $Z_{\alpha}$ from the z-table manually. 
# 
# Decide if your hypothesis is either a two-tailed, left-tailed, or right-tailed test. Accordingly, reject OR fail to reject the  null based on the comparison between $Z_{score}$ and $Z_{\alpha}$. 
# 
# 
# In other words, we determine whether or not the $Z_{score}$ lies in the "rejection region" in the distribution. A "rejection region" is an interval where the null hypothesis is rejected iff the $Z_{score}$ lies in that region.
# 
# 
# 
# Reference: 
# - Example 9.1.2 on this [page](https://stats.libretexts.org/Bookshelves/Introductory_Statistics/Book%3A_Introductory_Statistics_(Shafer_and_Zhang)/09%3A_Two-Sample_Problems/9.01%3A_Comparison_of_Two_Population_Means-_Large_Independent_Samples), courtesy www.stats.libretexts.org
# 
# 

# In[31]:


import statsmodels.api as sm
# ToDo: Complete the sm.stats.proportions_ztest() method arguments
z_score, p_value = sm.stats.proportions_ztest([convert_new, convert_old], 
                                              [n_new, n_old], alternative='larger')
print("z = {}\np = {}".format(z_score, p_value))


# **n.** What do the z-score and p-value you computed in the previous question mean for the conversion rates of the old and new pages?  Do they agree with the findings in parts **j.** and **k.**?<br><br>
# 
# 

#  **p-value from the Z-test (p = 0.0.9050583127590245) is nearly equal to the p-value obtained from the central limit theorem method (p = 0.90339999999999998).**  
#  
# **from z-score (z = -1.3109241984234394) is less than z-critical value (z = 1.645) for a one- tailed test and a significance level (α = 0.05) .** 
# 
# **As a consequence, the null hypothesis is not rejected since the results are not statistically significant.**

# <a id='regression'></a>
# ### Part III - A regression approach
# 
# ### ToDo 3.1 
# In this final part, you will see that the result you achieved in the A/B test in Part II above can also be achieved by performing regression.<br><br> 
# 
# **a.** Since each row in the `df2` data is either a conversion or no conversion, what type of regression should you be performing in this case?

# >**Logistic Regression type will be used as it help you predict the likelihood of an event happening or a choice being made (whether an individual convert or not).**

# **b.** The goal is to use **statsmodels** library to fit the regression model you specified in part **a.** above to see if there is a significant difference in conversion based on the page-type a customer receives. However, you first need to create the following two columns in the `df2` dataframe:
#  1. `intercept` - It should be `1` in the entire column. 
#  2. `ab_page` - It's a dummy variable column, having a value `1` when an individual receives the **treatment**, otherwise `0`.  

# In[32]:


# Create the necessary dummy variables
dummies = pd.get_dummies(df2['group'])
df2['ab_page'] = dummies.treatment
df2.head()


# **c.** Use **statsmodels** to instantiate your regression model on the two columns you created in part (b). above, then fit the model to predict whether or not an individual converts. 
# 

# In[33]:


# Fit your model, and summarize the results
df2['intercept'] = 1
mod = sm.Logit(df2['converted'], df2[['intercept', 'ab_page']])
results = mod.fit()
print(results.summary2())


# In[34]:


np.exp(results.params)


# **d.** Provide the summary of your model below, and use it as necessary to answer the following questions.

# In[35]:


results.summary2()


# **e.** What is the p-value associated with **ab_page**? Why does it differ from the value you found in **Part II**?<br><br>  
# 

# **Here is the null and alternative hypotheses associated with our regression model**
# 
# 
# <center>$H_0$ : $p_{new}$ - $p_{old}$ = 0</center>
# <center>$H_1$ : $p_{new}$ - $p_{old}$ ≠ 0</center>
# 
# 
# 
# 1-**The p-value associated with ab_page is (p =0.1899) and it is greater than our Type I error rate; (α = 0.05).**  
# 2- **As a consequence, the null hypothesis is not rejected since the results are not statistically significant.**  
# 3- **Furthermore, because the regression model is evaluating if the difference in conversion rates is equal to zero, the p-value here (p = 0.1899) varies from the p-value obtained in the previous section (p = 0.907).**  
# 

# **f.** Now, you are considering other things that might influence whether or not an individual converts.  Discuss why it is a good idea to consider other factors to add into your regression model.  Are there any disadvantages to adding additional terms into your regression model?

#  **I assume that considering extra factors to include in our regression model is a good option because it will add richness to our analysis and strengthen our regression model abilities, making our model more accurate.**   
#  **because there are some complications that may occur as a result of adding more variables, 
#  there is a problem called multicollinearity, we must ensure that our independent variables have no correlation with one another.**

# **g. Adding countries**<br> 
# Now along with testing if the conversion rate changes for different pages, also add an effect based on which country a user lives in. 
# 
# 1. You will need to read in the **countries.csv** dataset and merge together your `df2` datasets on the appropriate rows. You call the resulting dataframe `df_merged`. [Here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html) are the docs for joining tables. 
# 
# 2. Does it appear that country had an impact on conversion?  To answer this question, consider the three unique values, `['UK', 'US', 'CA']`, in the `country` column. Create dummy variables for these country columns. 
# 
# 
#  Provide the statistical output as well as a written response to answer this question.

# In[36]:


# Read the countries.csv
df_contries = pd.read_csv('countries.csv')
df_contries.head()


# In[37]:


# Join with the df2 dataframe
df_merged = df2.set_index('user_id').join(df_contries.set_index('user_id'), how='inner')
df_merged.reset_index(inplace=True)
df_merged.head()


# In[38]:


# Create the necessary dummy variables
df_merged[['CA', 'UK', 'US']] = pd.get_dummies(df_merged['country'])
df_merged.head()


# In[39]:


# Fit your model, and summarize the results
df_merged['intercept'] =1
model = sm.Logit(df_merged['converted'], df_merged[['intercept', 'CA', 'UK']])
results = model.fit()
print(results.summary2())


# >**From the above results, we can interpret the following:**  
# 1- Conversion rates in CA < US < UK, although the margin is very low that the conversion rate is not significant.  
# 2- This observations is not statistically significant.
# 

# **h. Fit your model and obtain the results**<br> 
# Though you have now looked at the individual factors of country and page on conversion, we would now like to look at an interaction between page and country to see if are there significant effects on conversion.  **Create the necessary additional columns, and fit the new model.** 
# 
# 
# Provide the summary results (statistical output), and your conclusions (written response) based on the results. 
# 

# In[40]:


df_merged['US_ab_page'] = df_merged['US'] * df_merged['ab_page']
df_merged['CA_ab_page'] = df_merged['CA'] * df_merged['ab_page']


# In[41]:


df_merged['intercept']=1 
model2 = sm.Logit(df_merged['converted'],df_merged[['intercept','ab_page','CA','UK','US_ab_page','CA_ab_page']])
result=model2.fit()
result.summary2()


# **We fail to reject the null hypothesis, The new page shouldn't be implemented as there is no evidence that it is better than the old page with respect to country.**

# <a id='finalcheck'></a>
# ## Final Check!
# 
# Congratulations!  You have reached the end of the A/B Test Results project!  You should be very proud of all you have accomplished!
# 
# 
# <a id='submission'></a>
# ## Submission
# You may either submit your notebook through the "SUBMIT PROJECT" button at the bottom of this workspace, or you may work from your local machine and submit on  the last page of this project lesson.  
# 
# 1. Before you submit your project, you need to create a .html or .pdf version of this notebook in the workspace here. To do that, run the code cell below. If it worked correctly, you should get a return code of 0, and you should see the generated .html file in the workspace directory (click on the orange Jupyter icon in the upper left).
# 
# 
# 2. Alternatively, you can download this report as .html via the **File** > **Download as** submenu, and then manually upload it into the workspace directory by clicking on the orange Jupyter icon in the upper left, then using the Upload button.
# 
# 
# 3. Once you've done this, you can submit your project by clicking on the "Submit Project" button in the lower right here. This will create and submit a zip file with this .ipynb doc and the .html or .pdf version you created. Congratulations!

# In[42]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Analyze_ab_test_results_notebook.ipynb'])


# In[ ]:




