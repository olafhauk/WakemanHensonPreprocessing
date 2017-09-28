#!/imaging/local/software/anaconda/latest/x86_64/bin/python
"""
==========================================
Submit qsub jobs for WH analysis
allow dependencies between jobs
==========================================

OH Sep 2017
"""

import subprocess
from os import path as op

# indices of subjects to process
subjs = range(0,16)

job_list = \
[
    # {'N':   'MF_NM',                                        # job name
    #  'Py':  'WH_MF_NM',                                     # Python script
    #  'Cf':  'WH_NM_config',                                 # configuration script
    #  'Ss':  subjs,                                          # subject indices
    #  'mem': '4GB',                                         # memory for qsub process
    #  'dep': '',                                             # name of preceeding process (optional)
    #  'node': '-W x=NODESET:ONEOF:FEATURES:MAXFILTER'}       # node constraint (optional)
    #  ###
    # {'N':   'ev_MN',
    #  'Py':  'WH_evos',
    #  'Cf':  'WH_MNE_config',
    #  'Ss':  subjs,
    #  'mem': '2GB',
    #  'dep': ''},
    #  ###
    # {'N':   'ec_MN',
    #  'Py':  'WH_plot_evocurves',
    #  'Cf':  'WH_MNE_config',
    #  'Ss':  subjs,
    #  'mem': '1GB',
    #  'dep': 'ev_MN'},
    #  ###
    # {'N':   'et_MN',
    #  'Py':  'WH_plot_topos',
    #  'Cf':  'WH_MNE_config',
    #  'Ss':  subjs,
    #  'mem': '1GB',
    #  'dep': 'ev_MN'},
     ###
    # {'N':   'cv_MN',
    #  'Py':  'WH_covmat',
    #  'Cf':  'WH_MNE_config',
    #  'Ss':  subjs,
    #  'mem': '16GB',
    #  'dep': ''},
    #  ###
    # {'N':   'cp_MN',
    #  'Py':  'WH_plot_cov',
    #  'Cf':  'WH_MNE_config',
    #  'Ss':  subjs,
    #  'mem': '1GB',
    #  'dep': 'cv_MN'}
    #  ###
    {'N':   'mat',
     'Py':  'WH_ConvertToMatlab',
     'Cf':  'WH_MNE_config',
     'Ss':  subjs,
     'mem': '2GB',
     'dep': ''}
]

# directory where python scripts are
dir_py = op.join('/', 'home', 'olaf', 'MEG', 'WakemanHensonEMEG')

# directory for qsub output
dir_qsub = op.join('/', 'home', 'olaf', 'MEG', 'WakemanHensonEMEG', 'qsub_out')


# keep track of qsub Job IDs
Job_IDs = {}

for job in job_list:

    for Ss in job['Ss']:

        N = job['N']
        Py = op.join(dir_py, job['Py'])
        Cf = job['Cf']
        mem = job['mem']

        # files for qsub output
        file_out = op.join(dir_qsub, job['Py'] + '_' + Cf + '-%d.out' % Ss)
        file_err = op.join(dir_qsub, job['Py'] + '_' + Cf + '-%d.err' % Ss)

        # if job dependent of previous job, get Job ID and produce command
        if 'dep' in job: # if dependency on previous job specified            
            if job['dep']=='':
                dep_str = ''
            else:
                job_id = Job_IDs[dep, str(Ss)]
                dep_str = '-W depend=afterok:%s' % (job_id)
        else:
            dep_str = ''

        if 'node' in job: # if node constraint present (e.g. Maxfilter)
            node_str = job['node']
        else:
            node_str = ''


        qsub_cmd = 'qsub /home/olaf/MEG/WakemanHensonEMEG/wrapper_qsub_python.sh \
                        -N %s%d \
                        -l walltime=24:00,mem=%s \
                        -o %s \
                        -e %s \
                        -v pycmd="%s.py %s",subj_idx=%d \
                        %s \
                        %s' \
                        % (N, Ss, mem, file_out, file_err, Py, Cf, Ss, dep_str, node_str)

        # format string for display
        print_str = qsub_cmd.replace(' ' * 25, '  ')
        print('\n%s\n' % print_str)

        # execute qsub command
        proc = subprocess.Popen(qsub_cmd, stdout=subprocess.PIPE, shell=True)

        # get linux output
        (out, err) = proc.communicate()

        # keep track of Job IDs from qsub
        Job_IDs[N, str(Ss)] = out.split('.')[0]