
#%%
import numpy as np
import pandas as pd
#%%
def bornes(x):
    return np.asarray([[20,99],[1,90],[1,min(0.625*x[1]/0.00954, 0.625*x[0]/0.0193, 200)],[max(10,1296000/(np.pi*x[2]**2)-4/3*x[2]),240]])
#%%
def cout_soudure(x):
    return 1.7781*0.625*x[1]*x[2]**2+ 0.6224*0.625*x[0]*x[2]*x[3] + 3.1661*(0.625*x[0])**2*x[3] + 19.84*(0.625*x[0])**2*x[2]

#%% 
def contraintes(x):
    _bornes = bornes(x)
    for i in range(len(x)) :
        if x[i] < _bornes[i,0] or x[i] > _bornes[i,1]:
            return False
    return True

#%%
def initialiser_points():
    x = np.zeros(4)
    _bornes = bornes(x)
    x[0]= np.random.uniform(high = _bornes[0,1])
    x[1]= np.random.uniform(low =  _bornes[1,0], high =  _bornes[1,1])
    _bornes = bornes(x)
    x[2]= np.random.uniform(high =  _bornes[2,1])
    _bornes = bornes(x)
    x[3]= np.random.uniform(low =  _bornes[3,0], high =  _bornes[3,1])

    return x


#%%
def mutation(candidat):
    _bornes = bornes(candidat)

    
    temp_array = candidat

    cpt=0
    while True: #do-while
        
        if(cpt%10 == 0):
            i = np.random.randint(0,4)
            temp=candidat[i]
        
        temp = candidat[i] + np.random.normal(0,1) * 0.1 * temp * (_bornes[i,1]- _bornes[i,0]) 
        temp_array[i] = temp

        if contraintes(temp_array):
            candidat[i] = temp
            break
        
        cpt+=1
    return candidat

#%%
def calculer_temperature_expo(t, T_init,epsilon_t=0.025): #exponentiel
    return (1-epsilon_t)**t*T_init


#%%
def calculer_temperature_log(t, T_init): # logarithmique
    if t<3:
        return T_init
    return T_init/np.log(t)

#%%
def calculer_temperature_poly(t,T_init,t_max=200, alpha=2): # polynomial
    return (1-t/t_max)**alpha * T_init # t_max est l'iteration maximale pour laquelle la temperature doit etre nulle

#%%
def proba_acceptance(T,deltaE):
    return np.exp(-deltaE/T)
#%%
def print_results(hist):
    
    scores = hist[:,1]
    best_score = min(scores)
    index = np.where(scores == best_score)
    #print(f"index : {index}")
    print(f"meilleurs dimensions : \n z1 = {0.625*hist[index[0][0],3]} \n z2 = {0.625*hist[index[0][0],4]} \n x3 = {hist[index[0][0],5]} \n x4 = {hist[index[0][0],6]}\n")
    print(f"meilleur score : {best_score}\n")

   


#%%
def preparation_table(hist):
    hist[:,3] = [0.625 * a for a in hist[:,3]]
    hist[:,4] = [0.625 * a for a in hist[:,4]]

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
def recuit_simule(T_init = 400,temperature= calculer_temperature_poly,itrs= 100,n = 50, m=10,epsilon = 0.001, verbose = False):
      # T_init ne doit pas etre posee comme ça
      
    
    historique = np.empty([0,7])
    i=0
    while(i<n):
        i+=1
        current_point = initialiser_points()
        best_point = current_point
        current_score = cout_soudure(current_point)
        best_score = current_score
        best_before_score = best_score
        k=0 # iterateur 
        l=0 # iterations pour suivre l'amelioration
        while(k<itrs):
          k+= 1
          
          new_point = mutation(current_point)
          new_score = cout_soudure(new_point)
          
          deltaE = new_score - current_score
          
          best_before_score = best_score

          if  deltaE <= 0 : 
              current_point = new_point
              current_score = new_score
              if current_score < best_score:
                  best_point = current_point
                  best_score = current_score
                
          else :
              T = temperature(k,T_init) + k//m * np.random.uniform(0,1) # Rechauffement apres chaque m iterations
              if np.random.uniform(0,1) < proba_acceptance(T,deltaE):
                  current_point = new_point
                  current_score = new_score


          if best_before_score - best_score < epsilon :  #peu ou pas d'amelioration 
                 l += 1 
          else :
                 l = 0

          if l == 50 : 
              current_point = best_point         #Retour au dernier meilleur point
              current_score = best_score
          

          if verbose :
                print(f"itr : {k}, point : {current_point}, score : {current_score}")
                
        historique = np.append(historique,[np.append([i,best_score,k],[best_point])],axis=0)

    return historique
#%%
while True:
    iter = input("Entrer le nombre d'iterations : ")
    epsilon = input("Entrer epsilon ( progres minimal ) : ")

    if int(iter) > 0 and float(epsilon) > 0:
      break
    else:
      print("Une des valeurs entrees n'est pas acceptee!")
    
hist = recuit_simule(itrs = int(iter), epsilon=float(epsilon))
#%%
print_results(hist)
#%%
print_table(hist)
#%%
print_analyse(hist)
#%%