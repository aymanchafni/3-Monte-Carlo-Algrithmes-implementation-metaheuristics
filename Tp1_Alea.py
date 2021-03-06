#%%
import numpy as np
import pandas as pd

def bornes(x):
    return np.asarray([[0,99],[1,100],[1,min(0.625*x[1]/0.00954, 0.625*x[0]/0.0193, 200)],[max(10,1296000/(np.pi*x[2]**2)-4/3*x[2]),240]])
#%%
def cout_soudure(x):
    return 1.7781*0.625*x[1]*x[2]**2+ 0.6224*0.625*x[0]*x[2]*x[3] + 3.1661*(0.625*x[0])**2*x[3] + 19.84*(0.625*x[0])**2*x[2]



#%%
def generer_points(n):
    x = np.zeros([n,4])
    for i in range(n):
        _bornes = bornes(x[i])
        x[i,0]= np.random.uniform(high = _bornes[0,1])
        x[i,1]= np.random.uniform(low =  _bornes[1,0], high =  _bornes[1,1])
        _bornes = bornes(x[i])
        x[i,2]= np.random.uniform(high =  _bornes[2,1])
        _bornes = bornes(x[i])
        x[i,3]= np.random.uniform(low =  _bornes[3,0], high =  _bornes[3,1])

    return x
   

#%%
def print_results(hist):
    
    scores = hist[:,1]
    best_score = min(scores)
    index = np.where(scores == best_score)
    print(f"meilleurs dimensions : \n z1 = {0.625*hist[index[0][0],3]} \n z2 = {0.625*hist[index[0][0],4]} \n x3 = {hist[index[0][0],5]} \n x4 = {hist[index[0][0],6]}\n")
    print(f"meilleur score : {best_score}\n")

    


#%%
def preparation_table(hist):
    hist[:,4] = [0.625 * a for a in hist[:,4]]
    hist[:,3] = [0.625 * a for a in hist[:,3]]

    table = pd.DataFrame(data=hist[:,1:], columns=["Score","Nbr itrs", "z1","z2","x3","x4"], index=hist[:,0]) 
    
    return table

#%%
def print_table(hist):
      print("historique detaille :\n")
      return preparation_table(hist)
#%%
def print_analyse(hist):
    print("Analyse des donnees generees :\n")
    return preparation_table(hist).describe()




#%%
def aleatoire(n = 50, itrs=100,epsilon = 0.001, samples_size = 10 ,verbose = False):
    
     
       #iterateur 
    i=0
    historique = np.empty([0,7])
    while(i<n):
        i+=1
        k=0
        l=0
        current_points = generer_points(samples_size)
        scores = np.apply_along_axis(cout_soudure, arr = current_points, axis = 1)
        score = np.min(scores)
        current_point = current_points[np.argmin(scores),]
        best_point = current_point
        best_score = score
        best_before_score = best_score
        
        while(k<itrs):
          k+=1   
          current_points = generer_points(samples_size)
          scores = np.apply_along_axis(cout_soudure, arr = current_points, axis = 1)

          score = np.min(scores)
          current_point = current_points[np.argmin(scores),]          
          
          best_before_score = best_score

          if(score < best_score):
                best_score = score
                best_point = current_point
          

          if best_before_score - best_score < epsilon :
                 l += 1 
          else :
                 l = 0

          if l == 50 : 
              break
          

          if verbose :
                print(f"itr : {k}, minimum : {current_point}, best score : {score}")
        
        historique = np.append(historique,[np.append([i,best_score,k],[best_point])],axis=0)
    return historique
#%%
while True:
    iter = input("Entrer le nombre d'iterations : ")
    epsilon = input("Entrer epsilon ( progres minimal ) : ")

    if int(iter) > 0 and float(epsilon) > 0:
      break
    else:
      print("Veuillez reesayer!")
    
hist = aleatoire(itrs = int(iter), epsilon=float(epsilon))
#%%
print_results(hist)
#%%
print_table(hist)
#%%
print_analyse(hist)

# %%
