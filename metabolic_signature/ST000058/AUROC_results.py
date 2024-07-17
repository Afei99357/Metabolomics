import pandas as pd
import operator
import numpy as np
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import matplotlib.pyplot as plt


df = pd.read_csv('/Users/yliao13/Desktop/st000058/aligned.csv')
df_factor = pd.read_csv('/Users/yliao13/Desktop/st000058/factors.csv')

for index, item in df_factor.iterrows():
    item['local_sample_id'] = item['local_sample_id'].strip()

df_height = df.loc[:, [' height' in i for i in df.columns]]
df_height = df_height.fillna(0)
df_height_transposed = df_height.T

groups = ['Group 2', 'Group 3', 'Group 4', 'Group 5', 'Group 6', 'Group 7']
time_course = ['2_hours', '4_hours', '8_hours', '12_hours', '24_hours', '48_hours']



df_new = pd.DataFrame(columns=df_height_transposed.columns)
df_new['target'] = ''
target = []

for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()

    treatment_type = df_factor[df_factor['local_sample_id'] == local_sample_id]['Treatment'].values[0]

    if operator.contains(treatment_type, "Methionine"):
        target.append(0)
        df_new = df_new.append(row)
        df_new.loc[index]['target'] = 0
    if operator.contains(treatment_type, "Homocysteine"):
        if treatment_type.endswith("Group 7"):
            target.append(1)
            df_new = df_new.append(row)
            df_new.loc[index]['target'] = 1

target = np.array(target)

df_new = df_new.iloc[:, :-1]

df_new = df_new.reset_index(drop=True)

# # create empty numpy array to store test values and predict values
# test_values = np.zeros(shape=(len(target), 2))
# predicted_values = np.zeros(shape=(len(target), 2))
test_values = []
predicted_values = []

scaler = StandardScaler()

for i in range(len(df_new)):
    train_selection = [j for j in range(len(df_new)) if i != j]
    test_selection = [i]

    train_x = df_new.iloc[train_selection, :]
    train_y = target[train_selection]

    test_x = df_new.iloc[test_selection, :]
    test_y = target[test_selection]

    train_x = pd.DataFrame(scaler.fit_transform(train_x)).values
    ####### PLS-DA ########
    plsr = PLSRegression(n_components=2, scale=False)
    plsr.fit(train_x, train_y)

    test_x = pd.DataFrame(scaler.fit_transform(test_x)).values
    predict_y = plsr.predict(test_x)[0]

    test_values.append(test_y[0])
    predicted_values.append(predict_y[0])


fpr, tpr, _ = metrics.roc_curve(test_values, predicted_values)
auc = metrics.roc_auc_score(test_values, predicted_values)

plt.plot(fpr, tpr, label="AUC="+str(auc))
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.legend(loc=4)
plt.show()




