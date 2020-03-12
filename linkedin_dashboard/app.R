#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(tidyverse)
df_jobs <- read_csv("../jobs_df_clean.csv")

#Job title types (Analyst, Scientist, Engineer, Manager)
#unique(df_jobs$title)
df_jobs <- df_jobs %>% 
    mutate(job_type = if_else(grepl(df_jobs$title, pattern="analyst", ignore.case = T), "Data Analyst", 
                              if_else(grepl(df_jobs$title, pattern="engineer", ignore.case = T), "Data Engineer",
                                      if_else(grepl(df_jobs$title, pattern="manager", ignore.case = T), "Data Science Manager",
                                       "Data Scientist")))
           )
job_types <- df_jobs %>% pull(job_type) %>% unique()

#Cities
#unique(df_jobs$location)
rename_cities <- function(df, city_name){
    #col = enquo(col)
    df$city[grepl(df$city, pattern=city_name, ignore.case = TRUE)] <- city_name
    return(df)
}

df_jobs$city <- df_jobs$location
df_jobs$city[grepl(df_jobs$location, pattern="QU,|Montréal")] <- "Montreal"
df_jobs$city[grepl(df_jobs$location, pattern="Quebec")] <- "Montreal"
df_jobs$city[grepl(df_jobs$location, pattern="ON,|Ontario")] <- "Toronto"
df_jobs$city[grepl(df_jobs$location, pattern="BC|British Columbia|Vancouver")] <- "Vancouver"
df_jobs$city[grepl(df_jobs$location, pattern="NY,|New York")] <- "Greater New York Area"
df_jobs$city[grepl(df_jobs$location, pattern="MA,")] <- "Greater Boston Area"
df_jobs$city[grepl(df_jobs$location, pattern="Massachusetts")] <- "Greater Boston Area"
df_jobs$city[grepl(df_jobs$location, pattern="Maryland|MD")] <- "Washington DC Area"
df_jobs$city[grepl(df_jobs$location, pattern="NC,")] <- "Raleigh, NC"
df_jobs$city[grepl(df_jobs$location, pattern="District of Columbia|DC|D\\.C\\.")] <- "Washington DC Area"

city_list <- c("Arlington", "Alexandria", "Vienna", "Bellevue", "Toronto", "Burlingame", "Cupertino", "San Carlos", "San Mateo", "Santa Clara",  "Sunnyvale", "McLean", "Campbell", "Dublin", "Menlo Park", "Redwood City", "Palo Alto", "Herndon", "Mountain View", "Montréal", "Raleigh", "Boston", "New York", "Seattle", "San Francisco", "San Jose")
for (citi in city_list){
    df_jobs <- rename_cities(df=df_jobs, city_name=citi)
}

cities <- df_jobs %>% group_by(city) %>% summarize(n=n()) %>% arrange(desc(n))
cities <- cities %>% filter(n>4) %>% pull(city) %>% unique()
#cities
# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("LinkedIn Data Scientists Jobs"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            selectInput(inputId = "city_hub",
                        label = "Choose a city:",
                        choices = cities),
            selectInput(inputId = "job",
                        label = "Choose a job type:",
                        choices = job_types),
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("skill_plot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    datasetInput <- reactive({
        city_hub = input$city_hub
        job = input$job
        
        #Filter dataset based on user inputs
        dat <- df_jobs %>% 
            filter(city == city_hub) %>% 
            filter(job_type == job)
    })
    output$skill_plot <- renderPlot({
        dat <- datasetInput()
        dat %>% 
            select(location, job_type, bigquery_Requirements:university_Requirements) %>% 
            group_by(location, job_type) %>% 
            summarize_all(.funs=sum) %>% 
            gather(key="attribute", value="value", -location, -job_type) %>% 
            separate(attribute, into =c("skill", "level"), sep="_") %>% 
            #mutate(skill = as.factor(skill, levels=skill[desc(value)]), ordered=TRUE) %>% 
            #mutate(skill=as.factor(skill)) %>% 
            #fct_relevel(skill, .x=skill, .fun=median) %>% 
            ggplot(aes(x=skill, y=value, fill=level)) +
            geom_col() +
            coord_flip() +
            theme_minimal() +
            #facet_wrap()
            NULL
        # generate bins based on input$bins from ui.R
        # x    <- faithful[, 2]
        # bins <- seq(min(x), max(x), length.out = input$bins + 1)

        # draw the histogram with the specified number of bins
        # hist(x, breaks = bins, col = 'darkgray', border = 'white')
    })
    
}

# Run the application 
shinyApp(ui = ui, server = server)
