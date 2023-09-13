import plumed
import matplotlib.pyplot as plt
import pandas as pd
import os


def cv_timeseries(files, out_dir):
    '''
    Make plots of collective variable timeseries.

    Parameters
    ----------
    files : list
        List of pahs to input files.
    out_dir : str
        Output directory.
    '''
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    dfs = []
    ylims = {}
    cv_names = []

    for f in files:
        df = plumed.read_as_pandas(f)
        dfs.append(df)

    df_all = pd.concat(dfs)

    cv_names = [x for x in df_all.columns]
    cv_names.remove('time')

    for x in cv_names:
        if not os.path.exists(os.path.join(out_dir, x)):
            os.mkdir(os.path.join(out_dir, x))
    
    for x in cv_names:
        ylims[x] = (df_all[x].min(), df_all[x].max())
    
    del df_all

    for i, df in enumerate(dfs):

        for x in cv_names:
            if not os.path.exists(os.path.join(out_dir, x)):
                os.mkdir(os.path.join(out_dir, x))
        
            fig, ax = plt.subplots()
            ax.plot(df['time'], df[x])
            ax.set_ylim(ylims[x][0], ylims[x][1])
            ax.set_xlabel('Time [ps]')
            ax.set_ylabel(x)
            plt.savefig(os.path.join(out_dir, x, f'sim{i}.png'), dpi=150)
            plt.close()
    

def cv_scatter(files, cv1, cv2, out_dir):
    '''
    Make scatter plots of pairs of collective variables.

    Parameters
    ----------
    files : list
        List of paths to collective variable files.
    cv1 : str
        Name of CV 1.
    cv2 : str
        Name of CV 2.
    out_dir : str
        Output directory.
    '''
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    for i, f in enumerate(files):
        df = plumed.read_as_pandas(f)

        fig, ax = plt.subplots()
        ax.scatter(df[cv1], df[cv2], color='k', alpha=0.5)
        ax.set_xlabel(cv1)
        ax.set_ylabel(cv2)
        plt.savefig(os.path.join(out_dir, f'{cv1}-{cv2}-sim{i}.png'), dpi=150)
        plt.close()
