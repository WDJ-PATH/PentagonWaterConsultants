# Pentagon Water Consultants - Website
A webpage for PENTAGON WATER CONSULTANTS - a Service Provider of Waste water &amp; Water Supply Consultancy Services

**Want to report a bug? Raise an issue on this repo.**

## :star2: &nbsp;&nbsp;Tools & Packages Used

![](https://img.shields.io/badge/1.-python--v3.6-blue)
![](https://img.shields.io/badge/2.-django--v3.0.3-yellow)
![](https://img.shields.io/badge/3.-PostgreSQL-success)
![](https://img.shields.io/badge/4.-whitenoise--v5.1.0-9cf)
![](https://img.shields.io/badge/5.-gunicorn--v20.0.4-orange)
![](https://img.shields.io/badge/6.-reportlab--v3.5.42-blueviolet)
![](https://img.shields.io/badge/7.-fuzzywuzzy--v0.17.0-ff69b4)
![](https://img.shields.io/badge/8.-xlwt--v1.3.0-yellowgreen)

**Others**

![](https://img.shields.io/badge/1.-HTML-critical)
![](https://img.shields.io/badge/2.-CSS-blue)
![](https://img.shields.io/badge/3.-Bootstrap--v4.5.0-success)
![](https://img.shields.io/badge/4.-pyCharmIDE-inactive)


## :star2: &nbsp;&nbsp;Features

Responsive UI optimised for mobile & desktop users.

### Manager Side

1. Register account
2. Search users and their tests
    1. Fuzzy Search - (User doesn't need to know the exact spelling of the customer name. This search produces result by checking similarity between words.) | New Feature :gift_heart: 
3. Add new tests
4. Update test details
5. Export Completed Tests 100 at a time to an excel sheet(.xls file), and delete those tests from the DB. | New Feature :gift_heart:  
6. Ban a user
7. Download test details as PDF

### Customer Side

1. Register account
2. Reset Password
3. View all their tests
4. View specific test details
5. Download unofficial PDF of test details
6. View enquiry information


### Security 
* Highly Secure DB storage : All passwords & sensitive information of users & managers are hashed with md5 hashing using the highly efficient hashlib library of python.
    * _Not even the DB admin can view it._ :sparkles:
* User passwords can only be changed using a security code provided at the time of account creation.


## :star2: &nbsp;&nbsp;User Interface

* **_Manager :_**

![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/m_login.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/m_register.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/m_dash.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/m_addtest.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/m_search.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/m_test_update_print.gif)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/m_export_delete.gif)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/m_ban.gif)

***

* **_Customer :_**

![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/Home.gif)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/u_login.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/u_register.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/u_passreset.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/u_dash.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/u_tests.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/u_testdetails.png)
![](https://github.com/WDJ-PATH/PentagonWaterConsultants/blob/master/PWC_UserScreensV2/u_pdf_download.gif)



***
<p align="center">
    Made with :heart: &nbsp;&nbsp;|&nbsp; All rights reserved.
</p>