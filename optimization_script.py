import pandas as pd
import numpy as np

import optimization.optimization_module as opt

print('Prepare plot with number of clusters description')

alerts = pd.read_csv("alerts.csv", index_col=0)
alerts_classes = alerts[' Class']
alerts_classes = alerts_classes.loc[alerts_classes != 'unknown']
df_full = pd.read_csv('Final_Database.csv', header = None, index_col=0)

best_cluster_n = 1
best_vec_perc = 0.5
best_neighbors_n = 5
val_opt = 0
best_method = ""
for cluster_n in range(8,20, 1):
    for vec_perc in np.arange(0.5, 1.0, 0.05):
        for n_neighbors in range(5, 15, 1):
            print(val_opt)
            val, method = opt.check_value(df_full, alerts_classes, cluster_n, vec_perc, n_neighbors)
            if val > val_opt:
                best_cluster_n = cluster_n
                best_vec_perc = vec_perc
                best_neighbors_n = n_neighbors
                val_opt = val
                best_method = method

with open('Optim_result.csv', 'w') as input:
    input.write('Best value: ' + str(val_opt) + '\n' + 'cluster_n: ' + str(best_cluster_n) + '\n' +
            'vec_perc: ' + str(vec_perc) + '\n' + 'neighbors_n: ' + str(best_neighbors_n) + '\n' +
            'best_method: ' + method)

print('Best value is '+str(val_opt))
print('cluster_n: '+ str(best_cluster_n))
print('vec_perc: '+ str(best_vec_perc))
print('neighbors_n: '+ str(best_neighbors_n))
