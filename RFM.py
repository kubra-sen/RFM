
import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
# TASK 1
# 1. Reading the dataset
df_ = pd.read_excel('RFM/online_retail_II.xlsx', sheet_name='Year 2010-2011')

df = df_.copy()
df.head()

# 2. Descriptive analysis of the data
df.describe().T

# 3. Analzing missing values
df.isnull().sum()

# 4. Handling missing values
df.dropna(inplace=True)

# 5.Unique number of
df["StockCode"].nunique()

# 6.Number of each product
df["Description"].value_counts()

# 7.Top sold products
df["Description"].value_counts().head(5)

# 8. Droping the cancelled transactions
df = df[~df["Invoice"].str.contains("C", na=False)]

# 9.Total Price
df["Total_Price"] = df["Price"] * df["Quantity"]

# TASK2
# Calculating RFM Metrics
df = df[df["Quantity" ] >0]
df = df[df["Price" ] >0]

today_date = dt.datetime(2011, 12, 11)

rfm = df.groupby('Customer ID').agg({"InvoiceDate": lambda date: (today_date - date.max()).days,
                                    "Invoice": lambda num: num.nunique(),
                                     "Total_Price": lambda price: price.sum()})

rfm.columns =  ['recency', 'frequency', 'monetary']

rfm.head()

# TASK 3
# Creating RFM scores and transforming these scores into one variable
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_Score"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)

# TASK 4
# Defining customer segments based on the RFM_scores they get
# Segment names mapping

seg_map = { r'[1-2][1-2]': 'hibernating',
            r'[1-2][3-4]': 'at_Risk',
            r'[1-2]5': 'cant_loose',
            r'3[1-2]': 'about_to_sleep',
            r'33': 'need_attention',
            r'[3-4][4-5]': 'loyal_customers',
            r'41': 'promising',
            r'51': 'new_customers',
            r'[4-5][2-3]': 'potential_loyalists',
            r'5[4-5]': 'champions'

}

rfm['segment'] = rfm['RFM_Score'].replace(seg_map, regex=True)
rfm.head()

# TASK 5

rfm[rfm['segment'] == 'need_attention'].describe().T
rfm[rfm['segment'] == 'cant_loose'].describe().T
rfm[rfm['segment'] == 'at_Risk'].describe().T

Loyals = pd.DataFrame()
Loyals = rfm[rfm['segment']=='loyal_customers']
Loyals.head()

Loyals.to_csv("loyal_customers.csv")