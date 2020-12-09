Getting tired to login to different finaicial institutions to check the stocks, ETFs, or mutual funds evreyday? I came up with this tool to solve this issue. It' is based on a profile, and the python script will read the profile, and get the data from yahoo finance, write it to mysql DB, and then we query the data from DB and generate the nice report in Grafana like below.

<img src=https://github.com/Miker48/stock-fund-report/blob/main/financial-report.png>

How to set it up:

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

   
   
   
  
