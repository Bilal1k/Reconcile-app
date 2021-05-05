shinyUI(
    fluidPage(
        selectInput("doctor", "Report Type:",
                    choices = c("Dr.1",
                                "Dr.2",
                                "Dr.3",
                                "Hospitals"),
                    selected = "Dr.1"),
        
        conditionalPanel(
            condition = "input.doctor == 'Dr.1'",
            fileInput("RA", "Remittance Advice File", multiple = FALSE, accept = ".csv"),
            fileInput("direct", "Direct Claims", multiple = FALSE, accept = ".csv")),
        
        conditionalPanel(
            condition = "input.doctor == 'Dr.2'",
            fileInput("RA", "Remittance Advice File", multiple = FALSE, accept = ".csv"), 
            fileInput("direct", "Direct Claims", multiple = FALSE, accept = ".csv")),
        
        
        # Dr.3 is using the office's billing software to bill hospital Pt. This need to be calculated separately.
        
        conditionalPanel(
            condition = "input.doctor == 'Dr.3'",
            fileInput("RA", "Remittance Advice File", multiple = FALSE, accept = ".csv"),
            fileInput("direct", "Direct Claims", multiple = FALSE, accept = ".csv"),
            fileInput("Hospital_1", "Hospital 1 Claims", multiple = FALSE, accept = ".csv"),
            fileInput("Hospital_2", "Hospital 2 Claims", multiple = FALSE, accept = ".csv")),
        
        conditionalPanel(
            condition = "input.doctor == 'Hospitals'",
            fileInput("RA", "Remittance Advice File", multiple = FALSE, accept = ".csv"),
            fileInput("Hospital_1", "Hospital 1 Claims", multiple = FALSE, accept = ".csv"),
            fileInput("Hospital_2", "Hospital 2 Claims", multiple = FALSE, accept = ".csv")),
            
        
        downloadButton("report", "Generate report")
    ))