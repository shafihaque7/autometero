#!/usr/bin/expect

spawn ssh azureuser@104.42.212.81
expect "password:"
send "Santunu12345\r"
expect "armvmhingeserver"
send "cd hingeautomation/\r"
expect "~/hingeautomation"
send "git pull\r"
interact
