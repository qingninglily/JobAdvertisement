import pandas as pd
import numpy as np
from datetime import datetime
import sys
import csv



def processData(directory):
    #Load the dataset
    data=pd.read_csv(directory)

    ##############################################################################################
    #Return rows with missing values
    missingvalueindex=[]
    for i in list(data.index):
        if data.iloc[i].isnull().any()==True:
            missingvalueindex.append(i)
    
    if len(missingvalueindex)>0:
        print('Rows with Missing Values:')
        for i in missingvalueindex:
            print('Row#',str(i+1),data.iloc[i])
    else:
        print('No missing values')

    ################################################################################################################
    #Create new features, such as Month and Weekday
    data['Conversion Rate']=data['Conversions']/data['Clicks']
    Month=[datetime.strptime(i,'%Y-%m-%d').month for i in data['Date']]
    Weekday=[datetime.strptime(i,'%Y-%m-%d').strftime('%A') for i in data['Date']]
    data['Month']=Month
    data['Weekday']=Weekday
    data.to_csv('C:/Users/Ruixin Zheng/Downloads/JobTarget/rawdata.csv',index=False)

    ################################################################################################################
    #Get large data
    dataReqID=data.drop(columns=['Date','Month','Weekday'])
    nunique=dataReqID.groupby(['Requisition ID','Requisition Title'])['Advertiser ID'].agg([('Number of Ad_ID/Req_ID','nunique')])

    groupbyReqID=dataReqID.groupby(['Requisition ID','Requisition Title','Advertiser ID']).agg('mean')
    groupbyReqID.rename(columns={'Clicks':'Clicks/day','Conversions':'Conversions/day','Cost':'Cost/day','Conversion Rate':'Conversion Rate/day'},inplace=True)
    groupbyReqID=groupbyReqID.reset_index(level=['Advertiser ID'])

    groupbyReqID=pd.merge(groupbyReqID,nunique,left_index=True,right_index=True,how='left')
    groupbyReqID=groupbyReqID.reset_index()
    groupbyReqID.to_csv('C:/Users/Ruixin Zheng/Downloads/JobTarget/groupbyReqID.csv',index=False)

    ###############################################################################################################
    #Get the Advertisers' Performance
    dataAd=data.drop(columns=['Date','Month','Weekday'])
    groupbyAd=dataAd.groupby(['Advertiser ID'])[['Clicks','Conversions','Cost','Conversion Rate']].mean()
    groupbyAd.rename(columns={'Clicks':'Avg Clicks','Conversions':'Avg Conversions','Cost':'Avg Cost','Conversion Rate':'Avg Conversion Rate'},inplace=True)
    groupbyAd.sort_values(by=['Avg Conversions','Avg Clicks'],ascending=False)
    
    avggroupbyAd=groupbyAd.mean(axis=0)
    
    groupbyAd.to_csv('C:/Users/Ruixin Zheng/Downloads/JobTarget/AdvertiserPerformance.csv')
    
    ################################################################################################################
    #Get Requisition Title's Performance 
    dataTitle=data.drop(columns=['Requisition ID','Date','Month','Weekday'])
    number_AdID=dataTitle.groupby('Requisition Title')['Advertiser ID'].agg([('Number of Ad_ID/Req_Title','nunique')])

    groupbyTitle=dataTitle.groupby(['Requisition Title','Advertiser ID']).agg('mean')
    groupbyTitle.rename(columns={'Clicks':'Avg Clicks','Conversions':'Avg Conversions','Cost':'Avg Cost','Conversion Rate':'Avg Conversion Rate'},inplace=True)
    groupbyTitle=groupbyTitle.reset_index(level=['Advertiser ID'])
    groupbyTitle=pd.merge(groupbyTitle,number_AdID,left_index=True,right_index=True,how='left')
    groupbyTitle.to_csv('C:/Users/Ruixin Zheng/Downloads/JobTarget/ReqTitlePerformance.csv')
    #################################################################################################################
    return({'data':data,'groupbyReqID':groupbyReqID,'groupbyAd':groupbyAd,'groupbyTitle':groupbyTitle})



def ReqID_chooseTopAd(Requisition_ID):
    processdata=processData(directory)
    groupbyReqID=processdata['groupbyReqID']
    

    data_req=groupbyReqID[groupbyReqID['Requisition ID']==ReqID]
    ###############################################################################################
    #check if a Requisition ID is posted in multiple Advertisers
    Number_AdID=data_req['Number of Ad_ID/Req_ID']
    #################################################################################################
    #Compare the Advertisers based on four cretiria
    if Number_AdID.values[0]>1:
        groupedReqID=data_req.set_index(['Requisition ID','Requisition Title'])
        groupedReqID=groupedReqID.drop(columns='Number of Ad_ID/Req_ID')

        avggroupedReqID=groupedReqID.drop(columns='Advertiser ID')
        avggroupedReqID=avggroupedReqID.mean(axis=0)
        avggroupedReqID.rename({'Clicks/day':'Avg Clicks/day','Conversions/day':'Avg Conversions/day','Cost/day':'Avg Cost/day','Conversion Rate/day':'Avg Conversion Rate/day'},inplace=True)


        topAd_clicks=groupedReqID[groupedReqID['Clicks/day']>avggroupedReqID['Avg Clicks/day']].sort_values(by='Clicks/day',ascending=False)
        topAd_conversions=groupedReqID[groupedReqID['Conversions/day']>avggroupedReqID['Avg Conversions/day']].sort_values(by='Conversions/day',ascending=False)
        topAd_cost=groupedReqID[groupedReqID['Cost/day']<avggroupedReqID['Avg Cost/day']].sort_values(by='Cost/day')
        topAd_conversionrate=groupedReqID[groupedReqID['Conversion Rate/day']>avggroupedReqID['Avg Conversion Rate/day']].sort_values(by='Conversion Rate/day',ascending=False)
        try:
            commonTopAd=pd.merge(topAd_clicks,topAd_conversions,topAd_cost,topAd_conversionrate,on='Advertiser ID',how='inner')
        except TypeError:
            commonTopAd='No Advetiser fitting all criteria'  



        with open('C:/Users/Ruixin Zheng/Downloads/JobTarget/chooseTopAd_'+str(ReqID)+'.csv','w') as writefile:
            writer=csv.writer(writefile,lineterminator='\n')
            writer.writerow(['Top Ad above Avg Clicks','Advertiser ID','Clicks/day','Conversions/day','Cost/day','Conversion Rate/day'])
            for n in range(len(topAd_clicks.values)):
                writer.writerow([n+1]+list(topAd_clicks.values[n]))

            writer.writerow(['Top Ad above Avg Conversions','Advertiser ID','Clicks/day','Conversions/day','Cost/day','Conversion Rate/day'])
            for n in range(len(topAd_conversions.values)):
                writer.writerow([n+1]+list(topAd_conversions.values[n]))

            writer.writerow(['Top Ad above Avg Costs','Advertiser ID','Clicks/day','Conversions/day','Cost/day','Conversion Rate/day'])
            for n in range(len(topAd_cost.values)):
                writer.writerow([n+1]+list(topAd_cost.values[n]))

            writer.writerow(['Top Ad above Avg Conversion Rate','Advertiser ID','Clicks/day','Conversions/day','Cost/day','Conversion Rate/day'])
            for n in range(len(topAd_conversionrate.values)):
                writer.writerow([n+1]+list(topAd_conversionrate.values[n]))
        print('Requisition ID:',ReqID)
        print('Results:#############################################################################################################')
        return({'groupedReqID':groupedReqID,'topAd_clicks':topAd_clicks,'topAd_conversions':topAd_conversions,'topAd_cost':topAd_cost,'topAd_conversionrate':topAd_conversionrate,'commonTopAd':commonTopAd})   
    else:
        #Find advertisers which perform better than current advertiser
        AdvertiserID=data_req['Advertiser ID'].values[0]

        #Find the Requisition IDs with the same title
        RequisitionTitle=data_req['Requisition Title'].values[0]

        groupbyTitle=processdata['groupbyTitle'].reset_index()
        TitlePerformance=groupbyTitle[groupbyTitle['Requisition Title']==RequisitionTitle]
        print('Requisition ID:',ReqID)
        print('Results###############################################################################################################')
        print('This job is only posted in one Advertiser (Advertiser ID:'+str(AdvertiserID)+')')
        return({'AdvertiserID':AdvertiserID,'Requisition Title':RequisitionTitle,'TitlePerformance':TitlePerformance})



if __name__=="__main__":
    directory=sys.argv[1]
    Requisition_IDs=sys.argv[2]
    Requisition_ID=[i.strip() for i in Requisition_IDs.split(',')]
    for i in range(len(Requisition_ID)):
        ReqID=int(Requisition_ID[i])
        #print(processData(directory))
        print(ReqID_chooseTopAd(ReqID))
        print('\n')
        print('\n')
        print('\n')
