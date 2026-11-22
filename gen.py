"""Contrived dataset for teaching the analysis workbench. Every effect below is
put in on purpose so that each one has a checkable right answer."""
import random, json
random.seed(20261122)
CAT=['A','B','C']; TEMPS=[40,50,60,70,80,90]; SHIFTS=['Day','Night']; REPS=16
TSLOPE={'A':0.10,'B':0.45,'C':0.25}   # yield per degree, by catalyst  -> the interaction
TBASE ={'A':8.0,'B':0.0,'C':4.0}      # yield offset at 40 C           -> lines cross near 55 C
PRESS_OPT=3.0; PRESS_K=1.8            # -K*(p-opt)^2                   -> the hidden curve
WEEK_DRIFT=0.35                       # process improvement per week   -> the clock
NOISE=2.0

order=[(c,t,s,k) for c in CAT for t in TEMPS for s in SHIFTS for k in range(REPS)]
random.shuffle(order); N=len(order)
half=[round(random.uniform(1.0,3.0),2) for _ in range(N//2)]
press=half+[round(6.0-p,2) for p in half]      # exactly symmetric about the optimum
random.shuffle(press)

rows=[]
for i,(cat,temp,shift,k) in enumerate(order):
    week=i//24+1; p=press[i]
    hum=round(35+0.50*week+random.gauss(0,2.0),1)          # tracks the calendar, causes nothing
    y=(30.0+TBASE[cat]+TSLOPE[cat]*(temp-40)
       -PRESS_K*(p-PRESS_OPT)**2+WEEK_DRIFT*week+random.gauss(0,NOISE))
    pur=99.0-0.08*(temp-40)-(1.5 if cat=='B' else 0.0)+random.gauss(0,0.5)
    rows.append(dict(run_id=i+1,week=week,shift=shift,catalyst=cat,temperature_c=temp,
        pressure_atm=p,stir_rate_rpm=int(round(random.uniform(200,800))),
        lab_humidity_pct=hum,yield_pct=round(y,2),purity_pct=round(pur,2)))
for r in rows:
    if r['week']==7: r['purity_pct']=None       # instrument down that week
json.dump(rows,open('lab.json','w'))
print('rows',len(rows))
