#!/usr/bin/env python3

# C. Ramos
# 2026 September
#
# Purpose:
# Generate the cross-section table for the ScotoLHC analysis
# from the organized MadGraph5_aMC@NLO scan files.
#
# The input files are expected in:
#     data_files/data_xsec/
#
# The output table is written to:
#     xsec_table/xsec_table.tex


import os
import argparse
from pathlib import Path
import pandas as pd


REPO_PATH = Path(__file__).resolve().parent
DATA_PATH = REPO_PATH / 'data_files' / 'data_xsec'
OUTPUT_PATH = REPO_PATH / 'xsec_table' / 'xsec_table.tex'

LHC_e = ['14', '100']
meta = 'mass#9900035'


processes = {
    'DY': {'type': 'NLO', 'path': 'mg5amc_ScotoScan_DY_EtaEtaV', 'label': r'$\eta\eta V$'},
    'CCDY': {'type': 'NLO', 'path': 'mg5amc_ScotoScan_CCDY_H0HX', 'label': 'CCDY'},
    'NCDY': {'type': 'NLO', 'path': 'mg5amc_ScotoScan_NCDY_EtaEta', 'label': 'NCDY'},
    'GF': {'type': 'XLO', 'path': 'mg5amc_ScotoScan_GGF_EtaEta', 'label': 'GF'},
    'AF': {'type': 'XLO', 'path': 'mg5amc_ScotoScan_AAF_HpHm', 'label': 'AF'}
}


def read_results(path, energy, process_type):

    """Read organized MadGraph scan results for a given process and energy."""

    process_dir = DATA_PATH

    if process_type == 'NLO':

        file_lo = process_dir / f'{path}_XLO_LHC{energy}.txt'
        file_nlo = process_dir / f'{path}_NLO_LHC{energy}.txt'

        if not file_lo.exists():
            raise FileNotFoundError(f'LO file not found: {file_lo}')

        if not file_nlo.exists():
            raise FileNotFoundError(f'NLO file not found: {file_nlo}')

        lo = pd.read_csv(file_lo, sep=r'\s+')
        nlo = pd.read_csv(file_nlo, sep=r'\s+')

        return {'LO': lo, 'NLO': nlo}

    elif process_type == 'XLO':
        file_xlo = process_dir / f'{path}_XLO_LHC{energy}.txt'

        if not file_xlo.exists():
            raise FileNotFoundError(f'XLO file not found: {file_xlo}')

        xlo = pd.read_csv(file_xlo, sep=r'\s+')

        return {'XLO': xlo}

    else:
        raise ValueError(f'Unknown process type: {process_type}')


def load_all_results():

    """Load scan results for all processes and collider energies."""

    results = {}

    for name, info in processes.items():
        results[name] = {}

        for energy in LHC_e:
            results[name][energy] = read_results(info['path'],energy,info['type'])

    return results


def sci_latex(x, digits=2):

    """Format a number in scientific notation for LaTeX."""

    coefficient, exponent = f'{x:.{digits}e}'.split('e')
    exponent = int(exponent)

    return rf'{{{coefficient} \cdot 10^{{{exponent}}}}}'


def format_xsec(df):

    """Format a cross section and its scale/PDF uncertainties."""

    cross_fb = df['cross'].iloc[0] * 1000 # mg5 values are in pb; the table is in fb.

    return (
        f'${sci_latex(cross_fb)}'
        f'^{{+{df["scale_hi_percent"].iloc[0]:.1f}\\%}}'
        f'_{{{df["scale_lo_percent"].iloc[0]:.1f}\\%}}'
        f'\\ ^{{+{df["pdf_hi_percent"].iloc[0]:.1f}\\%}}'
        f'_{{{df["pdf_lo_percent"].iloc[0]:.1f}\\%}}$'
    )


def get_xsec(df, mass, tolerance=1.0):

    """Return the scan point closest to the requested mass."""

    if df.empty:
        return df

    differences = (df[meta] - mass).abs()
    idx = differences.idxmin()

    if differences.loc[idx] > tolerance:
        return df.iloc[0:0]

    return df.loc[[idx]]


def format_process_row(process, mass, results):

    """Build the LaTeX table entries for one process and one mass."""

    info = processes[process]
    data_14 = results[process]['14']
    data_100 = results[process]['100']

    if info['type'] == 'NLO':

        LO_14 = get_xsec(data_14['LO'], mass)
        NLO_14 = get_xsec(data_14['NLO'], mass)
        LO_100 = get_xsec(data_100['LO'], mass)
        NLO_100 = get_xsec(data_100['NLO'], mass)

        # Check that all required data exist.

        if LO_14.empty:
            print(
                f'WARNING: Missing 14 TeV LO data '
                f'for {process}, mass = {mass}'
            )

        if NLO_14.empty:
            print(
                f'WARNING: Missing 14 TeV NLO data '
                f'for {process}, mass = {mass}'
            )

        if LO_100.empty:
            print(
                f'WARNING: Missing 100 TeV LO data '
                f'for {process}, mass = {mass}'
            )

        if NLO_100.empty:

            print(
                f'WARNING: Missing 100 TeV NLO data '
                f'for {process}, mass = {mass}'
            )

        if (LO_14.empty or NLO_14.empty or LO_100.empty or NLO_100.empty):
            return None

        k_14 = (NLO_14['cross'].iloc[0] / LO_14['cross'].iloc[0])
        k_100 = (NLO_100['cross'].iloc[0] / LO_100['cross'].iloc[0])

        return (
            f'{format_xsec(LO_14)} & '
            f'{format_xsec(NLO_14)} & '
            f'${k_14:.2f}$ & '
            f'{format_xsec(LO_100)} & '
            f'{format_xsec(NLO_100)} & '
            f'${k_100:.2f}$'
        )

    elif info['type'] == 'XLO':

        XLO_14 = get_xsec(data_14['XLO'], mass)
        XLO_100 = get_xsec(data_100['XLO'], mass)

        if XLO_14.empty:
            print(
                f'WARNING: Missing 14 TeV XLO data '
                f'for {process}, mass = {mass}'
            )

        if XLO_100.empty:
            print(
                f'WARNING: Missing 100 TeV XLO data '
                f'for {process}, mass = {mass}'
            )

        if XLO_14.empty or XLO_100.empty:
            return None

        return (
            f'{format_xsec(XLO_14)} & '
            r' &  & '
            f'{format_xsec(XLO_100)} & '
            r' & '
        )

    else:
        raise ValueError(f'Unknown process type: {info["type"]}')


def get_central_xsec(df, mass, tolerance=1.0):

    """Return the central cross section in fb for the closest mass point."""

    data = get_xsec(df, mass, tolerance)

    if data.empty:
        return None

    return data['cross'].iloc[0] * 1000


def print_summary(results, masses):
    """Print a compact cross-section summary to the terminal."""

    print()
    print('Cross-section summary')
    print('=====================')

    for mass in masses:

        print()
        print(f'm = {mass:.0f} GeV')

        for process, info in processes.items():
            if info['type'] == 'NLO':
                xsec_14 = get_central_xsec(results[process]['14']['NLO'],mass)
                xsec_100 = get_central_xsec(results[process]['100']['NLO'],mass)

            elif info['type'] == 'XLO':
                xsec_14 = get_central_xsec(results[process]['14']['XLO'],mass)
                xsec_100 = get_central_xsec(results[process]['100']['XLO'],mass)

            else:
                raise ValueError(f'Unknown process type: {info["type"]}')
            
            if xsec_14 is None or xsec_100 is None:
                print(f'  {process.replace("DY", "eta eta V"):<10} missing data')

            else:
                print(
                    f'  {process.replace("DY", "eta eta V"):<10} '
                    f'14 TeV: {xsec_14:.3e} fb    '
                    f'100 TeV: {xsec_100:.3e} fb'
                )
    print()
    print(f'More details on file: {OUTPUT_PATH}')


def make_table(results, masses):

    """Write the LaTeX cross-section table."""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, 'w') as f:
        f.write(
            r'\begin{table*}[t!]' '\n'
            r'\begin{center}' '\n'
            r'\resizebox{\textwidth}{!}{' '\n'
            r'\begin{tabular}{c | c | r r c || r r c}' '\n'
            r'\hline\hline' '\n'
            r'\multicolumn{2}{c}{} & '
            r'\multicolumn{3}{c}{$\sqrt{s} = 14\TeV$ LHC} & '
            r'\multicolumn{3}{c}{$\sqrt{s} = 100\TeV$ LHC}'
            '\n' r'\\' '\n'
            r'mass [GeV] & Process & '
            r'$\sigma^{\rm LO}$ [fb] & '
            r'$\sigma^{\rm NLO}$ [fb] & $K$ & '
            r'$\sigma^{\rm LO}$ [fb] & '
            r'$\sigma^{\rm NLO}$ [fb] & $K$'
            '\n' r'\\' '\n'
            r'\hline\hline' '\n'
        )

        for mass in masses:

            for i, (process, info) in enumerate(processes.items()):
                row = format_process_row(process, mass, results)

                if row is None:
                    continue

                if i == 0:
                    mass_cell = (
                        rf'\multirow{{{len(processes)}}}{{*}}'
                        rf'{{${mass:.0f}$}}'
                    )

                else:
                    mass_cell = ''

                f.write(
                    f'{mass_cell} & {info["label"]} & {row} \\\\\n'
                )

            f.write(r'\hline' '\n')

        f.write(
            r'\hline' '\n'
            r'\end{tabular}' '\n'
            r'} \end{center}' '\n'
            r'\end{table*}'
        )

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate the ScotoLHC cross-section table.')
    
    parser.add_argument(
        '--no-summary', action='store_true', help='Do not print the cross-section summary to the terminal.'
    )

    return parser.parse_args()

def main():

    args = parse_arguments()
    print('Loading MadGraph scan results...')
    results = load_all_results()

    # Use the DY 14 TeV LO scan as the reference mass grid.
    reference_df = results['DY']['14']['LO']
    masses = sorted(reference_df[meta].unique())

    print(f'Found {len(masses)} mass points.')
    make_table(results, masses)
    if not args.no_summary:
        print_summary(results, masses)

    print('Have a nice day!')


if __name__ == '__main__':
    main()