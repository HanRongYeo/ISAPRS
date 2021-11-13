# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:27:31 2020

@author: SheepCurry
"""

import subprocess

def run(data, score):
    p = subprocess.Popen(["powershell.exe", """function Get-AntiVirusProduct {
        [CmdletBinding()]
        param (
        [parameter(ValueFromPipeline=$true, ValueFromPipelineByPropertyName=$true)]
        [Alias('name')]
        $computername=$env:computername
    
    
        )
    
        #$AntivirusProducts = Get-WmiObject -Namespace "root\SecurityCenter2" -Query $wmiQuery  @psboundparameters # -ErrorVariable myError -ErrorAction 'SilentlyContinue' # did not work            
         $AntiVirusProducts = Get-WmiObject -Namespace "root\SecurityCenter2" -Class AntiVirusProduct  -ComputerName $computername
    
        $ret = @()
        foreach($AntiVirusProduct in $AntiVirusProducts){
            #Switch to determine the status of antivirus definitions and real-time protection.
            #The values in this switch-statement are retrieved from the following website: http://community.kaseya.com/resources/m/knowexch/1020.aspx
            switch ($AntiVirusProduct.productState) {
            "262144" {$defstatus = "Up to date" ;$rtstatus = "Disabled"}
                "262160" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}
                "266240" {$defstatus = "Up to date" ;$rtstatus = "Enabled"}
                "266256" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}
                "393216" {$defstatus = "Up to date" ;$rtstatus = "Disabled"}
                "393232" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}
                "393488" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}
                "397312" {$defstatus = "Up to date" ;$rtstatus = "Enabled"}
                "397328" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}
                "397584" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}
            default {$defstatus = "Unknown" ;$rtstatus = "Unknown"}
                }
    
            #Create hash-table for each computer
            $ht = @{}
            $ht.Computername = $computername
            $ht.Name = $AntiVirusProduct.displayName
            $ht.'Product GUID' = $AntiVirusProduct.instanceGuid
            $ht.'Product Executable' = $AntiVirusProduct.pathToSignedProductExe
            $ht.'Reporting Exe' = $AntiVirusProduct.pathToSignedReportingExe
            $ht.'Definition Status' = $defstatus
            $ht.'Real-time Protection Status' = $rtstatus
    
    
            #Create a new object for each computer
            $ret += New-Object -TypeName PSObject -Property $ht 
        }
        Return $ret
    } 
    $result = Get-AntiVirusProduct
    Write-Output $result"""],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    
    out,err = p.communicate()
    out_str = out.decode("utf-8")
    outList = out_str.split("\n")
    flag_enable = False
    flag_new = False
    flag_up = False
    
    print(out_str)
    
    for line in outList:
        if "Product GUID" in line:
            flag_enable = False
            flag_new = False
            flag_up = False
            
        elif "Name" in line:
            flag_new = True
            data["anti_name"] = line.split(" : ")[1].rstrip()
                    
        elif "Real-time" in line:
            if "Enabled" in line:
                data["enable"] = 1
                flag_enable = True
            else:
                data["enable"] = 0
                
        elif "Definition" in line:
            if "Up to date" in line:
                flag_up = True
                data["uptodate"] = 1
            else:
                data["uptodate"] = 0
            
        if flag_enable and flag_new and flag_up:
            break
    
    if flag_enable:
        score += 0.0555
        return (score)
    else:
        return (score)
    
def run_exist(data):
    p = subprocess.Popen(["powershell.exe", """function Get-AntiVirusProduct {
        [CmdletBinding()]
        param (
        [parameter(ValueFromPipeline=$true, ValueFromPipelineByPropertyName=$true)]
        [Alias('name')]
        $computername=$env:computername
    
    
        )
    
        #$AntivirusProducts = Get-WmiObject -Namespace "root\SecurityCenter2" -Query $wmiQuery  @psboundparameters # -ErrorVariable myError -ErrorAction 'SilentlyContinue' # did not work            
         $AntiVirusProducts = Get-WmiObject -Namespace "root\SecurityCenter2" -Class AntiVirusProduct  -ComputerName $computername
    
        $ret = @()
        foreach($AntiVirusProduct in $AntiVirusProducts){
            #Switch to determine the status of antivirus definitions and real-time protection.
            #The values in this switch-statement are retrieved from the following website: http://community.kaseya.com/resources/m/knowexch/1020.aspx
            switch ($AntiVirusProduct.productState) {
            "262144" {$defstatus = "Up to date" ;$rtstatus = "Disabled"}
                "262160" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}
                "266240" {$defstatus = "Up to date" ;$rtstatus = "Enabled"}
                "266256" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}
                "393216" {$defstatus = "Up to date" ;$rtstatus = "Disabled"}
                "393232" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}
                "393488" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}
                "397312" {$defstatus = "Up to date" ;$rtstatus = "Enabled"}
                "397328" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}
                "397584" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}
            default {$defstatus = "Unknown" ;$rtstatus = "Unknown"}
                }
    
            #Create hash-table for each computer
            $ht = @{}
            $ht.Computername = $computername
            $ht.Name = $AntiVirusProduct.displayName
            $ht.'Product GUID' = $AntiVirusProduct.instanceGuid
            $ht.'Product Executable' = $AntiVirusProduct.pathToSignedProductExe
            $ht.'Reporting Exe' = $AntiVirusProduct.pathToSignedReportingExe
            $ht.'Definition Status' = $defstatus
            $ht.'Real-time Protection Status' = $rtstatus
    
    
            #Create a new object for each computer
            $ret += New-Object -TypeName PSObject -Property $ht 
        }
        Return $ret
    } 
    $result = Get-AntiVirusProduct
    Write-Output $result"""],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    
    out,err = p.communicate()
    out_str = out.decode("utf-8")
    outList = out_str.split("\n")
    flag_enable = False
    flag_new = False
    flag_up = False
    
    print(out_str)
    
    for line in outList:
        if "Product GUID" in line:
            flag_enable = False
            flag_new = False
            flag_up = False
            
        elif "Name" in line:
            flag_new = True
            data["anti_name"] = line.split(" : ")[1].rstrip()
                    
        elif "Real-time" in line:
            if "Enabled" in line:
                if data["enable"] == 0:
                    data["enable"] = 1
                    data["score"] += 0.111
                    flag_enable = True
                else:
                    flag_enable = True
            else:
                if data["enable"] == 1:
                    data["enable"] = 0
                    data["score"] -= 0.111
                
        elif "Definition" in line:
            if "Up to date" in line:
                flag_up = True
                data["uptodate"] = 1
            else:
                flag_up = True
                data["uptodate"] = 0
            
        if flag_enable and flag_new and flag_up:
            break
    
# data={'anti_name': 'Bitdefender Antivirus Free Antimalware', 'enable': 1, 'uptodate': 1,'score':0.8}
# score=0
# # run(data,score)
# run_exist(data)
# print(data)
# print(score)