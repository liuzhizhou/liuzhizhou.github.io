import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import beta
import scipy.stats as stats
import sympy
import math

def generatePriorSample(model = 1, method = 'gibbs', size = 10):
    """
    prior distribution comes from Uniform(0,1)
    `model == 1` means p1 < p2 < p3 < p4 < p5
    `model == 2` means p1 > p2 > p3 > p4 > p5
    `model == 3` means p1 < p2 < p3 > p4 > p5

    Method 
    - `method == 'sequential'` 
    - `method == 'reorder'`
    - `method == 'gibbs'`
    means generating the sample by sequential order, reordering or gibbs sampling, 
    respectively.
    """
    if method == 'sequential':
        if model == 1:
            p1Array = np.random.uniform(0,1,size)
            p2Array = np.array([np.random.uniform(p1,1) for p1 in p1Array])
            p3Array = np.array([np.random.uniform(p2,1) for p2 in p2Array])
            p4Array = np.array([np.random.uniform(p3,1) for p3 in p3Array])
            p5Array = np.array([np.random.uniform(p4,1) for p4 in p4Array])
            return p1Array, p2Array, p3Array, p4Array, p5Array

        elif model == 2:
            p1Array = np.random.uniform(0,1,size)
            p2Array = np.array([np.random.uniform(0,p1) for p1 in p1Array])
            p3Array = np.array([np.random.uniform(0,p2) for p2 in p2Array])
            p4Array = np.array([np.random.uniform(0,p3) for p3 in p3Array])
            p5Array = np.array([np.random.uniform(0,p4) for p4 in p4Array])
            return p1Array, p2Array, p3Array, p4Array, p5Array
        
        elif model == 3:
            p1Array = np.random.uniform(0,1,size)
            p2Array = np.array([np.random.uniform(p1,1) for p1 in p1Array])
            p3Array = np.array([np.random.uniform(p2,1) for p2 in p2Array])
            p4Array = np.array([np.random.uniform(0,p3) for p3 in p3Array])
            p5Array = np.array([np.random.uniform(0,p4) for p4 in p4Array])
            return p1Array, p2Array, p3Array, p4Array, p5Array
    
        else: raise ValueError("Model NOT found.")
    elif method == 'reorder':
        data = np.random.uniform(0,1,(size,5))
        dataSort = np.sort(data,axis=1)
        if model == 1:
            p1Array = dataSort[:,0]
            p2Array = dataSort[:,1]
            p3Array = dataSort[:,2]
            p4Array = dataSort[:,3]
            p5Array = dataSort[:,4]
            return p1Array, p2Array, p3Array, p4Array, p5Array
        elif model == 2:
            p1Array = dataSort[:,4]
            p2Array = dataSort[:,3]
            p3Array = dataSort[:,2]
            p4Array = dataSort[:,1]
            p5Array = dataSort[:,0]
            return p1Array, p2Array, p3Array, p4Array, p5Array
        elif model == 3:
            # Note that M3 does not fully specify the order
            # There are 6 situations, each of them w.p. 1/6
            # dice = 0,1,2,3,4,5 corresponding to:
            # 0: p3 > p2 > p1 > p4 > p5
            # 1: p3 > p2 > p4 > p1 > p5
            # 2: p3 > p2 > p4 > p5 > p1
            # 3: p3 > p4 > p2 > p1 > p5
            # 4: p3 > p4 > p2 > p5 > p1
            # 5: p3 > p4 > p5 > p2 > p1
            p1Array = np.zeros(size)
            p2Array = np.zeros(size)
            p3Array = np.zeros(size)
            p4Array = np.zeros(size)
            p5Array = np.zeros(size)
            for i in range(size):
                dice = np.random.choice(range(6), p=[1/6]*6)
                if dice == 0:
                    p3Array[i] = dataSort[i,4]
                    p2Array[i] = dataSort[i,3]
                    p1Array[i] = dataSort[i,2]
                    p4Array[i] = dataSort[i,1]
                    p5Array[i] = dataSort[i,0]
                elif dice == 1:
                    p3Array[i] = dataSort[i,4]
                    p2Array[i] = dataSort[i,3]
                    p4Array[i] = dataSort[i,2]
                    p1Array[i] = dataSort[i,1]
                    p5Array[i] = dataSort[i,0]
                elif dice == 2:
                    p3Array[i] = dataSort[i,4]
                    p2Array[i] = dataSort[i,3]
                    p4Array[i] = dataSort[i,2]
                    p5Array[i] = dataSort[i,1]
                    p1Array[i] = dataSort[i,0]
                elif dice == 3:
                    p3Array[i] = dataSort[i,4]
                    p4Array[i] = dataSort[i,3]
                    p2Array[i] = dataSort[i,2]
                    p1Array[i] = dataSort[i,1]
                    p5Array[i] = dataSort[i,0]
                elif dice == 4:
                    p3Array[i] = dataSort[i,4]
                    p4Array[i] = dataSort[i,3]
                    p2Array[i] = dataSort[i,2]
                    p5Array[i] = dataSort[i,1]
                    p1Array[i] = dataSort[i,0]
                elif dice == 5:
                    p3Array[i] = dataSort[i,4]
                    p4Array[i] = dataSort[i,3]
                    p5Array[i] = dataSort[i,2]
                    p2Array[i] = dataSort[i,1]
                    p1Array[i] = dataSort[i,0]
                else: raise ValueError("Unexpected value for dice.")
            return p1Array, p2Array, p3Array, p4Array, p5Array
        else: raise ValueError("Model NOT found.")
    elif method == 'gibbs':
        p1Array = np.zeros(size)
        p2Array = np.zeros(size)
        p3Array = np.zeros(size)
        p4Array = np.zeros(size)
        p5Array = np.zeros(size)

        if model == 1:
            p1Array[0] = 1/10
            p2Array[0] = 3/10
            p3Array[0] = 5/10
            p4Array[0] = 7/10
            p5Array[0] = 9/10
            i = 0
            while i < size-1:
                cand1 = np.random.uniform(0,p2Array[i])
                cand2 = np.random.uniform(p1Array[i],p3Array[i])
                cand3 = np.random.uniform(p2Array[i],p4Array[i])
                cand4 = np.random.uniform(p3Array[i],p5Array[i])
                cand5 = np.random.uniform(p4Array[i],1)
                if (cand1 < cand2 < cand3 < cand4 < cand5):
                    p1Array[i+1] = cand1
                    p2Array[i+1] = cand2
                    p3Array[i+1] = cand3
                    p4Array[i+1] = cand4
                    p5Array[i+1] = cand5
                    i +=1
            return p1Array, p2Array, p3Array, p4Array, p5Array
        
        elif model == 2:
            p5Array[0] = 1/10
            p4Array[0] = 3/10
            p3Array[0] = 5/10
            p2Array[0] = 7/10
            p1Array[0] = 9/10

            i = 0
            while i < size-1:
                cand1 = np.random.uniform(p2Array[i],1)
                cand2 = np.random.uniform(p3Array[i],p1Array[i])
                cand3 = np.random.uniform(p4Array[i],p2Array[i])
                cand4 = np.random.uniform(p5Array[i],p3Array[i])
                cand5 = np.random.uniform(0,p4Array[i])
                if (cand1 > cand2 > cand3 > cand4 > cand5):
                    p1Array[i+1] = cand1
                    p2Array[i+1] = cand2
                    p3Array[i+1] = cand3
                    p4Array[i+1] = cand4
                    p5Array[i+1] = cand5
                    i +=1
            return p1Array, p2Array, p3Array, p4Array, p5Array

        elif model == 3:
            p5Array[0] = 0
            p4Array[0] = 0.1
            p3Array[0] = 5/10
            p2Array[0] = 0.1
            p1Array[0] = 0
            i = 0
            while i < size-1:
                cand1 = np.random.uniform(0,p2Array[i])
                cand2 = np.random.uniform(p1Array[i],p3Array[i])
                cand3 = np.random.uniform(max(p2Array[i],p4Array[i]),1)
                cand4 = np.random.uniform(p5Array[i],p3Array[i])
                cand5 = np.random.uniform(0,p4Array[i])
                if (cand1 < cand2 < cand3 and cand3 > cand4 > cand5):
                    p1Array[i+1] = cand1
                    p2Array[i+1] = cand2
                    p3Array[i+1] = cand3
                    p4Array[i+1] = cand4
                    p5Array[i+1] = cand5
                    i +=1
            return p1Array, p2Array, p3Array, p4Array, p5Array
        
        else: raise ValueError("Model NOT found.")

def generateAllThree(model,size):
    MSequential = generatePriorSample(model=model, method='sequential', size=size)
    MReorder = generatePriorSample(model=model, method='reorder', size=size)
    MGibbs = generatePriorSample(model=model, method='gibbs', size=size)
    return MSequential, MReorder, MGibbs

def pltAllThree(modelData,title):
    methods = ["Sequential","Reorder","Gibbs"]
    fig, axes = plt.subplots(1,3,figsize=(20,8))
    m = 0
    for ax in axes:
        for i in range(5):
            sns.kdeplot(modelData[m][i],ax=ax,color=colors[i],label= f"p{i+1}")
        ax.legend()
        ax.set_title(methods[m])
        m += 1
    fig.suptitle(title)
    plt.savefig(f'{title}.pdf')

def liklihood(pmaxs,D=[(0,3),(1,6),(4,12),(3,6),(0,0)]):
    Prod = 1
    for j in range(5):
        yj, nj = D[j]
        Prod *= math.comb(nj,yj)*(pmaxs[j] ** yj) * (1-pmaxs[j]) ** (nj-yj)
    return Prod

def generatePosteriorSample(model = 1, size = 10, D=None):
    if D == None:
        raise ValueError("No Data")
    p1Array = np.zeros(size)
    p2Array = np.zeros(size)
    p3Array = np.zeros(size)
    p4Array = np.zeros(size)
    p5Array = np.zeros(size)

    y1, n1 = D[0]
    y2, n2 = D[1]
    y3, n3 = D[2]
    y4, n4 = D[3]
    y5, n5 = D[4]

    if model == 1:
        p1Array[0] = 1/10
        p2Array[0] = 3/10
        p3Array[0] = 5/10
        p4Array[0] = 7/10
        p5Array[0] = 9/10
        i = 0
        while i < size-1:
            cand1 = np.random.beta(y1+1,n1-y1+1)
            cand2 = np.random.beta(y2+1,n2-y2+1)
            cand3 = np.random.beta(y3+1,n3-y3+1)
            cand4 = np.random.beta(y4+1,n4-y4+1)
            cand5 = np.random.beta(y5+1,n5-y5+1)
            if (cand1 < cand2 < cand3 < cand4 < cand5):
                p1Array[i+1] = cand1
                p2Array[i+1] = cand2
                p3Array[i+1] = cand3
                p4Array[i+1] = cand4
                p5Array[i+1] = cand5
                i +=1
        return p1Array, p2Array, p3Array, p4Array, p5Array
    
    elif model == 2:
        p5Array[0] = 1/10
        p4Array[0] = 3/10
        p3Array[0] = 5/10
        p2Array[0] = 7/10
        p1Array[0] = 9/10
        i = 0
        while i < size-1:
            cand1 = np.random.beta(y1+1,n1-y1+1)
            cand2 = np.random.beta(y2+1,n2-y2+1)
            cand3 = np.random.beta(y3+1,n3-y3+1)
            cand4 = np.random.beta(y4+1,n4-y4+1)
            cand5 = np.random.beta(y5+1,n5-y5+1)
            if (cand1 > cand2 > cand3 > cand4 > cand5):
                p1Array[i+1] = cand1
                p2Array[i+1] = cand2
                p3Array[i+1] = cand3
                p4Array[i+1] = cand4
                p5Array[i+1] = cand5
                i +=1
        return p1Array, p2Array, p3Array, p4Array, p5Array

    elif model == 3:
        p5Array[0] = 0
        p4Array[0] = 0.1
        p3Array[0] = 5/10
        p2Array[0] = 0.1
        p1Array[0] = 0
        i = 0
        while i < size-1:
            cand1 = np.random.beta(y1+1,n1-y1+1)
            cand2 = np.random.beta(y2+1,n2-y2+1)
            cand3 = np.random.beta(y3+1,n3-y3+1)
            cand4 = np.random.beta(y4+1,n4-y4+1)
            cand5 = np.random.beta(y5+1,n5-y5+1)
            if (cand1 < cand2 < cand3 and cand3 > cand4 > cand5):
                p1Array[i+1] = cand1
                p2Array[i+1] = cand2
                p3Array[i+1] = cand3
                p4Array[i+1] = cand4
                p5Array[i+1] = cand5
                i +=1
        return p1Array, p2Array, p3Array, p4Array, p5Array
    
    else: raise ValueError("Model NOT found.")

def pltPosterior(PData,title):
    fig, ax = plt.subplots(1,1,figsize=(7,8))
    pmaxs = []
    for i in range(5):
        sns.kdeplot(PData[i],ax=ax,color=colors[i],label= f"p{i+1}")
        data = ax.lines[i].get_xydata()
        pmaxs.append(data[np.where(data[:, 1] == max(data[:, 1]))][0][0])
    ax.legend()
    fig.suptitle(title)
    plt.savefig(f'{title}.pdf')
    return pmaxs

def trunc_Beta_pdf(x, a, b, trunc_start, trunc_end):
    return stats.beta.pdf(x, a, b)/(stats.beta.cdf(trunc_end,a, b)-stats.beta.cdf(trunc_start,a, b)) if trunc_start < x < trunc_end else 0

colors = ['#40a798','#3b4a6b','#22b2da','#f0d43a','#f98b60']

D = [(0,3),(1,6),(4,12),(3,6),(0,0)]
y1, n1 = D[0]
y2, n2 = D[1]
y3, n3 = D[2]
y4, n4 = D[3]
y5, n5 = D[4]
I = 100000

M1 = generateAllThree(1, I)
pltAllThree(M1,"Model1")
print("Loading...")
PDGM1_priorBySequential = np.mean([liklihood([M1[0][j][i] for j in range(5)]) for i in range(I)])
PDGM1_priorByReorder = np.mean([liklihood([M1[1][j][i] for j in range(5)]) for i in range(I)])
PDGM1_priorByGibbs = np.mean([liklihood([M1[2][j][i] for j in range(5)]) for i in range(I)])
print("Loading...")

M2 = generateAllThree(2, I)
pltAllThree(M2,"Model2")
print("Loading...")

PDGM2_priorBySequential = np.mean([liklihood([M2[0][j][i] for j in range(5)]) for i in range(I)])
PDGM2_priorByReorder = np.mean([liklihood([M2[1][j][i] for j in range(5)]) for i in range(I)])
PDGM2_priorByGibbs = np.mean([liklihood([M2[2][j][i] for j in range(5)]) for i in range(I)])
print("Loading...")

M3 = generateAllThree(3, I)
pltAllThree(M3,"Model3")
print("Loading...")

PDGM3_priorBySequential = np.mean([liklihood([M3[0][j][i] for j in range(5)]) for i in range(I)])
PDGM3_priorByReorder = np.mean([liklihood([M3[1][j][i] for j in range(5)]) for i in range(I)])
PDGM3_priorByGibbs = np.mean([liklihood([M3[2][j][i] for j in range(5)]) for i in range(I)])
print("Loading...")


M1Posterior = generatePosteriorSample(model = 1, size = I, D=D)
M1pmaxs = pltPosterior(M1Posterior,"M1Posterior")
P1M1 = np.mean([trunc_Beta_pdf(M1pmaxs[0], y1+1, n1-y1+1, 0, M1Posterior[1][i]) for i in range(I)])
P2G1M1 = np.mean([trunc_Beta_pdf(M1pmaxs[1], y2+1, n2-y2+1, M1pmaxs[0], M1Posterior[2][i]) for i in range(I)])
P3G12M1 = np.mean([trunc_Beta_pdf(M1pmaxs[2], y3+1, n3-y3+1, M1pmaxs[1], M1Posterior[3][i]) for i in range(I)])
P4G123M1 = np.mean([trunc_Beta_pdf(M1pmaxs[3], y4+1, n4-y4+1, M1pmaxs[2], M1Posterior[4][i]) for i in range(I)])
P5G1234M1 = trunc_Beta_pdf(M1pmaxs[4], y5+1, n5-y5+1, M1pmaxs[3], 1)
PthetaGDM1 = P1M1 * P2G1M1 * P3G12M1 * P4G123M1 * P5G1234M1
PDGM1_posterior = liklihood(M1pmaxs)*120/PthetaGDM1
print("Loading...")

M2Posterior = generatePosteriorSample(model = 2, size = I, D=D)
M2pmaxs = pltPosterior(M2Posterior,"M2Posterior")
P1M2 = np.mean([trunc_Beta_pdf(M2pmaxs[0], y1+1, n1-y1+1, M2Posterior[1][i], 1) for i in range(I)])
P2G1M2 = np.mean([trunc_Beta_pdf(M2pmaxs[1], y2+1, n2-y2+1, M2Posterior[2][i], M2pmaxs[0]) for i in range(I)])
P3G12M2 = np.mean([trunc_Beta_pdf(M2pmaxs[2], y3+1, n3-y3+1, M2Posterior[3][i], M2pmaxs[1]) for i in range(I)])
P4G123M2 = np.mean([trunc_Beta_pdf(M2pmaxs[3], y4+1, n4-y4+1, M2Posterior[4][i], M2pmaxs[2]) for i in range(I)])
P5G1234M2 = trunc_Beta_pdf(M2pmaxs[4], y5+1, n5-y5+1, 0, M2pmaxs[3])
PthetaGDM2 = P1M2 * P2G1M2 * P3G12M2 * P4G123M2 * P5G1234M2
PthetaGDM2, P1M2, P2G1M2 , P3G12M2 , P4G123M2 , P5G1234M2
PDGM2_posterior = liklihood(M2pmaxs)*120/PthetaGDM2
print("Loading...")

M3Posterior = generatePosteriorSample(model = 3, size = I, D=D)
M3pmaxs = pltPosterior(M3Posterior,"M3Posterior")
P1M3 = np.mean([trunc_Beta_pdf(M3pmaxs[0], y1+1, n1-y1+1, 0, M3Posterior[1][i]) for i in range(I)])
P2G1M3 = np.mean([trunc_Beta_pdf(M3pmaxs[1], y2+1, n2-y2+1, M3pmaxs[0], M3Posterior[2][i]) for i in range(I)])
P3G12M3 = np.mean([trunc_Beta_pdf(M3pmaxs[2], y3+1, n3-y3+1, max(M3pmaxs[1],M3Posterior[3][i]), 1) for i in range(I)])
P4G123M3 = np.mean([trunc_Beta_pdf(M3pmaxs[3], y4+1, n4-y4+1, M3Posterior[4][i], M3pmaxs[2]) for i in range(I)])
P5G1234M3 = trunc_Beta_pdf(M3pmaxs[4], y5+1, n5-y5+1, 0, M3pmaxs[3])
PthetaGDM3 = P1M3 * P2G1M3 * P3G12M3 * P4G123M3 * P5G1234M3
PthetaGDM3,P1M3, P2G1M3 , P3G12M3 , P4G123M3 , P5G1234M3
PDGM3_posterior = liklihood(M3pmaxs)*20/PthetaGDM3
print("Loading...")



p1, p2, p3, p4, p5 = sympy.symbols('p(1:6)')
integrand = math.comb(n1,y1) * (p1 ** y1) * (1-p1) ** (n1-y1) * math.comb(n2,y2) * (p2 ** y2) * (1-p2) ** (n2-y2) * \
    math.comb(n3,y3) * (p3 ** y3) * (1-p3) ** (n3-y3) * math.comb(n4,y4) * (p4 ** y4) * (1-p4) ** (n4-y4) * \
        math.comb(n5,y5) * (p5 ** y5) * (1-p5) ** (n5-y5)
integrandp1 = sympy.integrate(integrand, (p1,0,p2))
integrandp12 = sympy.integrate(integrandp1, (p2,0,p3))
integrandp123 = sympy.integrate(integrandp12, (p3,0,p4))
integrandp1234 = sympy.integrate(integrandp123, (p4,0,p5))
integrandp12345 = sympy.integrate(integrandp1234, (p5,0,1))
PDGM1_real = integrandp12345.evalf() * 120
print("Loading...")

integrandp1 = sympy.integrate(integrand, (p1,p2,1))
integrandp12 = sympy.integrate(integrandp1, (p2,p3,1))
integrandp123 = sympy.integrate(integrandp12, (p3,p4,1))
integrandp1234 = sympy.integrate(integrandp123, (p4,p5,1))
integrandp12345 = sympy.integrate(integrandp1234, (p5,0,1))
PDGM2_real = integrandp12345.evalf() * 120
print("Loading...")

integrandp1 = sympy.integrate(integrand, (p1,0,p2))
integrandp12 = sympy.integrate(integrandp1, (p2,0,p3))
integrandp123 = sympy.integrate(integrandp12, (p3,p4,1))
integrandp1234 = sympy.integrate(integrandp123, (p4,p5,1))
integrandp12345 = sympy.integrate(integrandp1234, (p5,0,1))
PDGM3_real = integrandp12345.evalf() * 20
print("Loading...")

PM1GD_priorBySequential = PDGM1_priorBySequential/(PDGM1_priorBySequential+PDGM2_priorBySequential+PDGM3_priorBySequential)
PM2GD_priorBySequential = PDGM2_priorBySequential/(PDGM1_priorBySequential+PDGM2_priorBySequential+PDGM3_priorBySequential)
PM3GD_priorBySequential = PDGM3_priorBySequential/(PDGM1_priorBySequential+PDGM2_priorBySequential+PDGM3_priorBySequential)

PM1GD_priorByReorder = PDGM1_priorByReorder/(PDGM1_priorByReorder+PDGM2_priorByReorder+PDGM3_priorByReorder)
PM2GD_priorByReorder = PDGM2_priorByReorder/(PDGM1_priorByReorder+PDGM2_priorByReorder+PDGM3_priorByReorder)
PM3GD_priorByReorder = PDGM3_priorByReorder/(PDGM1_priorByReorder+PDGM2_priorByReorder+PDGM3_priorByReorder)

PM1GD_priorByGibbs = PDGM1_priorByGibbs/(PDGM1_priorByGibbs+PDGM2_priorByGibbs+PDGM3_priorByGibbs)
PM2GD_priorByGibbs = PDGM2_priorByGibbs/(PDGM1_priorByGibbs+PDGM2_priorByGibbs+PDGM3_priorByGibbs)
PM3GD_priorByGibbs = PDGM3_priorByGibbs/(PDGM1_priorByGibbs+PDGM2_priorByGibbs+PDGM3_priorByGibbs)

PM1GD_posterior = PDGM1_posterior/(PDGM1_posterior+PDGM2_posterior+PDGM3_posterior)
PM2GD_posterior = PDGM2_posterior/(PDGM1_posterior+PDGM2_posterior+PDGM3_posterior)
PM3GD_posterior = PDGM3_posterior/(PDGM1_posterior+PDGM2_posterior+PDGM3_posterior)

PM1GD_real = PDGM1_real/(PDGM1_real+PDGM2_real+PDGM3_real)
PM2GD_real = PDGM2_real/(PDGM1_real+PDGM2_real+PDGM3_real)
PM3GD_real = PDGM3_real/(PDGM1_real+PDGM2_real+PDGM3_real)

print("P(D|M1) using")
print("prior samples generated by:")
print("    - Sequential: ", PDGM1_priorBySequential, "Take Log: ", math.log(PDGM1_priorBySequential))
print("    - Reorder: ", PDGM1_priorByReorder, "Take Log: ", math.log(PDGM1_priorByReorder))
print("    - Gibbs: ", PDGM1_priorByGibbs, "Take Log: ", math.log(PDGM1_priorByGibbs))
print("posterior samples generated by Gibbs: ", PDGM1_posterior, "Take Log: ", math.log(PDGM1_posterior))
print("Real value calculated by Sympy.integrate(): ", PDGM1_real, "Take Log: ", math.log(PDGM1_real))
print(" ")
print("P(D|M2) using")
print("prior samples generated by:")
print("    - Sequential: ", PDGM2_priorBySequential, "Take Log: ", math.log(PDGM2_priorBySequential))
print("    - Reorder: ", PDGM2_priorByReorder, "Take Log: ", math.log(PDGM2_priorByReorder))
print("    - Gibbs: ", PDGM2_priorByGibbs, "Take Log: ", math.log(PDGM2_priorByGibbs))
print("posterior samples generated by Gibbs: ", PDGM2_posterior, "Take Log: ", math.log(PDGM2_posterior))
print("Real value calculated by Sympy.integrate(): ", PDGM2_real, "Take Log: ", math.log(PDGM2_real))
print(" ")
print("P(D|M3) using")
print("prior samples generated by:")
print("    - Sequential: ", PDGM3_priorBySequential, "Take Log: ", math.log(PDGM3_priorBySequential))
print("    - Reorder: ", PDGM3_priorByReorder, "Take Log: ", math.log(PDGM3_priorByReorder))
print("    - Gibbs: ", PDGM3_priorByGibbs, "Take Log: ", math.log(PDGM3_priorByGibbs))
print("posterior samples generated by Gibbs: ", PDGM3_posterior, "Take Log: ", math.log(PDGM3_posterior))
print("Real value calculated by Sympy.integrate(): ", PDGM3_real, "Take Log: ", math.log(PDGM3_real))
print(" ")
print("Model Posterior Probability for ")
print("prior samples generated by:")
print(f"    - Sequential: P(M1|D)={PM1GD_priorBySequential}, P(M2|D)={PM2GD_priorBySequential}, P(M3|D)={PM3GD_priorBySequential}")
print(f"    - Reorder: P(M1|D)={PM1GD_priorByReorder}, P(M2|D)={PM2GD_priorByReorder}, P(M3|D)={PM3GD_priorByReorder}")
print(f"    - Gibbs: P(M1|D)={PM1GD_priorByGibbs}, P(M2|D)={PM2GD_priorByGibbs}, P(M3|D)={PM3GD_priorByGibbs}")
print(f"posterior samples generated by Gibbs: P(M1|D)={PM1GD_posterior}, P(M2|D)={PM2GD_posterior}, P(M3|D)={PM3GD_posterior}")
print(f"Real value calculated by Sympy.integrate(): P(M1|D)={PM1GD_real}, P(M2|D)={PM2GD_real}, P(M3|D)={PM3GD_real}")