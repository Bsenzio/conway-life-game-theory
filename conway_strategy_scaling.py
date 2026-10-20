#!/usr/bin/env python3
"""Phase 7: Strategy-space scaling on the ORIGINAL finite 5x5 Conway board.

Windows:
    py -m pip install numpy scipy matplotlib
    py conway_strategy_scaling.py
    py conway_strategy_scaling.py --samples 100 --seed 20261020

Each sampled 10-action strategy set is nested: the first 3, 5, and 10
actions are compared under identical cellular budgets and update rules.
The script writes CSV, PNG, JSON and an English scientific report.
"""
import argparse, csv, json, math, random
from pathlib import Path
from itertools import combinations
from collections import Counter
import numpy as np
from scipy.optimize import linprog
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

N=5
BUDGETS=(3,4,5,6,7)
ACTION_COUNTS=(3,5,10)
NEIGHBORS=[]
for k in range(25):
    r,c=divmod(k,5)
    NEIGHBORS.append(sum(1<<(rr*5+cc)
        for rr in range(max(0,r-1),min(5,r+2))
        for cc in range(max(0,c-1),min(5,c+2)) if (rr,cc)!=(r,c)))

def evolve(mask):
    """Generation 1 is initial; Generation 10 is after nine B3/S23 updates."""
    x=mask
    for _ in range(9):
        y=0
        for k,nb in enumerate(NEIGHBORS):
            count=(x&nb).bit_count()
            if count==3 or (count==2 and ((x>>k)&1)):
                y|=1<<k
        x=y
    return x.bit_count()

def board(mask):
    return '/'.join(''.join(str((mask>>(5*r+c))&1) for c in range(5)) for r in range(5))

def pure_ne(M):
    # Row player maximizes M, column player minimizes M.
    maxcol=M.max(axis=0)
    minrow=M.min(axis=1)
    return [(i,j) for i in range(M.shape[0]) for j in range(M.shape[1])
            if M[i,j]>=maxcol[j]-1e-8 and M[i,j]<=minrow[i]+1e-8]

def minimax(M):
    m,n=M.shape
    # max v subject to M.T p >= v
    primal=linprog(np.r_[np.zeros(m),-1.0],
        A_ub=np.column_stack((-M.T,np.ones(n))),
        b_ub=np.zeros(n),A_eq=[np.r_[np.ones(m),0.0]],b_eq=[1.0],
        bounds=[(0,None)]*m+[(None,None)],method='highs')
    dual=linprog(np.r_[np.zeros(n),1.0],
        A_ub=np.column_stack((M,-np.ones(m))),
        b_ub=np.zeros(m),A_eq=[np.r_[np.ones(n),0.0]],b_eq=[1.0],
        bounds=[(0,None)]*n+[(None,None)],method='highs')
    if not (primal.success and dual.success):
        raise RuntimeError('Minimax linear programming failed')
    p=np.maximum(primal.x[:m],0);p/=p.sum()
    q=np.maximum(dual.x[:n],0);q/=q.sum()
    gap=abs(primal.x[-1]-dual.x[-1])
    if gap>1e-6:raise RuntimeError(f'Duality gap: {gap}')
    return float(p@M@q),p,q,gap

def wilson(k,n):
    z=1.959963984540054;p=k/n;den=1+z*z/n
    mid=(p+z*z/(2*n))/den
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return mid-half,mid+half

def csvwrite(path,headers,rows):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--samples',type=int,default=100)
    ap.add_argument('--seed',type=int,default=20261020)
    ap.add_argument('--output',default='Conway_Strategy_Scaling')
    args=ap.parse_args()
    if args.samples<2:ap.error('--samples must be >= 2')
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    rng=random.Random(args.seed)
    regions={'A':[5*r+c for r in (0,1) for c in range(5)],
             'B':[5*r+c for r in (3,4) for c in range(5)]}
    pools={b:{who:[sum(1<<k for k in comb) for comb in combinations(region,b)]
             for who,region in regions.items()} for b in BUDGETS}
    cache={}
    def outcome(mask):
        if mask not in cache:cache[mask]=evolve(mask)
        return cache[mask]
    games=[];payoffs=[];strategies=[];equilibria=[];summary=[]
    for b in BUDGETS:
        for s in range(args.samples):
            # SAME nested sampled sets, compare sizes 3/5/10 as paired games.
            aa=rng.sample(pools[b]['A'],10)
            bb=rng.sample(pools[b]['B'],10)
            full=np.array([[outcome(a|z) for z in bb] for a in aa],dtype=float)
            for size in ACTION_COUNTS:
                M=full[:size,:size]
                value,p,q,gap=minimax(M)
                pure=pure_ne(M)
                uid=f'B{b}_S{s+1:04d}_K{size}'
                games.append([uid,b,s+1,size,b*2,(b*2)/25,value,
                              len(pure),int(len(pure)==0),
                              float(M.mean()),int(M.min()),int(M.max()),
                              int(np.sum(p>1e-7)),int(np.sum(q>1e-7)),gap])
                for i in range(size):
                    strategies.append([uid,'A',i+1,aa[i],board(aa[i])])
                    strategies.append([uid,'B',i+1,bb[i],board(bb[i])])
                for i in range(size):
                    for j in range(size):
                        payoffs.append([uid,b,s+1,size,i+1,j+1,int(M[i,j]),-int(M[i,j])])
                for i,j in pure:
                    equilibria.append([uid,i+1,j+1,int(M[i,j])])
                # One optimal mixed pair from LP; degeneracy means non-unique possible.
                for i,prob in enumerate(p):
                    if prob>1e-9:
                        strategies.append([uid,'A-optimal-probability',i+1,round(float(prob),10),''])
                for j,prob in enumerate(q):
                    if prob>1e-9:
                        strategies.append([uid,'B-optimal-probability',j+1,round(float(prob),10),''])
        print(f'Completed budget {b}: {args.samples*3} matrices')
    gi={name:i for i,name in enumerate(['GameID','Budget','Sample','ActionsPerPlayer',
            'InitialCells','InitialDensity','MinimaxValue','PureNECount','NoPureNE',
            'MeanOutcome','MinOutcome','MaxOutcome','ASupport','BSupport','DualityGap'])}
    for b in BUDGETS:
        for k in ACTION_COUNTS:
            subset=[r for r in games if r[1]==b and r[3]==k]
            vals=np.array([r[6] for r in subset],float)
            no=sum(r[8] for r in subset)
            lo,hi=wilson(no,len(subset))
            summary.append([b,k,len(subset),no,no/len(subset),lo,hi,
                            float(vals.mean()),float(vals.std(ddof=1)),
                            float(np.median(vals)),float(vals.min()),float(vals.max()),
                            float(np.mean([r[7] for r in subset])),
                            float(np.mean([r[12] for r in subset])),
                            float(np.mean([r[13] for r in subset]))])
    sh=['Budget','ActionsPerPlayer','SampledGames','NoPureGames','NoPureRate',
        'Wilson95Low','Wilson95High','MeanMinimax','SDMinimax','MedianMinimax',
        'MinMinimax','MaxMinimax','MeanPureNECount','MeanASupport','MeanBSupport']
    gh=list(gi)
    csvwrite(out/'summary.csv',sh,summary)
    csvwrite(out/'games.csv',gh,games)
    csvwrite(out/'payoffs.csv',['GameID','Budget','Sample','ActionsPerPlayer',
        'AAction','BAction','PayoffA','PayoffB'],payoffs)
    csvwrite(out/'strategies.csv',['GameID','Player','ActionIndex','MaskOrProbability','Grid'],strategies)
    csvwrite(out/'pure_equilibria.csv',['GameID','AAction','BAction','LiveCells'],equilibria)
    paired=[]
    lookup={(r[1],r[2],r[3]):r for r in games}
    for b in BUDGETS:
        for s in range(1,args.samples+1):
            r3,r5,r10=[lookup[b,s,k] for k in ACTION_COUNTS]
            paired.append([b,s,r3[6],r5[6],r10[6],
                           r5[6]-r3[6],r10[6]-r5[6],r10[6]-r3[6],
                           r3[8],r5[8],r10[8],
                           int(len({r3[8],r5[8],r10[8]})>1)])
    ph=['Budget','Sample','Value3','Value5','Value10','Delta5Minus3',
        'Delta10Minus5','Delta10Minus3','NoPure3','NoPure5','NoPure10',
        'PureExistenceChanged']
    csvwrite(out/'paired_comparisons.csv',ph,paired)
    for metric,filename,title,ylabel in [
        (4,'01_no_pure_equilibrium_rates.png','Games without pure Nash equilibria','Proportion of sampled games'),
        (7,'02_minimax_value_by_action_count.png','Mean minimax value vs action count','Expected final live cells'),
        (12,'03_mean_pure_equilibria.png','Mean number of pure equilibria','Pure equilibria per sampled game')]:
        fig,ax=plt.subplots(figsize=(9,5.5))
        for b in BUDGETS:
            rows=[r for r in summary if r[0]==b]
            ax.plot(ACTION_COUNTS,[r[metric] for r in rows],marker='o',label=f'{b} cells/player')
        ax.set_xticks(ACTION_COUNTS);ax.set(xlabel='Actions per player',ylabel=ylabel,title=title)
        if metric==4:ax.set_ylim(0,1)
        ax.legend(ncol=2);ax.grid(alpha=.25);fig.tight_layout()
        fig.savefig(out/filename,dpi=220);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5.5))
    labels=[];data=[]
    for b in BUDGETS:
        for k in ACTION_COUNTS:
            labels.append(f'{b}/{k}')
            data.append([r[6] for r in games if r[1]==b and r[3]==k])
    ax.boxplot(data,tick_labels=labels,showfliers=False)
    ax.set(xlabel='Cell budget / actions per player',ylabel='Minimax value',
           title='Distribution of minimax values across nested action sets')
    ax.tick_params(axis='x',rotation=60);ax.grid(axis='y',alpha=.25)
    fig.tight_layout();fig.savefig(out/'04_minimax_boxplots.png',dpi=220);plt.close(fig)
    metadata={
        'experiment':'Phase 7 - Strategy-space scaling on fixed 5x5 Conway',
        'seed':args.seed,'samples_per_budget':args.samples,
        'budgets':BUDGETS,'action_counts':ACTION_COUNTS,
        'generation_convention':'G1 initial, G10 after 9 B3/S23 updates',
        'placement':'A top two rows, B bottom two rows, middle row initially empty',
        'sampling':'uniform distinct combinations without replacement within each sampled 10-action set',
        'nesting':'3 and 5 action games are upper-left subgames of sampled 10x10 matrix',
        'payoffs':'A=N10, B=-N10','unique_joint_masks_cached':len(cache),
        'total_games':len(games),'total_payoff_entries':len(payoffs),
        'independence':'Sets sampled independently within budget; 3/5/10 comparisons are paired',
        'scope':'Restricted sampled strategy games, not unrestricted full-board game'}
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    lines=['# Phase 7 — Strategy-Space Scaling in a Fixed 5×5 Cellular Automaton','',
        '## Abstract','',
        f'This study evaluates {len(games):,} finite zero-sum games and {len(payoffs):,} '
        'deterministic strategy pairings on an unchanged 5×5 Conway B3/S23 board. '
        'The number of available actions per player is varied (3, 5, 10), '
        'while the cell budget is controlled (3–7 cells/player). '
        'Strategy sets are nested within each independently sampled 10-action set.',
        '', '## Methods','',
        '- The board is 5×5 with dead exterior boundaries.',
        '- Generation 1 is the initial configuration; Generation 10 follows nine synchronous updates.',
        '- Player A seeds the top two rows and maximizes the final live-cell count.',
        '- Player B seeds the bottom two rows and minimizes that same count.',
        '- Each player selects distinct fixed-cardinality seed patterns.',
        '- For each budget and sample, one 10×10 matrix is drawn; its upper-left 3×3 and 5×5 subgames are evaluated.',
        '- Minimax equilibria are solved with primal and dual linear programs (SciPy HiGHS).',
        '- Pure equilibria are matrix entries that are simultaneously a column maximum and row minimum.',
        '- Wilson 95% intervals describe the proportion of sampled games lacking pure equilibria.',
        '', '## Results','',
        '| Cells/player | Actions/player | No pure NE | No pure NE (%) | Mean minimax | Mean pure NE |',
        '|---:|---:|---:|---:|---:|---:|']
    for r in summary:
        lines.append(f'| {r[0]} | {r[1]} | {r[3]}/{r[2]} | {100*r[4]:.1f} | {r[7]:.3f} | {r[12]:.3f} |')
    lines+=['','## Paired strategy-space comparisons','']
    for b in BUDGETS:
        rows=[r for r in paired if r[0]==b]
        d=np.array([r[7] for r in rows])
        change=sum(r[11] for r in rows)
        lines.append(f'- Budget {b}: mean V(10)−V(3) = {d.mean():+.3f} live cells; '
                     f'{change}/{len(rows)} sets changed pure-equilibrium existence between at least two action counts.')
    lines+=['','## Interpretation and limitations','',
        'An increase in the number of available actions changes the restricted game itself; '
        'there is no general monotonicity guarantee for the zero-sum value when both players gain actions.',
        'The absence of a pure equilibrium does not imply the absence of Nash equilibria: '
        'every finite game has a mixed equilibrium.',
        'The strategy sets are sampled from restricted non-overlapping 10-cell player regions. '
        'These observations do not establish equilibria or universal thresholds for the unrestricted 5×5 automaton.',
        'The sampled game sets are independent within each budget, but the 3/5/10-action outcomes '
        'from the same set are paired and should not be treated as independent.',
        'This experiment tests strategy-space scaling, not the effect of changing the board size.',
        '','## Reproducibility','',
        f'Seed: `{args.seed}`. Independent sets per budget: `{args.samples}`.',
        'Reproduce with `py conway_strategy_scaling.py --samples '
        f'{args.samples} --seed {args.seed}`.',
        'All seed patterns, payoff entries, and representative optimal mixed-strategy '
        'probabilities are exported as CSV.']
    (out/'scientific_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (out/'README.txt').write_text(
        'PHASE 7 — FIXED 5x5 BOARD, STRATEGY MATRICES 3x3 / 5x5 / 10x10\n\n'
        'Windows:\n  py -m pip install numpy scipy matplotlib\n'
        '  py conway_strategy_scaling.py\n\n'
        'Outputs: CSV tables, figures, metadata, and English scientific report.\n'
        'A separate Excel workbook is included in the supplied ZIP package.\n'
        'The standalone script deliberately needs no special spreadsheet library.\n',encoding='utf-8')
    print(f'SUCCESS: {len(games)} games, {len(payoffs)} payoff entries, {len(cache)} distinct initial boards')
    print('BUDGET  ACTIONS  NO_PURE  MEAN_VALUE')
    for r in summary:
        print(f'{r[0]:>6} {r[1]:>8} {r[4]:>8.1%} {r[7]:>11.3f}')
    print('Output:',out.resolve())

if __name__=='__main__':main()
