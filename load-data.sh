#!/bin/sh

#sed -i 's/ \+/:/g' $1
sed -i 's/ //g' $1

mysql -u root -ptest1234 <<EOF
#create database if not exists investments;
#CREATE USER 'grafanaRO'@'192.168.1.238' IDENTIFIED BY 'T0p$3CRT!';
#GRANT SELECT ON investments.* TO 'grafanaRO'@'192.168.1.238';
use investments;
#create table if not exists stock (Year int(4) NOT NULL, Month int(2) NOT NULL, Day int(2) NOT NULL, Symbol varchar(6) NOT NULL, Qty float(10,2) NOT NULL, Price float(10,2) NOT NULL, Cost float(10,2) NOT NULL, Mkt_Value float(10,2) NOT NULL, Daily_Change float(10,2) NOT NULL, Daily_Change_Ratio float(6,2) NOT NULL, Total_Gain float(10,2) NOT NULL, Total_Gain_Ratio float(6,2) NOT NULL, One_Year_R varchar(20), Asset varchar(25) NOT NULL, Broker varchar(20) NOT NULL, Owner varchar(10) NOT NULL, Category varchar(10) NOT NULL, PRIMARY KEY (Year, Month, Day, Symbol, Broker, Owner, Category));
load data local infile '$1' into table stock fields terminated by ':';
EOF
