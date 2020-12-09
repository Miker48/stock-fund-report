Getting tired to login to different finaicial institutions to check the stocks, ETFs, or mutual funds evryday? I came up with this tool to solve this issue. It' is based on a profile, and the python script will read the profile, and get the data from finance.yahoo.com, write it to mysql DB, and then from grafana we query the data from DB and generate the nice report like below.

<img src=https://github.com/Miker48/stock-fund-report/blob/main/financial-report.png>

How to set it up:

1. install yahoo_fin

   pip3 install yahoo_fin

2. install pandas

   pip3 install pandas

3. install request_html

   pip3 install requests_html
