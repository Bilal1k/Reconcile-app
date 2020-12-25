# Reconsile-app
OHIP Billing reconciliation app

This R Shiny application was developed to automate billing reconciliation calculations and generate reports. It takes OHIP "Ontario Health Insurance Plan" Remittance advice files and a private csv report "for private billing and location tags" and generates a report that includes monthly payments per Doctor and some aggregated data for analytical purposes.
Creating those reports was done manually using Excel before this app was developed. It was a time consuming task that was prone to human error.
This app "with some modifications" can be used by most private medical professionals in Ontario, Canada. 

It contains 9 different files. A Windows batch file to run the app from windows desktop, a UI.r file that contains the front-end, a Server.R that directs the data to the appropriet Rmd file for cleaning, calculations and generating a pdf reports. There are 4 Rmd files, 1 for each practitioner. One of the practitioner's bills from 3 different locations, 2 of which are Hopitals, there is a seperate Rmd files that generates a report for hospital billing. In addition to that, there is an Run.r file that locates the app folder and connects the front-end to the back-end. 

This app was created using RStudio 1.2.5033 and R 4.0.
