shinyUI(
    fluidPage(
        selectInput("doctor", "Report Type:",
                    choices = c("Dr.1",
                                "Dr.2",
                                "Dr.3",
                                "Hospitals")),
        
        conditionalPanel(
            condition = "input.doctor == 'Dr.1'",
            fileInput("RA1", "Remittance Advice File", multiple = FALSE, accept = ".csv"),
            fileInput("direct1", "Direct Claims", multiple = FALSE, accept = ".csv")),
        
        conditionalPanel(
            condition = "input.doctor == 'Dr.2'",
            fileInput("RA2", "Remittance Advice File", multiple = FALSE, accept = ".csv"), 
            fileInput("direct2", "Direct Claims", multiple = FALSE, accept = ".csv")),
        
        
        # Dr.3 is using the office's billing software to bill hospital Pt. This need to be calculated separately.
        
        conditionalPanel(
            condition = "input.doctor == 'Dr.3'",
            fileInput("RA3", "Remittance Advice File", multiple = FALSE, accept = ".csv"),
            fileInput("direct3", "Direct Claims", multiple = FALSE, accept = ".csv"),
            fileInput("Hospital_1", "Hospital 1 Claims", multiple = FALSE, accept = ".csv"),
            fileInput("Hospital_2", "Hospital 2 Claims", multiple = FALSE, accept = ".csv")),
        
        conditionalPanel(
            condition = "input.doctor == 'Hospitals'",
            fileInput("RA3H", "Remittance Advice File", multiple = FALSE, accept = ".csv"),
            fileInput("Hospital_1H", "Hospital 1 Claims", multiple = FALSE, accept = ".csv"),
            fileInput("Hospital_2H", "Hospital 2 Claims", multiple = FALSE, accept = ".csv")),
            
        
        downloadButton("report", "Generate report")
    ))