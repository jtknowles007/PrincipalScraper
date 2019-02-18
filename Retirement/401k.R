# Script to chart cumulative balance and contribution to 403(b) plan
library(tidyverse)
library(scales)
jk <- read.csv("../401k.csv")
mydate <- as.Date(jk$Date, "%m-%d-%Y")

jk.df <- data.frame(mydate,jk$Total.Balance,jk$Cumulative.Contribution)
colnames(jk.df) <- c("Date","Total","Contribution")

jkview <- ggplot(jk.df, aes(jk.df$Date, y = value)) +
    geom_line(aes(y = jk.df$Total, col="Total")) +
    # geom_line(aes(y = jk.df$Contribution, col="Contribution")) +
    labs(title = "Carla's 401(k) Balance", x="Date", y = "Balance", color="Type") +
    scale_color_brewer(palette="Dark2") +
    scale_x_date(date_breaks = "1 months", date_minor_breaks = "1 month", labels = date_format("%b-%Y")) +

    scale_y_continuous(labels=dollar_format(prefix="$")) +
    theme(plot.title = element_text(hjust = 0.5), axis.text.x = element_text(angle=60,hjust=1))
jkview
