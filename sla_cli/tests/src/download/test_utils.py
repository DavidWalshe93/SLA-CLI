"""
Author:     David Walshe
Date:       11 April 2021
"""

import os
import pytest

import httpretty
from httpretty import register_uri

import sla_cli.src.download.utils as sut


@httpretty.activate
@pytest.mark.parametrize("url",
                         [
                             "https://www.dropbox.com/s/k88qukc20ljnbuo/PH2Dataset.rar?dl=1",
                             "https://uwaterloo.ca/vision-image-processing-lab/sites/ca.vision-image-processing-lab/files/uploads/files/skin_image_data_set-1.zip",
                             "https://uwaterloo.ca/vision-image-processing-lab/sites/ca.vision-image-processing-lab/files/uploads/files/skin_image_data_set-2.zip",
                             "http://www.cs.rug.nl/~imaging/databases/melanoma_naevi/complete_mednode_dataset.zip",
                             "https://md-datasets-cache-zipfiles-prod.s3.eu-west-1.amazonaws.com/zr7vgbcyr2-1.zip",
                             "https://skinclass.de/MClass/MClass-D.zip",
                             "https://skinclass.de/MClass/MClass-ND",
                             "https://isic-archive.com/api/v1",
                         ])
def test_download_file(url, tmpdir):
    """
    :GIVEN: A url endpoint for an online resource.
    :WHEN:  Downloading a dataset from the given url.
    :THEN:  Verify the download method behaves as expected.
    """
    register_uri(
        httpretty.GET,
        uri=url,
        body=f"From {url}"
    )

    with tmpdir.as_cwd():
        dst_path = os.path.join(os.getcwd(), "test_file.zip")
        assert os.path.exists(dst_path) == False

        sut.download_file(url, dst_path, 10)

        assert os.path.exists(dst_path) == True

        with open(dst_path) as fh:
            assert fh.read() == f"From {url}"
