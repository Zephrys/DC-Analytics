library("shiny")
library("shinyjs")
library("plotly")

library("tm")
library(wordcloud)
library(ggplot2)
library(reshape2)
library(RColorBrewer)

clog = read.csv("clog.csv", stringsAsFactors = TRUE, header = FALSE)
clog$V2 = NULL
clog$V5 = NULL
clog$V6 = NULL
clog$V7 = NULL
clog$V8 = NULL

colnames(clog) = c("timestamp", "ip search", "class")

categories = c("Explicit", "Softwares", "Hindi/Telugu/Japanese/Unclassified", "Indian TV", "Sports", "Indian Movies", "English TV", "Songs", "English Movies", "Academics", "Games")

class_agg = as.data.frame(table(clog$class))
class_agg = subset(class_agg, class_agg$Freq > 10)
class_agg$Var1 = as.factor(class_agg$Var1)

clog$`ip search` = as.character(clog$`ip search`)
clog$timestamp =as.character(clog$timestamp)
clog$timestamp = as.POSIXlt(clog$timestamp,format="%Y-%m-%d %H:%M:%S")


ui <- fluidPage(
  
  navbarPage("DC Analytics",
             tabPanel("Wordclouds",
                        sidebarPanel(
                          selectInput("category", "Categories", choices = categories),
                          sliderInput("max.words", "Maximum Words", min = 1,  max = 500,  value = 150),
                          sliderInput("min.freq","Minimum Frequency:", min = 1,  max = 50, value = 5)

                        ),
                        mainPanel(
                          column(12, plotOutput("wordcloud")),
                          h3("What are wordclouds?"),
                          div("Fun visualizations of what Bitsians are searching for. The selected terms are algorithmically selected, based on their frequency of occurence."),
                          br(),
                          div("This is what you came for?!")
                        )

             ),

          tabPanel("Searches by Hour",
           sidebarPanel(
               selectInput("time_category", "Categories", choices = categories)
             ),
           mainPanel(
             column(12, plotOutput("time_plot")),
             h3("What is searched when?"),
             div("Ever wondered when Bitisans search for porn, and when for Football Matches?"),
             br(),
             div("Go through the plots, and let us know of anycorrelations(if you find any)!")
           )
  ),
  
  tabPanel("Pie Share of Searches",
      mainPanel(
       column(12, plotOutput("plot")),
       h3("What is BITS Pilani searching?"),
       div("I know you expected a bigger percentage for \"Explicit\", but we watch TV Shows too!"),
       div("More than 50% accounted by \"Explicit\" and \"English TV\"!"),
       br(),
       div("And they say DC++ is for Academics...")
      )
   ),
  
  tabPanel("Length of Search Query",
    mainPanel(
      column(12, plotOutput("length_plot")),
      div("Just wondering how long our searches are..."),
      br(),
      div("Seems pretty normal :p")
      )
    ),
  
  tabPanel("About",
    h2("What is this!"),
    div("An attempt by three pSentiSemites at understanding what BITS Pilani thinks, via DC++!"),
    hr(),
    h3("How?"),
    div("We ran a script for 7 days, from the 14th of November to the 20th of November, which logged all searches on Nebula(the DC Hub)."), 
    br(), 
    div("For analytics purposes, we developed a module to classify the search results into 10 broad categories."),
    br(), 
    div("The analytics provided here is based on the data collected in this 7-day period."),
    hr(),
    h3("What next?"),
    br(), 
    div("We have a lot of ideas, like developing a hostel-wise search map, and picking up of certain trends via the searches."),
    br(), 
    div("Modules for real-time analytics are being developed, hold tight!"),
    br(),
    tags$div(class="header", checked=NA,
     tags$p("If you found this interesting and have an idea to pitch in, do contribute!"),
     tags$a(href="https://github.com/Zephrys/DC-Analytics", "Our Github Repository")
    ),
    
    hr(),
    h4("Disclaimer"),
    
    div("Our sole intention is to analyze the search queries, hopefully you're not ashamed of yours :p"),
    hr()
    
    ),
  
  footer = "Analytics by pSentiSem Productions",
  inverse = TRUE,
  collapsable = TRUE
  
  )
)

server <- function(input, output) {
  
  get_words = function(category)({
    category_number = switch (category,
      "Explicit" = 1,
      "Indian TV" = 2,
      "Sports" = 3,
      "Indian Movies" = 4,
      "English TV" = 5,
      "Songs" = 6,
      "English Movies" = 7,
      "Academics" = 8,
      "Games" = 9,
      "Softwares" = 10,
      "Hindi/Telugu/Japanese/Unclassified" = 11
      )
    
    class_clog = subset(clog, clog$class == category_number)
    words = lapply(strsplit(class_clog$`ip search`, ":"), tail, n=1)
    
    text = paste(words, collapse = " ")
    docs <- Corpus(VectorSource(text)) 
    docs <- tm_map(docs, PlainTextDocument)
    docs <- tm_map(docs, content_transformer(tolower))
    docs <- tm_map(docs, removeWords, stopwords("english"))
    docs <- tm_map(docs, removePunctuation)
    docs <- tm_map(docs, stripWhitespace)
    
    return (docs)
  })

  get_length_df = function()({
    words = lapply(strsplit(clog$`ip search`, ":"), tail, n=1)
    df <- data.frame(matrix(unlist(words), nrow=19313, byrow=T),stringsAsFactors=FALSE)
    colnames(df) = c("word")
    df_nrow = data.frame(Group=df$word, x=nchar(df$word))
    return (as.data.frame(table(df_nrow$x)))
  })
  
  get_hourly_data = function(category){
    
    category_number = switch (category,
                              "Explicit" = 1,
                              "Indian TV" = 2,
                              "Sports" = 3,
                              "Indian Movies" = 4,
                              "English TV" = 5,
                              "Songs" = 6,
                              "English Movies" = 7,
                              "Academics" = 8,
                              "Games" = 9,
                              "Softwares" = 10,
                              "Hindi/Telugu/Japanese/Unclassified" = 11
    )
    
    class_clog = subset(clog, clog$class == category_number)
    return (as.data.frame(table(unclass(class_clog$timestamp)$hour)))
    
  }
  output$plot = renderPlot({
    ggplot(class_agg, aes(x=factor(1), y = class_agg$Freq, fill = categories))+
      geom_bar(width = 1, stat = "identity")+
      coord_polar(theta = "y", start = 90)+
      scale_fill_brewer(palette="Set3")+
      labs(x="", y="")+
      ggtitle("Share of Categories Searched")+
      theme_minimal()
  })
  
  output$wordcloud =  renderPlot({
    wordcloud(get_words(input$category), max.words = input$max.words, min.freq = input$min.freq, random.order = FALSE, colors = brewer.pal(8,"Dark2"))
  })
 
  output$length_plot = renderPlot({
    ggplot(get_length_df(), aes(x=Var1, y = Freq))+
      labs(x = "Length of Search Query", y = "Searches")+
      ggtitle("Length of Search Queries")+
      geom_bar(stat="identity", fill="blue")
    
  }) 
  
  output$time_plot = renderPlot({
    
    ggplot(get_hourly_data(input$time_category), aes(x=Var1, y=Freq, group = 1))+
      labs(x = "Hour", y = "Search Count")+
      ggtitle("Search Queries by Time")+
      geom_line()
  })
  
  
}
shinyApp(ui = ui, server = server)
