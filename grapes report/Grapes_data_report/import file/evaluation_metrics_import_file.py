import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import time

def save_histogram_for_training_and_testing_data(class_list,training_data_dict,testing_data_dict,file_path):
    
    training_data = []
    for ele in training_data_dict:
        training_data.append(training_data_dict[ele])
    
    testing_data = []
    for ele in testing_data_dict:
        testing_data.append(testing_data_dict[ele])
    
    X_axis = np.arange(len(class_list))

    plt.figure(figsize = (20,25))
    
    plt.bar(X_axis - 0.2, training_data, 0.4, label = 'Training Data')
    plt.bar(X_axis + 0.2, testing_data, 0.4, label = 'Testing Data')
    
    plt.xticks(X_axis, class_list,rotation = 65)
    plt.xlabel("Groups")
    plt.ylabel("Number of Images")
    plt.title("Number of Images in each group")
    plt.legend()
    plt.savefig(file_path)
    plt.close()

import seaborn as sns
import matplotlib.pyplot as plt
from numpy import argmax
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix
from tabulate import tabulate

def save_conf_matrix(model,X_test,y_test,class_list,file_path):
    # Getting y predicted
    y_pred_prob = model.predict(X_test)
    y_pred = []

    for ele in y_pred_prob:
        y_pred.append(argmax(ele))
    
    # Getting Confusion Matrix
    conf_matrix = confusion_matrix(y_true=y_test, y_pred=y_pred)
    plt.figure(figsize = (18,20))
    plot = sns.heatmap(conf_matrix, annot=True,annot_kws={
                    'fontsize': 16,
                    'fontweight': 'bold',
                    'fontfamily': 'serif',
                   # 'color': 'black'
                }, cmap='Blues')

    plot.set_title('\n Seaborn Confusion Matrix with labels \n\n');
    plot.set_xlabel('\n Predicted Category')
    plot.set_ylabel('Actual Category ');

    ## Ticket labels - List must be in alphabetical order
    plot.xaxis.set_ticklabels(class_list,rotation = 80)
    plot.yaxis.set_ticklabels(class_list,rotation = 0)

    ## Display the visualization of the Confusion Matrix.
    plt.savefig(file_path)
    plt.close()


def percentage_accuracy(TP,FP,TN,FN):
    accuracy = (TP + TN) / (TP + FP + TN + FN)
    accur_per = accuracy*100
    return (accur_per)

def percentage_error(TP,FP,TN,FN):
    accur_per = percentage_accuracy(TP,FP,TN,FN)
    return (100 - accur_per)

def precision(TP,FP,TN,FN):
    prec = (TP) / (TP + FP)
    return (prec)

def recall(TP,FP,TN,FN):
    rec = (TP) / (TP + FN)
    return (rec)

def sensitivity(TP,FP,TN,FN):
    sen = (TP) / (TP + FN)
    return (sen)

def specificity(TP,FP,TN,FN):
    spec = (TN) / (FP + TN)
    return (spec)

def f1_score(TP,FP,TN,FN):
    prec = precision(TP,FP,TN,FN)
    rec = recall(TP,FP,TN,FN)
    f1_sc = (2*prec*rec) / (prec + rec)
    return (f1_sc)

def G_mean(TP,FP,TN,FN):
    spec  = specificity(TP,FP,TN,FN)
    prec = precision(TP,FP,TN,FN)
    return np.sqrt(spec*prec)

def MCC(TP,FP,TN,FN):
    num = (TP*TN) - (FP-FN)
    den = (TP + FP)*(TP + FN)*(TN + FP)*(TN + FN)
    return num/(np.sqrt(den))
    

def print_evaluation_metrics(model,X_test_numpy_array,y_test,file_path):
    y_pred_prob = model.predict(X_test_numpy_array)
    y_pred = []

    for ele in y_pred_prob:
        y_pred.append(argmax(ele))
        
    cnf_matrix =  confusion_matrix(y_true=y_test, y_pred=y_pred)
    
    # Calculating True Positive, False Positive, True Negative, False Negative
    FP = cnf_matrix.sum(axis=0) - np.diag(cnf_matrix) 
    FN = cnf_matrix.sum(axis=1) - np.diag(cnf_matrix)
    TP = np.diag(cnf_matrix)
    TN = cnf_matrix.sum() - (FP + FN + TP)
    
    FP = FP.astype(float)
    FN = FN.astype(float)
    TP = TP.astype(float)
    TN = TN.astype(float)
    
    # Accuracy
    accuracy = percentage_accuracy(TP,FP,TN,FN)
    accuracy = list(accuracy)
    accuracy.append("Accuracy")
    
    # Percentage Error
    error_per = percentage_error(TP,FP,TN,FN)
    error_per = list(error_per)
    error_per.append("Error")
    
    # Precision
    prec = precision(TP,FP,TN,FN)
    prec = list(prec)
    prec.append("Precision")
    
    # Recall
    rec = recall(TP,FP,TN,FN)
    rec = list(rec)
    rec.append("Recall")
    
    # Sensitivity
    sen = sensitivity(TP,FP,TN,FN)
    sen = list(sen)
    sen.append("Sensitivity")
    
    # Specificity
    spec = specificity(TP,FP,TN,FN)
    spec = list(spec)
    spec.append("Specificity")
    
    # F1 Score
    f_sc = f1_score(TP,FP,TN,FN)
    f_sc = list(f_sc)
    f_sc.append("F1 Score")
    
    # G Mean
    g_mean = G_mean(TP,FP,TN,FN)
    g_mean = list(g_mean)
    g_mean.append("G Mean")
    
    # MCC ( Matthews Correlation Coefficient )
    mcc = MCC(TP,FP,TN,FN)
    mcc = list(mcc)
    mcc.append("Matthews Correlation Coefficient")
    
    data = [accuracy,error_per,prec,rec,sen,spec,f_sc,g_mean,mcc]
    head = ["Class 1","Class 2","Class 3","Class 4","Measure"]
    
    res_df = pd.DataFrame(data,columns = head)
    res_df.to_excel(file_path)
    
    print("\n\n Report \n\n\n")
    print(tabulate(data, headers=head, tablefmt="grid"))

def save_of_training_loss_vs_epochs(model_history,epochs,file_path):
    color = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan']
    sz = len(model_history)
    total_x_label = epochs+1

    plt.figure(figsize = (20,20))
    labels = ["Proposed Model 1","SoyNet Model","Xception Model","Densenet 121 Model","AlexNet Model","VGG16 Model","ResNet 50 Model","EfficientNetB2 Model"]


    for i in range(sz): 
        try:
            loss_train = model_history[i]['loss']
        except:
            model_history[i] = model_history[i].history
            loss_train = model_history[i]['loss']
        epochs = range(1,total_x_label)
        plt.plot(epochs, loss_train, color[i], label=labels[i])
        
    plt.title('Training loss \n')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend(loc ="lower left")
    plt.savefig(file_path)
    plt.close()

def save_of_training_accuracy_vs_epochs(model_history,epochs,file_path):
    color = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan']
    sz = len(model_history)
    total_x_label = epochs+1

    plt.figure(figsize = (20,20))
    labels = ["Proposed Model 1","SoyNet Model","Xception Model","Densenet 121 Model","AlexNet Model","VGG16 Model","ResNet 50 Model","EfficientNetB2 Model"]

    for i in range(sz): 
        try:
            acc_train = model_history[i]['accuracy']
        except:
            model_history[i] = model_history[i]['accuracy']
            acc_tarin = model_history[i]['accuracy']
        epochs = range(1,total_x_label)
        plt.plot(epochs, acc_train, color[i] , label=labels[i])
    plt.title('Training Accuracy\n')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend(loc ="lower right")
    plt.savefig(file_path)
    plt.close()

def save_histogram_for_training_and_testing_accuracy(model_list,training_acc,testing_acc,file_path):
    
    X_axis = np.arange(len(model_list))

    plt.figure(figsize = (20,25))
    
    plt.bar(X_axis - 0.2, training_acc, 0.4, label = 'Training Acc')
    plt.bar(X_axis + 0.2, testing_acc, 0.4, label = 'Testing Acc')
    
    plt.xticks(X_axis, model_list,rotation = 65)
    plt.xlabel("Models")
    plt.ylabel("Accuracy")
    plt.title("Models Accuarcy")
    plt.legend(loc ="upper right")
    plt.savefig(file_path)
    plt.close()

def func_help():
    print("save_histogram_for_training_and_testing_accuracy(model_list,training_acc,testing_acc,file_path)")
    print("save_of_training_accuracy_vs_epochs(model_history,epochs,file_path)")
    print("save_of_training_loss_vs_epochs(model_history,epochs,file_path)")
    print("print_evaluation_metrics(model,X_test_numpy_array,y_test,file_path)")
    print("save_conf_matrix(model,X_test,y_test,class_list,file_path)")
    print("save_histogram_for_training_and_testing_data(class_list,training_data_dict,testing_data_dict,file_path)")
