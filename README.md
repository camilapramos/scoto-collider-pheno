# (Some) Phenomenology of the Scotogenic Model at the LHC

M. Boukidi, C. Ramos, and R. Ruiz

This repository was created to organize scripts used to obtain some results for the project 'Precise QCD Predictions for the Scotogenic Model at Colliders'. The idea is to create a simple pipeline for reproducibility purposes.

Events were generated using **MadGraph5_aMC@NLO** (MG5). The relevant files are then copied and renamed for convenience, and python scripts are used to obtain a summary of the inert scalar production cross-section at the LHC at 14 and 100 TeV (with NLO accuracy for some processes), as well as branching ratios of the decay of the Z involving the BSM neutrinos in the final state.

---

### Scripts

| Script                    | Purpose                                                                               |
| ------------------------- | ------------------------------------------------------------------------------------- |
| [`organize_xsec_files.py`](./organize_xsec_files.py)  | Collects the relevant MadGraph cross-section scan files into [data_files/data_xsec/](./data_files/data_xsec/). |
| [`organize_decay_files.py`](./organize_decay_files.py) | Collects the relevant MadGraph decay scan files into [data_files/data_decay/](./data_files/data_decay/).        |
| [`make_xsec_table.py`](./make_xsec_table.py)      | Reads the organized cross-section scans and generates the LaTeX cross-section table.  |
| [`make_br_plots.py`](./make_br_plots.py)        | Reads the organized decay scans and generates the branching-ratio figures.            |

The [mg5_scripts/](./mg5_scripts/) directory contains the MG5 scripts used to generate the relevant processes.

The user should specify, on the scripts for organization, the path where the MG5 events are stored.


---

# 0. Generate processes with MG5 (optional)

This step is optional, the organized files can be found in [`data_files`](./data_files/).

Download the model UFO files, then run on your MG5 directory:
```text
./bin/mg5_aMC run_mg5amc_ScotoLHC14_MultiProc.dat
./bin/mg5_aMC run_mg5amc_ScotoLHC100_MultiProc.dat
./bin/mg5_aMC run_mg5amc_ScotoLHC_decayZ_inv.dat
./bin/mg5_aMC run_mg5amc_ScotoLHC_decayZ_taus.dat
```


## Organizing the cross-section files

The script [`organize_xsec_files.py`](./organize_xsec_files.py) copies the relevant scan summary files from the MadGraph process directories into [data_files/data_xsec/](./data_files/data_xsec/).

The processes currently included for production of inert scalars are associated production with a weak boson V ($\eta \eta V$), charged-current Drell-Yan (CCDY), neutral-current Drell-Yan (NCDY), gluon fusion (GF), and photon fusion (AF)

The organized files follow the naming convention:

```text
mg5amc_ScotoScan_<process>_<order>_LHC<energy>.txt
```

For example:

```text
mg5amc_ScotoScan_DY_EtaEtaV_NLO_LHC14.txt
mg5amc_ScotoScan_DY_EtaEtaV_NLO_LHC100.txt
```

Before running the script, **modify the eventsFoldersPath to were events are stored.**

Then run:

```bash
./organize_xsec_files.py
```

The resulting files should appear in [data_files/data_xsec/](./data_files/data_xsec/).

## Organizing the decay files

In analogy to the previous script, [`organize_decay_files.py`](./organize_decay_files.py) collects the decay scan results from the corresponding process directories. The resulting files should appear in [data_files/data_decay](./data_files/data_decay/).

---

# 1. Generating the cross-section table

The script [`make_xsec_table.py`](./make_xsec_table.py) reads the organized cross-section files from [data_files/data_xsec/](./data_files/data_xsec/) and generates [xsec_table/xsec_table.tex](./xsec_table/xsec_table.tex)

The table contains the cross sections at $\sqrt{s} = 14$ TeV, and $\sqrt{s} = 100$ TeV with LO and NLO accuracy with the QCD K-factor (for some processes). The table also includes scale uncertainties and PDF uncertainties. The command to run the script is

```bash
./make_xsec_table.py
```

The script will also print a summary of the results, which can be suppressed with the --no-summary flag

---

# 2. Generating the branching ratio plots

The script [`make_br_plots.py`](./make_br_plots.py) reads the files in [data_files/data_decay/](./data_files/data_decay/) and generates the branching ratio plots for $Z \to \tau^{+} \tau^{-} N_{1} N_{1}$ and $Z \to \nu_{\tau} \overline{\nu_{\tau}} N_{1} N_{1}$. The command to run the script is

```bash
./make_br_plots.py
```

The generated figures are saved in [br_plots/](./br_plots/). If other scalar masses are generated, these can be displayed by changing the list `m_eta_vals`in the script.
