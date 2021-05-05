shinyServer(function(input, output) {
  
  # make rmd and file choice reactive
  # choose Rmd file based on chosen practitioner
  Dr <- eventReactive(input$update, {
    switch(input$doctor,
           "Dr.1" = "Dr1.Rmd",
           "Dr.2" = "Dr2.Rmd",
           "Dr.3" = "Dr3.Rmd",
           "Hospitals" = "Hospitals.Rmd")
  }, ignoreNULL = FALSE)
  
  # choose file names based on chosen practitioner
  params <-  eventReactive(input$update, {
    switch(input$doctor,
           "Dr.1" = list(RA = input$RA$datapath, direct = input$direct$datapath),
           "Dr.2" = list(RA = input$RA$datapath, direct = input$direct$datapath),
           "Dr.3" = list(RA = input$RA$datapath, direct = input$direct$datapath),
           "Hospitals" = list(RA = input$RA$datapath, direct = input$direct$datapath,
                           Hospital_1 = input$Hospital_1$datapath,
                           Hospital_1 = input$Hospital_2$datapath))
  }, ignoreNULL = FALSE)
  
  # Build a pdf report
  output$report <- downloadHandler(
    filename = "report.pdf",
    content = function(file) {
      # Copy the report file to a temporary directory before processing it, in
      # case we don't have write permissions to the current working dir (which
      # can happen when deployed).
      tempReport <- file.path(tempdir(), Dr())
      file.copy(Dr(), tempReport, overwrite = TRUE)
      
      # Set up reactive parameters to pass to Rmd 
      params <- params()
      
      # Knit the document, passing in the `params` list, and evaluate it in a
      # child of the global environment (this isolates the code in the document
      # from the code in this app).
      Sys.setenv(RSTUDIO_PANDOC="C:/Program Files/RStudio/bin/pandoc")
      rmarkdown::render(tempReport, output_file = file,
                        params = params,
                        envir = new.env(parent = globalenv())
      )
    }
  )
}
)
