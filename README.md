# JobAdvertisement

# Project

This provides the python script for processing the rawdata and returning the new structured dataset and analytical result.

## Contents
---
- **General**
    - Folder setup
- **Data Processing Scripts**
    - `processData.py`
 
## General
### Folder setup
This script uses the command line. To run this script, open the command line and navigate to the folder containing them by entering

```
cd C:\Users\Ruixin Zheng\Downloads\JobTarget
```

and then entering

```
python <name_of_script> <parameter_1> <parameter_2> ...
```

Before you can run any scripts, make sure you have installed [Python](https://www.python.org/) and have also installed the following libraries using these commands:

```
pip install pandas
pip install numpy
pip install datetime
pip install csv
```

---


## `processdData.py`

This script handles grouping rawdata, creating new useful dataset and exporting the top advertiser IDs for the given requisition IDs. 

### Usage

```
python processData.py <directory> <RequisitionID_1>,<Requisition ID_2>,<Requisition_ID3>...
```

*Example:*
```
python processData.py dataset.csv 25574815,25810861
```
This script can accept multiple Requisition IDs and results will be shown separately in the ID order you put in the command line. Running the script allows you to get top advertisers that perform better than average advertisers performance in four different aspects (clicks, converions, cost and conversion rate). If the script is run normally, the console will print the rows with top Advertiser IDs. When Requisition ID only has one Advertiser ID, the console will instead return the correspongding **Advertiser ID** and **Requisition Title** that could be used as input in `Tabeau` to check job site's and title's performance.


### `processData(directory)`

This function will first print the rows with any missing values or it will return **No missing values** in the console if there is no missing values. This function also adds three useful new features--`Conversion Rate`,`Month` and `Weekday` into original dataset. Based on the dataset from directory address, it automatically produce four csv files in `JobTarget` folder:

- `rawdata.csv`--Concatenating new features with original columns
- `roupbyReqID.csv`--Grouped by **Requisition ID**
- `AdvertiserPerformance.csv`--Grouped by **Advertiser ID**
- `ReqTitlePerformance.csv`--Grouped by **Requisition Title**

### `ReqID_chooseTopAd(Requisition_ID)`

This function will first run `processData(directory)` automatically to get the main data table. If the given `Reuiqsition ID` has multiple correspinding advertiser IDs, this function will return four tables listing all advertisers that perform above the average level in four aspects--average clicks, average conversions, average cost and average conversion rate. The result will be saved in JobTarget folder as `chooseTopAd_<Requisition ID>.csv`.If the given `Reuiqsition ID` has only one advertiser ID, this function will return the corresponding `Advertiser ID`, `Requisition Title` and the data table grouped by this Requisition Title.

