inmates <- read.csv("C:/Users/Administrator/Desktop/School/Spring2024/DTSC_3010_IntroTo_DataScience/Data/Inmate_Texas_Cleaned_December 2023.csv")
inmates
summary(inmates)
hist(inmates$Age)  
mean(inmates$Age,trim = 0, na.rm = TRUE)

install.packages('ggplot2')
library('ggplot2')

# density plot, density inmates age
d<- density(inmates$Age, na.rm = TRUE)
plot(d)


library(dplyr)
#gender bar graph

ggplot(inmates, aes(Gender, fill = Gender))+geom_bar()+ggtitle("Bar Graph of inmate Gender")

#Race bar graph

ggplot(inmates, aes(Race, fill = Race))+geom_bar()+ggtitle("Bar Graph of inmate Race")

#race and parole decision
ggplot(inmates, aes(LastParoleDecision,fill =LastParoleDecision))+geom_bar()+ggtitle(" Bar Graph of Last parole decision")

#scatter plot of race and last parole decision
p <- ggplot(inmates, aes(factor(Race), LastParoleDecision)) 
p + geom_boxplot() + ggtitle(" Scatter plot of Race and Last parole decision")+geom_jitter() + theme_bw()

#scatter plot of Gender and last parole decision
p <- ggplot(inmates, aes(factor(Gender), LastParoleDecision)) 
p + geom_boxplot() + ggtitle(" Scatter plot of Gender and Last parole decision")+geom_jitter() + theme_bw()

#scatter plot of Race and Parole Eligibility
p <- ggplot(inmates, aes(factor(Race), ParoleEligibility)) 
p + geom_boxplot() + ggtitle(" Scatter plot of Race and Last parole decision")+geom_jitter() + theme_bw()

#factor categorical variables

inmates$Gender <- as.factor(inmates$Gender)
inmates$Race <- as.factor(inmates$Race)
inmates$ParoleEligibility <- as.factor(inmates$ParoleEligibility)
inmates$LastParoleDecision <- as.factor(inmates$LastParoleDecision)

#group scatter plot
pairs(~Gender+Age+ParoleEligibility+Race+LastParoleDecision,data=inmates,
      main="Scatterplot Matrix", cex = .25)
library(caret)

#factor categorical variables
inmates$Gender <- as.factor(inmates$Gender)
inmates$Race <- as.factor(inmates$Race)
inmates$ParoleEligibility <- as.factor(inmates$ParoleEligibility)
inmates$LastParoleDecision <- as.factor(inmates$LastParoleDecision)

#linear model age using gender and race and parole eligibility
model <- lm(Age ~ Gender + Race+ParoleEligibility, data = inmates)
summary(model)

#Test and Train Split
sample_size <- floor(0.8*nrow(inmates))

#check training data size
sample_size

#get the index of training samples
train_ind <- sample(seq_len(nrow(inmates)), size = sample_size)

#generate the train and test dataset
train <- inmates[train_ind,]
test <- inmates[-train_ind,]

#check how the train and test dataset look like
head(train)
head(test)

#train a simple linear model with training data 
model<- lm (Age ~ Gender + Race+ParoleEligibility,data = train)

#model summary
summary(model)

#optional diagnosis graphs
layout(matrix(c(1,2,3,4),2,2))
plot(model)

#evaluate the model on test data
prediction <- predict(model,newdata = test)

#check head of the prediction
summary(prediction)

#compute root mean square error(RMSE)
install.packages("hydroGOF")
library("hydroGOF")

rmse(prediction,test$Age,na.rm = TRUE)

#test correlation between predicted values and real values
cor.test(prediction,test$Age, use = "complete")

#train linear models with regularization
train<-train[complete.cases(train),]

#set cross validation method: 5 fold CV, repeated two times
fitControl <- trainControl(
  method = "repeatedcv",
  number = 5,
  repeats =2
)

#train the model
glmFit1 <-train(Age ~ Gender + Race+ParoleEligibility,data = train,
                method = "penalized",
                trControl = fitControl)
1
#check the model
glmFit1

#apply the model on the test data
test <- test[complete.cases(test),]
prediction <- predict(glmFit1,newdata = test)

#evaluate prediction on the test data
rmse(prediction,test$Age)

cor.test(prediction,test$Age)


library(caret)
#Decision tree

svmradial <- train(LastParoleDecision ~Gender + Race+ParoleEligibility, data = train,
                   method="C5.0",
                   trControl=fitControl)
#apply model

prediction_svmradial <- predict(svmradial, newdata = test)

      #evaluate prediction

confusionMatrix(prediction_svmradial,test$LastParoleDecision)


   #Support Vector Machine with linear Kernel

svmpoly <- train(LastParoleDecision ~ Gender + Race+ParoleEligibility, data = train,
                 method="svmPoly",
                 trControl=fitControl)
#apply model

svmpoly

prediction_svmpoly <- predict(svmpoly, newdata = test)

#evaluate prediction

confusionMatrix(prediction_svmpoly,test$LastParoleDecision)

