Getting tired of having to login to multiple financial institutions everyday to check on your stocks, ETFs, or mutual funds? I created this utility to make this process more convenient. In this project, we will make a profile containing the financial assets we want to view, a python script to read the profile and to retrieve data from websites such as fiance.yahoo.com, a MySQL data base to store the data, and a dashboard in Grafana to generate a report of the profile.

<img src=https://github.com/Miker48/stock-fund-report/blob/main/financial-report.png>

 Here are the main steps for setting-up MariaDB and Grafana on Centos 8:
<h2>1. Install Python module, and download the python scripts </h2>
   1.1 install python modules: yahoo_fin, pandas, and request_html

      pip3 install yahoo_fin
      pip3 install pandas
      pip3 install requests_html
      
   1.2 create directory for this tool
   
       mkdir /home/miker/investment
       cd /home/miker/investment
       
   1.3 Create the profile "my_investments" like the following
   
        ##########################################################
        # Format
        #   symbol Qty cost Asset Institution Owner Type
        # 
        #   Use space to seperate the fields
        #   Asset: [stock|Fund|ETF]
        #   Institution : [ETrade|TDAMeritrade|Fidelity|Vanguard|...]
        #   Type: [Regular|IRA|ROTH|401K]
        ##########################################################
        AAPL 100 10000 stock TDAmeritrade Tom Regular
        TSLA 50 15000 stock Fidelity Tom Roth
        VGHCX 100 20000 Fund Vanguard Tom IRA

   
   1.4 download the python script "stock-report.py" and "load-data.sh"
   
      curl https://github.com/Miker48/stock-fund-report/blob/main/stock-report.py > stock-report.py 
      curl https://github.com/Miker48/stock-fund-report/blob/main/load-data.sh > load-data.sh
   
   1.5 setup the cronjob like this so that if will automatically downliad the data, and upload it to the mysql DB every weekday 
      
      05 19 * * 1-5 /home/miker/investment/stock-report.py > /home/miker/investment/daily-reports/$(date +\%F)
      25 19 * * 1-5 /home/miker/investment/load-data.sh /home/miker/investment/daily-reports/$(date +\%F)
   

<h2>2. Install / Config Mariadb</h2>

 
 2.1 install mariadb, for CentOS 8 run

    dnf install -y mariadb
   
   for Mac OS
    
    brew install mariadb

 2.2 setup / config mariadb, for CentOS 8 run

     systemctl enable --now mariadb
     mysql_secure_installation
     
   for macOS run
     
     "mysql.server start"
     
 2.3 create database and read only user for Grafana

     mysql -u root -pxxxxx   # if we run mysql_secure_installation, and set root password
     or
     mysql  # if not run mysql_secure_installation
      >create database investments;
      >CREATE USER 'grafanaRO'@'localhost' IDENTIFIED BY 'mypassword';
      >GRANT SELECT ON investments.* TO 'grafanaRO'@'localhost';

 
 2.4 create table and load sample data
 
    mysql -uroot -pxxxxx investments <<EOF
    create table if not exists stock (Year int(4) NOT NULL, Month int(2) NOT NULL, Day int(2) NOT NULL, Symbol varchar(6) NOT NULL, Qty float(10,2) NOT NULL, Price float(10,2) NOT NULL, Cost float(10,2) NOT NULL, Mkt_Value float(10,2) NOT NULL, Daily_Change float(10,2) NOT NULL, Daily_Change_Ratio float(6,2) NOT NULL, Total_Gain float(10,2) NOT NULL, Total_Gain_Ratio float(6,2) NOT NULL, One_Year_R varchar(20), Asset varchar(25) NOT NULL, Broker varchar(20) NOT NULL, Owner varchar(10) NOT NULL, Category varchar(10) NOT NULL, PRIMARY KEY (Year, Month, Day, Symbol, Broker, Owner, Category));
    load data local infile my_investments into table stock fields terminated by ':';
    EOF


<h2>3. Install / Setup Grafana</h2>

3.1 install grafana server and pie chart plugin, for CentOS8 run the folowing commands as user root

    dnf install grafana
    grafana-cli plugins install grafana-piechart-panel
    
   for macOS run
    
    brew install grafana

3.2 enable / start grafana server, for CentOS 8 run

    systemctl enable --now grafana-server
    
   for macOS run
    
    brew services start grafana

3.3 setup data source

    go to http://localhost:3000

    login as admin/admin

    change password and setup data source
    setting ---> "Data Sources" ---> "Add Data Source" ---> select "MySQL" ---> fill the following fields under "MySQL Connection", 
    "Host" "Database" (should be investments here) "User" "Password" ---> Click "Save & Test"
    
   <img src=https://github.com/Miker48/Expense-project/blob/master/Setup-Datasource.png>
   
3.4 Download the grafana dashboard code

    curl https://github.com/Miker48/stock-fund-report/blob/main/Investment-Report-v1.json> investment-report.json

3.5 import grafana dashboard 

    click "Grafana" icon on the top left ---> Home ---> Import Dashboard ---> upload .json file ---> and select the file dowbloaded above ---> click "Import"
   
Now you have the nice single pane of glass view of your investments report! 
  
