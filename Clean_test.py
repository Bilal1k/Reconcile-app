import numpy as np
import pandas as pd
from csv import reader
from pandas import DataFrame
import io
import datetime as dt



# Read OHIP Remmitance file
path = 'C:\\Users\\Bilal\\Documents\\Projects\\Shiny 3.1\\ZB_Jan.csv'
txt = open(path, 'r')
txtr = txt.read()
txt.close()

# Read the file's header
ind1 = "\"Group Number"
ind2 = "Address"
header = txtr[txtr.index(ind1):txtr.index(ind2)-1]
header = io.StringIO(header)
header = pd.read_csv(header, sep=",", quotechar='"', encoding='iso-8859-1')
header.columns=["Name","Value"]
 
# Get practitioner's name and payment date
RA_Dr = header.loc[header["Name"]=="Payee",["Value"]]
RA_Dr = RA_Dr.iat[0,0]
RA_Date = header.loc[header["Name"]=='Payment Date',["Value"]]
RA_Date = RA_Date.iat[0,0]
RA_Date = dt.datetime.strptime(RA_Date,'%d/%m/%Y')
# Date.strftime('%d/%m/%Y')

# Get payment data
ind1 = '\"Group #'
ind2 = '\n\n'
RAs = txtr[txtr.index(ind1):len(txtr)]
RAs = RAs[0:RAs.index(ind2)]
RAs = io.StringIO(RAs)
RAs = pd.read_csv(RAs, sep=",", quotechar='"', encoding='iso-8859-1')

# Rejections
ind1 = 'Rejected Claims'
ind2 = '\n\n'
Reject = txtr[txtr.index(ind1)+15:len(txtr)]
Reject = Reject[0:Reject.index(ind2)]
Reject = io.StringIO(Reject)
Reject = pd.read_csv(Reject, sep=",", quotechar='"', encoding='iso-8859-1')

# Append Rejections to RAs
RAs = RAs.append(Reject)

# Clean
RAs = RAs[RAs['First Name'].notna()]
RAs['Amt Paid'] = RAs['Amt Paid'].str.replace('$', '', regex=True).astype(float)
RAs['Amt Submitted'] = RAs['Amt Submitted'].str.replace('$', '', regex=True).astype(float)
RAs['Service Date'] = pd.to_datetime(RAs['Service Date'], format='%d/%m/%Y')
RAs['Weekday'] = RAs['Service Date'].dt.day_name()

# Read Hospital Claims

# H1
path_H1 = 'C:\\Users\\Bilal\\Documents\\Projects\\Shiny 3.1\\SJH_Jan.csv'
txt_H1 = open(path_H1, 'r')
txtr_H1 = txt_H1.read()
txt_H1.close()

H1 = io.StringIO(txtr_H1)
H1 = pd.read_csv(H1, sep=",", quotechar='"', encoding='iso-8859-1', header=2)

# Header should be one but for some weird reason is 2 in SJH_Jan.csv
# H1 = pd.read_csv(H1, sep=",", quotechar='"', encoding='iso-8859-1', header=1)

# Clean, pars dates and add weedays
H1['S Date'] = pd.to_datetime(H1['S Date'], format='%d/%m/%Y')
H1['Weekday'] = H1['S Date'].dt.day_name()

H1.columns = H1.columns.str.replace(' ','_', regex=True)
RAs.columns = RAs.columns.str.replace(' ','_', regex=True)

# Take out hospital claims from RAs
ind = (RAs['HCN'].isin(H1['Hcn']) & RAs['Service_Date'].isin(H1['S_Date']) & RAs['Amt_Submitted'].isin(H1['Fee']))
RAs = RAs[ind == False]

# H2
path_H2 = 'C:\\Users\\Bilal\\Documents\\Projects\\Shiny 3.1\\TWH_Jan.csv'
txt_H2 = open(path_H2, 'r')
txtr_H2 = txt_H2.read()
txt_H2.close()

H2 = io.StringIO(txtr_H2)
H2 = pd.read_csv(H2, sep=",", quotechar='"', encoding='iso-8859-1', header=1)

# Clean, pars dates and add weedays
H2['S Date'] = pd.to_datetime(H2['S Date'], format='%d/%m/%Y')
H2['Weekday'] = H2['S Date'].dt.day_name()
H2.columns = H2.columns.str.replace(' ','_', regex=True)

# Take out hospital claims from RAs
ind = (RAs['HCN'].isin(H2['Hcn']) & RAs['Service_Date'].isin(H2['S_Date'])
             & RAs['Amt_Submitted'].isin(H2['Fee']))                          
RAs = RAs[ind == False]

# Add service type and clean RAs
RAs['Type'] = np.where(RAs['Service_Code'].isin(['G432A', 'G858A']), 'OHIP.VF', 'OHIP.Clinic')

RAs = RAs[['First_Name', 'Last_Name', 'Service_Code', 'Service_Date', 'NS',
     'Amt_Submitted', 'Amt_Paid', 'Expl_Code','Weekday','Type']]

# Import Direct
path_Direct = 'C:\\Users\\Bilal\\Documents\\Projects\\Shiny 3.1\\Direct_Jan.csv'
txt_Direct = open(path_Direct, 'r')
txtr_Direct = txt_Direct.read()
txt_Direct.close()

Direct = io.StringIO(txtr_Direct)
Direct = pd.read_csv(Direct, sep=",", quotechar='"', encoding='iso-8859-1', header=1)


# Clean Direct
Direct.columns = Direct.columns.str.replace(' ','_', regex=True)
Direct['S_Date'] = pd.to_datetime(Direct['S_Date'], format='%d/%m/%Y')
Direct = Direct[Direct['S_Date'].dt.month == ((RA_Date - pd.DateOffset(months=1)).month)]
Direct['Weekday'] = Direct['S_Date'].dt.day_name()
Direct.columns = Direct.columns.str.replace(' ','_', regex=True)
Direct = Direct[Direct['Doctor'].str.contains(str(RA_Dr.split()[-1:]).strip('\'[]\''))]
Direct['Paid'] = Direct['Paid'].replace(np.nan, 0)
Direct = Direct[['First', 'Last', 'Serv_Code', 'S_Date', 'NS', 'Fee', 'Paid','Weekday']]
Direct['Type'] = np.where(Direct['Serv_Code'].isin(['G432A', 'G858A','VF']),
        'Direct.VF', np.where(Direct['Serv_Code'].str.contains('TORIC|CHALAZION|MISSED'),
            'Direct.Dr',np.where(Direct['Serv_Code'].str.contains('^MED'), 'Meds', 'Direct.Clinic')))

# Calculate unpaid amounts
RAs['Diff'] = RAs['Amt_Submitted'] - RAs['Amt_Paid']

Unpaid = RAs[RAs['Amt_Paid'] == 0].groupby('Service_Code').agg(
    Count=pd.NamedAgg(column='Amt_Submitted', aggfunc=len),
     Unpaid=pd.NamedAgg(column='Amt_Submitted', aggfunc=sum)).sort_values('Unpaid', ascending=False)

Part_unpaid = RAs[(RAs['Diff'] > 0) & (RAs['Amt_Paid'] != 0)].groupby('Service_Code').agg(
    Count=pd.NamedAgg(column='Amt_Submitted', aggfunc=len),
    Submitted=pd.NamedAgg(column='Amt_Submitted', aggfunc=sum),
    Unpaid=pd.NamedAgg(column='Diff', aggfunc=sum)).sort_values("Unpaid", ascending=False)

sum_unpaid = sum(Unpaid['Unpaid'])
sum_part_unpaid = sum(Part_unpaid['Unpaid'])



OHIP_Clinic = sum(RAs['Amt_Paid'][RAs['Type'] == 'OHIP.Clinic'])
OHIP_VF = sum(RAs['Amt_Paid'][RAs['Type'] == 'OHIP.VF'])
Direct_Clinic = sum(Direct['Paid'][Direct['Type'] == 'Direct.Clinic'])
Direct_VF = sum(Direct['Paid'][Direct['Type'] == 'Direct.VF'])
Direct_Dr = sum(Direct['Paid'][Direct['Type'] == 'Direct.Dr'])

print(OHIP_Clinic,OHIP_VF,Direct_Clinic,Direct_VF,Direct_Dr)

Payable = (0.35 * OHIP_Clinic) + (0.5 * OHIP_VF) - (0.65 * Direct_Clinic) - (0.5 * Direct_VF) - (Direct_Dr)
Payable


