#!/usr/bin/env python3
# C. Ramos
# 2026 September 
# # Purpose: 
# Generate the branching-ratio figures for the ScotoLHC analysis 
# from the organized MadGraph5_aMC@NLO decay scan files. 
# # The input files are expected in: 
# data_files/decay_data/ 
# # The output figures are written to: 
# br_plots/ 

from pathlib import Path 
import pandas as pd 
import matplotlib.pyplot as plt 
import mplhep as mh 
from mplhep.styles.lhcb import LHCb2 as styleGuide 
import seaborn as sns 

REPO_PATH = Path(__file__).resolve().parent 
DATA_PATH = REPO_PATH / 'data_files' / 'data_decay' 
OUTPUT_PATH = REPO_PATH / 'br_plots' 

Z_width = 2.4955 
m_eta_vals = [250, 500, 1000] 
ls_list = ['solid', 'dashdot', ':', 'solid'] 
addtxt = ( r'$|Y_{\ell N_{1}}|=\delta_{\tau \ell}$' '\n' r'$m_{N_{2}} = m_{N_{3}} = 10^{10}$ GeV' ) 

def read_decay_data(filename): 
    """Read an organized MadGraph decay scan file.""" 

    filepath = DATA_PATH / filename 
    if not filepath.exists(): 
        raise FileNotFoundError( f'Decay scan file not found: {filepath}' ) 
    return pd.read_csv(filepath, sep=r'\s+') 

def get_mass_label(mass): 
    """Return the LaTeX label for the charged scalar mass.""" 

    if mass > 999: 
        return r'$m_{\eta^{\pm}} = %1.0f$ TeV' % (mass / 1e3) 
    else: 
        return r'$m_{\eta^{\pm}} = %1.0f$ GeV' % mass 

def make_br_plot( scan_df, ylabel, output_file ): 
    """Generate and save a branching-ratio plot.""" 

    mh.style.use("LHCb2") 

    fig, ax = plt.subplots(figsize=(9, 8)) 
    for i, mass in enumerate(m_eta_vals): 
        df_m = scan_df[ scan_df["mass#9900035"] == mass ] 
        mass_label = get_mass_label(mass) 
        ax.plot(df_m["mass#9900012"], df_m["cross"] / Z_width,label=mass_label,ls=ls_list[i]) 

    ax.set_yscale('log') 
    ax.legend(frameon=True) 
    ax.text(0.6,0.85,addtxt,bbox=dict(facecolor='white',edgecolor='black'),transform=ax.transAxes,fontsize=20) 
    ax.set_xlabel(r'$m_{N_{1}}$ [GeV]', loc='right') 
    ax.set_ylabel(ylabel, loc='top') 
    ax.tick_params(direction="in") 
    ax.grid(alpha=0.3) 
    fig.tight_layout() 

    filepath = OUTPUT_PATH / output_file 
    fig.savefig(filepath) 
    print(f'Figure written to: {filepath}') 

def main(): 
    print('Loading decay scan results...') 

    scan_df_c = read_decay_data('mg5amc_ScotoScan_decayZtoTauTauN1N1.txt') 
    scan_df_n = read_decay_data('mg5amc_ScotoScan_decayZtoNutNutbarN1N1.txt') 

    OUTPUT_PATH.mkdir( parents=True, exist_ok=True ) 
    make_br_plot(scan_df_c,r'BR$(Z \to \tau^{+} \tau^{-} N_{1} N_{1})$','BRZtautauN1N1.pdf') 
    make_br_plot(scan_df_n,r'BR$(Z \to \nu_{\tau} \overline{\nu_{\tau}} N_{1} N_{1})$','BRZnunuBarN1N1.pdf') 

    print() 
    print('have a nice day!') 

if __name__ == '__main__': main()