"""
Author:     David Walshe
Date:       07 April 2021
"""

import pytest

from cli import cli


def test_ls(cli_runner):
    """
    :GIVEN: Nothing.
    :WHEN:  Using the 'ls' command to view the available datasets.
    :THEN:  Verify the correct output is seen in the tests.
    """
    expected = ['Datasets',
                '------------------------------------------------',
                'atlas_of_dermoscopy',
                'bcn_20000',
                'bcn_2020_challenge',
                'brisbane_isic_challenge_2020',
                'dermofit',
                'dermoscopedia_cc_by',
                'dermis',
                'dermquest',
                'ham10000',
                'isic_2020_challenge_mskcc_contribution',
                'isic_2020_vienna_part_1',
                'isic_2020_vienna_part_2',
                'jid_editorial_images_2018',
                'mclass_d',
                'mclass_nd',
                'mednode',
                'msk_1',
                'msk_2',
                'msk_3',
                'msk_4',
                'msk_5',
                'pad_ufes_20',
                'ph2',
                'sonic',
                'sydney_mia_smdc_2020_isic_challenge_contribution',
                'uda_1',
                'uda_2']

    res = cli_runner.invoke(cli, ["ls"])

    assert res.output.strip() == "\n".join(expected)
    assert res.exit_code == 0
