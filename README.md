Getting tired to login to different finaicial institutions to check the stocks, ETFs, or mutual funds everyday? I came up with this tool to solve this issue. It is based on a profile, and the python script will read the profile, and get the data from yahoo finance, write it to mysql DB, and then we query the data from DB and generate the nice report in Grafana like below.

This project will allow users to view all their stocks, ETFs, and mutual funds in a single page. The program runs API calls in fiance.yahoo.com and morningstar.com to grab the data for an inputted profile before sending the data into a mysql database to be queried for a report later.

<img src=https://github.com/Miker48/stock-fund-report/blob/main/financial-report.png>

 Here are the main steps for setting-up MariaDB and Grafana on Centos 8:
<h2>1. Install Python module, and download the python scripts </h2>
   1.1 install python modules: yahoo_fin, pandas, and request_html

      pip3 install yahoo_fin
      pip3 install pandas
      pip3 install requests_html
   
   1.2 Create the profile "my_investments" like the following
        ##########################################################
        # Format
        # symbol # Qty # cost # Asset # Institution # Owner # Type
        #   Asset: [stock|Fund|ETF]
        #   Institution : [ETrade|TDAMeritrade|Fidelity|Vanguard|...]
        #   Type: [Regular|IRA|ROTH|401K]
        ##########################################################
        AAPL 100 10000 stock TDAmeritrade Tom Regular
        TSLA 50  15000 stock Fidelity Tom Roth
        VGHCX 100 20000 Fund Vanguard Tom IRA

      
   
   1.3 download the python script "stock-report.py" and "load-data.sh"
   
   1.4 setup the cronjob like this
      
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
      >create database spending;
      >CREATE USER 'grafanaRO'@'localhost' IDENTIFIED BY 'mypassword';
      >GRANT SELECT ON spending.* TO 'grafanaRO'@'localhost';
     
      
 2.4 download the sample-data

    curl https://raw.githubusercontent.com/Miker48/Expense-project/master/sample-data > sample-data
 
 2.5 create table and load sample data
 
    mysql -uroot -pxxxxx spending <<EOF
    create table if not exists bill ( Year char(4) NOT NULL, Month char(3) NOT NULL, Name varchar(25) NOT NULL, Amount float(10,2) NOT NULL, Paid varchar(3) NOT NULL, PRIMARY KEY (Year, Month, Name));
    load data local infile 'sample-data' into table bill fields terminated by ':';
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
    "Host" "Database" "User" "Password" ---> Click "Save & Test"
    
   <img src=https://github.com/Miker48/Expense-project/blob/master/Setup-Datasource.png>
3.4 Download the grafana dashboard code

    curl https://raw.githubusercontent.com/Miker48/Expense-project/master/Expense.json > Expense.json

3.5 import grafana dashboard 

    click "Grafana" icon on the top left ---> Home ---> Import Dashboard ---> upload .json file ---> and select the file dowbloaded above ---> click "Import"
   
Now you have the nice single pane of glass view of investment report! 
  
