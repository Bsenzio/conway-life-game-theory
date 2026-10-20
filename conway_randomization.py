#!/usr/bin/env python3
"""Phase 8: paired payoff-permutation baseline for Conway 5x5 seeding games.
Usage: py conway_phase8_randomization.py --input-dir Conway_Strategy_Scaling --output-dir Conway_Phase8 --permutations 200 --seed 20261020
Dependencies: numpy, scipy, matplotlib. Reads phase 7 payoffs.csv and games.csv.
"""
import argparse, csv, json, math
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.stats import binomtest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read_csv(p):
    with open(p, newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def write_csv(p, rows, fields):
    with open(p,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def saddle(a):
    # A maximizes rows, B minimizes columns.
    return bool(np.any((a == a.max(axis=0)[None,:]) & (a == a.min(axis=1)[:,None])))
def value(a):
    m,n=a.shape
    res=linprog(np.r_[np.zeros(m),-1.],A_ub=np.c_[-a.T,np.ones(n)],b_ub=np.zeros(n),A_eq=np.c_[np.ones((1,m)),np.zeros((1,1))],b_eq=[1.],bounds=[(0,None)]*m+[(None,None)],method='highs')
    if not res.success: raise RuntimeError(res.message)
    return float(res.x[-1])
def wilson(k,n,z=1.959963984540054):
    p=k/n; d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/d
    return c-h,c+h

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input-dir',default='Conway_Strategy_Scaling');ap.add_argument('--output-dir',default='Conway_Phase8');ap.add_argument('--permutations',type=int,default=200);ap.add_argument('--value-permutations',type=int,default=12);ap.add_argument('--seed',type=int,default=20261020)
    args=ap.parse_args();src=Path(args.input_dir);out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    if args.permutations<2 or args.value_permutations<0 or args.value_permutations>args.permutations:raise ValueError('Invalid permutation counts')
    pay=defaultdict(list)
    for r in read_csv(src/'payoffs.csv'):
        pay[r['GameID']].append((int(r['AAction']),int(r['BAction']),float(r['PayoffA'])))
    games=read_csv(src/'games.csv');rng=np.random.default_rng(args.seed)
    details=[]; bygroup=defaultdict(list); n_checked=0
    for idx,g in enumerate(games):
        gid=g['GameID']; k=int(g['ActionsPerPlayer']); budget=int(g['Budget']); mat=np.full((k,k),np.nan)
        for i,j,v in pay[gid]:mat[i-1,j-1]=v
        if np.isnan(mat).any():raise ValueError(f'Missing payoffs in {gid}')
        observed_no=int(not saddle(mat)); claimed=int(g['NoPureNE'])
        if observed_no!=claimed:raise ValueError(f'Phase 7 pure equilibrium mismatch: {gid}')
        vals=mat.ravel(); shuffled_no=0; control_values=[]
        for rep in range(args.permutations):
            perm=rng.permutation(vals).reshape(k,k)
            shuffled_no+=int(not saddle(perm))
            if rep<args.value_permutations:control_values.append(value(perm))
        p=shuffled_no/args.permutations
        orig_val=float(g['MinimaxValue'])
        if idx<5 and abs(value(mat)-orig_val)>1e-6:raise ValueError(f'Phase 7 minimax mismatch {gid}')
        rec={'GameID':gid,'Budget':budget,'ActionsPerPlayer':k,'ObservedNoPure':observed_no,'Permutations':args.permutations,'PermutedNoPureCount':shuffled_no,'PermutedNoPureRate':p,'DifferenceObservedMinusControl':observed_no-p,'OriginalMinimax':orig_val,'MeanPermutedMinimax':float(np.mean(control_values)) if control_values else '', 'DifferenceMinimax':orig_val-float(np.mean(control_values)) if control_values else '', 'ValuePermutations':args.value_permutations}
        details.append(rec);bygroup[(budget,k)].append(rec);n_checked+=1
    write_csv(out/'game_level_results.csv',details,list(details[0]))
    summaries=[]
    for (budget,k),rows in sorted(bygroup.items()):
        n=len(rows);observed=sum(r['ObservedNoPure'] for r in rows);perm_count=sum(r['PermutedNoPureCount'] for r in rows);perm_n=n*args.permutations
        obs_rate=observed/n;control_rate=perm_count/perm_n
        d=np.array([r['DifferenceObservedMinusControl'] for r in rows]);
        # Paired game-level bootstrap, not treating within-game permutations as independent.
        bootrng=np.random.default_rng(args.seed+budget*100+k)
        boot=np.mean(d[bootrng.integers(0,n,size=(4000,n))],axis=1)
        lo,hi=np.quantile(boot,[.025,.975]);
        # Monte Carlo randomization test for the sum of pure-NE indicators:
        # conditional on each game's fixed payoff multiset, the permutation null
        # makes the observed arrangement exchangeable with independent shuffled arrangements.
        # Sample Bernoulli(p_i) indicators (approximation using MC p_i estimates).
        pi=np.array([r['PermutedNoPureRate'] for r in rows]);nullrng=np.random.default_rng(args.seed+budget*200+k)
        sims=np.zeros(30000,dtype=np.int16)
        for prob in pi:sims+=(nullrng.random(30000)<prob)
        expected=float(pi.sum());pval=(1+np.count_nonzero(abs(sims-expected)>=abs(observed-expected)-1e-12))/(len(sims)+1)
        valdiff=[r['DifferenceMinimax'] for r in rows if r['DifferenceMinimax']!='']
        summaries.append({'Budget':budget,'ActionsPerPlayer':k,'Games':n,'ObservedNoPureCount':observed,'ObservedNoPureRate':obs_rate,'ControlNoPureRate':control_rate,'DifferenceObservedMinusControl':obs_rate-control_rate,'PairedBootstrap95Low':lo,'PairedBootstrap95High':hi,'PermutationNullTwoSidedPApprox':pval,'MeanOriginalMinimax':float(np.mean([r['OriginalMinimax'] for r in rows])),'MeanControlMinimax':float(np.mean([r['MeanPermutedMinimax'] for r in rows])) if valdiff else '', 'MeanMinimaxDifference':float(np.mean(valdiff)) if valdiff else ''})
    write_csv(out/'summary_by_budget_and_actions.csv',summaries,list(summaries[0]))
    fig,axs=plt.subplots(1,3,figsize=(15,4.6),sharey=True)
    for ax,k in zip(axs,[3,5,10]):
        rows=[r for r in summaries if r['ActionsPerPlayer']==k];b=[r['Budget'] for r in rows];ax.plot(b,[100*r['ObservedNoPureRate'] for r in rows],marker='o',label='Conway');ax.plot(b,[100*r['ControlNoPureRate'] for r in rows],marker='s',label='Shuffled payoffs');ax.set_title(f'{k} × {k} strategies');ax.set_xlabel('Cells per player');ax.set_xticks(b);ax.grid(alpha=.25)
    axs[0].set_ylabel('Games without pure Nash equilibrium (%)');axs[-1].legend();fig.suptitle('Conway payoff structure vs within-matrix permutation control');fig.tight_layout();fig.savefig(out/'01_pure_equilibrium_comparison.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5));
    for k in [3,5,10]:
        rows=[r for r in summaries if r['ActionsPerPlayer']==k];ax.errorbar([r['Budget']+(k-5)*.035 for r in rows],[100*r['DifferenceObservedMinusControl'] for r in rows],yerr=[[100*(r['DifferenceObservedMinusControl']-r['PairedBootstrap95Low']) for r in rows],[100*(r['PairedBootstrap95High']-r['DifferenceObservedMinusControl']) for r in rows]],marker='o',capsize=3,label=f'{k}×{k}')
    ax.axhline(0,color='black',linewidth=1);ax.set_xlabel('Cells per player');ax.set_ylabel('Conway minus shuffled (percentage points)');ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(out/'02_paired_differences.png',dpi=170);plt.close(fig)
    with open(out/'metadata.json','w') as f:json.dump({'seed':args.seed,'permutations_per_game':args.permutations,'minimax_permutations_per_game':args.value_permutations,'games':n_checked,'total_payoff_entries':sum(int(g['ActionsPerPlayer'])**2 for g in games),'null':'Within each original matrix, independently permute all payoff entries, preserving exact multiset including ties','statistics':'Game-level paired bootstrap CI; approximate conditional permutation-null Monte Carlo p-value based on estimated per-game null probabilities','caution':'Matrix entries are dependent; nested 3/5/10 games are not independent; p-values are exploratory and unadjusted for 15 comparisons.'},f,indent=2)
    lines=['# Phase 8 — Structural equilibrium analysis against payoff-permutation baselines','',f'Input: Phase 7; {n_checked} sampled games, {args.permutations} permutations/game ({n_checked*args.permutations:,} shuffled matrices).','', 'Each permutation preserves the exact payoff multiset of its original matrix, including all ties, but destroys its row/column strategic arrangement. The 5×5 Conway board and B3/S23 rules are unchanged.','', '## Results','', '| Cells/player | Strategies | Conway no-pure % | Shuffled no-pure % | Difference (pp) | Paired bootstrap 95% CI (pp) | Exploratory p |','|---:|---:|---:|---:|---:|---:|---:|']
    for r in summaries:lines.append(f"| {r['Budget']} | {r['ActionsPerPlayer']}×{r['ActionsPerPlayer']} | {100*r['ObservedNoPureRate']:.1f} | {100*r['ControlNoPureRate']:.1f} | {100*r['DifferenceObservedMinusControl']:+.1f} | [{100*r['PairedBootstrap95Low']:+.1f}, {100*r['PairedBootstrap95High']:+.1f}] | {r['PermutationNullTwoSidedPApprox']:.4f} |")
    lines+=['','## Interpretation','', 'A difference from this baseline establishes nonrandom strategic arrangement relative to uniform within-matrix permutations; it does **not** uniquely identify Conway dynamics as the cause, because spatially restricted seeding and shared-action correlations also shape the matrix.','', 'The permutation null treats each matrix payoff multiset as fixed. The per-game control rate is estimated by Monte Carlo. The paired confidence interval resamples games (not individual permutations). Exploratory p-values approximate a conditional null using Monte Carlo-estimated game-specific Bernoulli probabilities and are not corrected for multiple comparisons.','', 'Minimax control values are computed on a smaller subset of permutations per game; they are descriptive, not formal tests.','', 'Strategy sets of sizes 3, 5, and 10 are nested within the same 10-action samples, so comparisons across sizes are correlated. No claims of universal behavior or hardware execution of these randomized controls are made.','', '## Reproducibility','', '`py -m pip install numpy scipy matplotlib`','', '`py conway_phase8_randomization.py --input-dir Conway_Strategy_Scaling --output-dir Conway_Phase8 --permutations 200 --value-permutations 12 --seed 20261020`','']
    (out/'scientific_report.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Completed:',n_checked,'games;',n_checked*args.permutations,'shuffled matrices')
    for r in summaries:print(r['Budget'],r['ActionsPerPlayer'],f"original={r['ObservedNoPureRate']:.2f}",f"control={r['ControlNoPureRate']:.3f}",f"delta={r['DifferenceObservedMinusControl']:+.3f}")
if __name__=='__main__':main()
