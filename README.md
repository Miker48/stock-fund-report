Getting tired to login to different finaicial institutions to check the stocks, ETFs, or mutual funds evreyday? I came up with this tool to solve this issue. It' is based on a profile, and the python script will read the profile, and get the data from yahoo finance, write it to mysql DB, and then we query the data from DB and generate the nice report in Grafana like below.

<img src=https://github.com/Miker48/stock-fund-report/blob/main/financial-report.png>

 Here are the main steps for setting-up MariaDB and Grafana on Centos 8:

   1. install python modules: yahoo_fin, pandas, and request_html

   pip3 install yahoo_fin
   pip3 install pandas
   pip3 install requests_html
   
   2. downloadd the profile "my_investments" 
   
   3. download the python script "stock-report.py" and "load-data.sh"
   
   4. setup the cronjob like this
      
   05 19 * * * /home/miker/investment/stock-report.py > /home/miker/investment/daily-reports/$(date +\%F)
   25 19 * * * /home/miker/investment/load-data.sh /home/miker/investment/daily-reports/$(date +\%F)
   
   4. setup grafana data source, and import the dashboard
   
   5. enjoy the new convinient tool

   
   
  

<h2>1. Install / Config Mariadb</h2>

 
 1.1 install mariadb, for CentOS 8 run

    dnf install -y mariadb
   
   for Mac OS
    
    brew install mariadb

 1.2 setup / config mariadb, for CentOS 8 run

     systemctl enable --now mariadb
     mysql_secure_installation
     
   for macOS run
     
     "mysql.server start"
     
 1.3 create database and read only user for Grafana

     mysql -u root -pxxxxx   # if we run mysql_secure_installation, and set root password
     or
     mysql  # if not run mysql_secure_installation
      >create database spending;
      >CREATE USER 'grafanaRO'@'localhost' IDENTIFIED BY 'mypassword';
      >GRANT SELECT ON spending.* TO 'grafanaRO'@'localhost';
     
      
 1.4 download the sample-data

    curl https://raw.githubusercontent.com/Miker48/Expense-project/master/sample-data > sample-data
 
 1.5 create table and load sample data
 
    mysql -uroot -pxxxxx spending <<EOF
    create table if not exists bill ( Year char(4) NOT NULL, Month char(3) NOT NULL, Name varchar(25) NOT NULL, Amount float(10,2) NOT NULL, Paid varchar(3) NOT NULL, PRIMARY KEY (Year, Month, Name));
    load data local infile 'sample-data' into table bill fields terminated by ':';
    EOF


<h2>2. Install / Setup Grafana</h2>

2.1 install grafana server and pie chart plugin, for CentOS8 run the folowing commands as user root

    dnf install grafana
    grafana-cli plugins install grafana-piechart-panel
    
   for macOS run
    
    brew install grafana

2.2 enable / start grafana server, for CentOS 8 run

    systemctl enable --now grafana-server
    
   for macOS run
    
    brew services start grafana

2.3 setup data source

    go to http://localhost:3000

    login as admin/admin

    change password and setup data source
    setting ---> "Data Sources" ---> "Add Data Source" ---> select "MySQL" ---> fill the following fields under "MySQL Connection", 
    "Host" "Database" "User" "Password" ---> Click "Save & Test"
    
   <img src=https://github.com/Miker48/Expense-project/blob/master/Setup-Datasource.png>
2.4 Download the grafana dashboard code

    curl https://raw.githubusercontent.com/Miker48/Expense-project/master/Expense.json > Expense.json

2.5 import grafana dashboard 

    click "Grafana" icon on the top left ---> Home ---> Import Dashboard ---> upload .json file ---> and select the file dowbloaded above ---> click "Import"
   
Now you have the nice single pane of glass view of monthly expense dashboard! 
  
