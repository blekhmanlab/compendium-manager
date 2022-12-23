import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import projects.parsing

@pytest.fixture
def fastq_dir_paired():
    """Creates a mock fastq/ directory with files in it, which we can
    test are being deleted as expected."""
    # Make a fastq directory
    subprocess.run(
        ['mkdir', 'tests/fastq'],
        stdout=subprocess.PIPE, text=True
    )
    # create forward and reverse fastq files for each sample
    with open('tests/SraAccList.txt', 'r') as f:
        for sample in f.readlines():
            for ext in [1,2]:
                subprocess.run(
                    ['touch', f'tests/fastq/{sample[:-1]}_{ext}.fastq'],
                    stdout=subprocess.PIPE, text=True
                )
    yield True
    # cleanup
    subprocess.run(
        ['rm', '-rf', 'tests/fastq'],
        stdout=subprocess.PIPE, text=True
    )

def test_load_summary():
    samples = projects.parsing.load_summary('tests')
    assert len(samples) == 6

def test_Process_summary():
    proj = projects.parsing.Process_summary('tests')
    assert len(proj.samples) == 6

def test_Project_Rerun_as_single_end(fastq_dir_paired):
    proj = projects.parsing.Process_summary('tests')
    # make sure we're starting with paired-end files
    assert len(os.listdir('tests/fastq')) == 12

    # Get ready to re-run as single end by deleting the reverse reads
    proj.Rerun_as_single_end()

    # Make sure half the files are gone
    fastqs = os.listdir('tests/fastq')
    assert len(fastqs) == 6
    # Make sure all the files are forward reads
    for f in fastqs:
        assert f[-8:] == '_1.fastq'