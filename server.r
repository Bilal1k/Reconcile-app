if (!require("shiny")) install.packages("shiny")


shinyServer(function(input, output) {
  Dr <- eventReactive(input$update, {
    switch(input$doctor,
           "Dr.1" = "Dr1.Rmd",
           "Dr.2" = "Dr2.Rmd",
           "Dr.3" = "Dr3.Rmd",
           "Hospitals" = "Hospitals.Rmd")
  }, ignoreNULL = FALSE)
  output$report <- downloadHandler(

    filename = "report.pdf",
    content = function(file) {
      # Copy the report file to a temporary directory before processing it, in
      # case we don't have write permissions to the current working dir (which
      # can happen when deployed).
      tempReport <- file.path(tempdir(), Dr())
      file.copy(Dr(), tempReport, overwrite = TRUE)
      
      # Set up parameters to pass to Rmd document
      params <- list(RA1 = input$RA1$datapath,
                     RA3 = input$RA3$datapath,
                     RA2 = input$RA2$datapath,
                     direct1 = input$direct1$datapath,
                     direct2 = input$direct2$datapath,
                     direct3 = input$direct3$datapath,
                     Hospital_1 = input$Hospital_1$datapath,
                     Hospital_2 = input$Hospital_2$datapath,
                     RA3H = input$RA3H$datapath,
                     Hospital_1H = input$Hospital_1H$datapath,
                     Hospital_2H = input$Hospital_2H$datapath)
      
      # Knit the document, passing in the `params` list, and eval it in a
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
