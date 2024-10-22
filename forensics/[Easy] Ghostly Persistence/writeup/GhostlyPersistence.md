![img](assets/banner.png)

<img src='assets/htb.png' style='zoom: 80%;' align=left /> <font size='10'>Ghostly Persistence</font>

30<sup>th</sup> August 2024

Prepared By: Nauten

Challenge Author(s): Nauten

Difficulty: <font color='green'>Easy</font>

<br><br>

# Synopsis

- Ghostly Persistence is an easy forensics challenge involving analyzing multiple evtx files searching for powershell executed code in order to obtain the flag.

## Description

- On a quiet Halloween night, when the world outside was wrapped in shadows, an intrusion alert pierced through the calm. The alert, triggered by an internal monitoring system, pinpointed unusual activity on a specific workstation.

  Can you illuminate the darkness and uncover what happened during this intrusion? 
  
  Note: flag is split into two parts

## Skills Required

- Familiarity with evtx file structure
- Familiarity with Powershell

## Skills Learned

- Analyzing evtx files
- Analyzing basic Powershell code

# Enumeration

We are given the following file:

- `Logs.zip`: containing a set of Windows event logs

![](assets/8579e260-138c-4304-973f-783efdaefb8e.png)

There are a lot of files but only one seems to have a different size.

To parse this type of file `python-evtx` can be used. It's also possible to convert all files in the XML counterpart using a single command:

![](assets/e3dbc8fc-6f5e-4c24-89c8-f07ce25beb0d.png)

Analyzing the file **Microsoft-Windows-PowerShell_Operational.xml** it's possible to find multiple commands with identifier "4104" that corresponds to "Execute a Remote Command".

Looking at it in sequential order we find multiple executions.

First part:

![](assets/bb18b989-f630-4a25-9331-50a50e2d9eb0.png)

![](assets/b2cd3166-45f1-4cc1-90a0-813c89f414d8.png)

A file named **wLDwomPJLN.ps1** is downloaded from a remote domain and gets executed. 
In the second event block it's possible to see the content of it. 

It executes some enumeration on the system and setup a persistence mechanism creating a new task that runs on startup with a custom powershell payload (base64 encoded).

Second part:

![](assets/6a4877cb-bfea-434b-9c46-80f3d22a148e.png)

![](assets/6ddcf384-8eb1-4246-ba81-d1213f560504.png)

A file named **3MZvgfcEiT.ps1** is downloaded from a remote domain and gets executed. 
In the second event block it's possible to see the content of it. It executes some enumeration on the system and set a new entry on the registry path `HKCU:\Software\cPdQnixceg` 

# Solution

Analyzing closer the code of the first part:

![](assets/8a8458f9-9413-44c1-95b8-f779ed0a3834.png)

It's possible to notice a base64 string:

![](assets/370adade-3968-49b1-bf60-b2e8ba496e87.png)

And the second part:

![](assets/1dbbc924-a10c-48e0-9dc7-81caabab0cfc.png)

![](assets/bf129833-bb6b-4ee9-abe4-7655d769fa70.png)

**Combine the two parts and get the full flag:** `HTB{Gh0st_L0c4t10n_W4s_R3v34l3d}`