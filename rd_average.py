#!/usr/bin/python3
# Copyright 2017-2018 Wyoh Knott
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import os
import sys
import glob
import numpy as np
import pandas as pd
from multiprocessing import Pool


def get_lossy_average(args):
    [path, format] = args

    if not glob.glob(path + "/" + format + "/lossy/*.out"):
        print("Lossy results files could not be found for format {}.".format(
            format))
        return

    rawdata = []
    columns = [
        "file_name", "quality", "orig_file_size", "compressed_file_size",
        "height", "frames", "pixels", "bpp", "compression_ratio", 
        "encode_time", "encode_fpm", "decode_time", "decode_fpm"
        "y_ssim_score", "rgb_ssim_score", "msssim_score", "psnrhvsm_score",
        "vmaf_score"
    ]
    final_columns = [
        "quality", "avg_bpp", "avg_compression_ratio", "avg_space_saving",
        "wavg_encode_fpm", "wavg_decode_fpm", "wavg_y_ssim_score",
        "wavg_rgb_ssim_score", "wavg_msssim_score", "wavg_psnrhvsm_score",
        "wavg_vmaf_score"
    ]

    data_path = path + "/" + format + "/lossy/"

    for f in glob.glob(data_path + "*.out"):
        rawdata.append(pd.read_csv(f, sep=":"))

    quality_length = len(rawdata[0].index)

    resolution_list = []
    for data in rawdata:
        resolution_list = resolution_list + data["height"][data.index == 1].tolist()
    resolution_list = list(set(resolution_list)) + ["any"]

    for resolution in resolution_list:
        
        merged_data = []
        final_data = pd.DataFrame(columns=final_columns)

        for i in range(quality_length):
            merged_data.insert(i, pd.DataFrame(columns=columns))

            for data in rawdata:
                if resolution == "any":
                    merged_data[i] = merged_data[i].append(data.iloc[[i]])
                else:
                    merged_data[i] = merged_data[i].append(data[(data.index == i) & (data["height"] == resolution)])

            merged_data[i].sort_values("file_name", ascending=True, inplace=True)

            quality = np.mean(merged_data[i]["quality"])
            sum_orig_file_size = np.sum(merged_data[i]["orig_file_size"])
            sum_compressed_file_size = np.sum(
                merged_data[i]["compressed_file_size"])
            sum_pixels = np.sum(merged_data[i]["pixels"])
            avg_bpp = sum_compressed_file_size * 8 / sum_pixels
            avg_compression_ratio = sum_orig_file_size / sum_compressed_file_size
            avg_space_saving = 1 - (1 / avg_compression_ratio)
            wavg_encode_fpm = np.average(
                merged_data[i]["encode_fpm"], weights=merged_data[i]["pixels"])
            wavg_decode_fpm = np.average(
                merged_data[i]["decode_fpm"], weights=merged_data[i]["pixels"])
            wavg_y_ssim_score = np.average(
                merged_data[i]["y_ssim_score"], weights=merged_data[i]["pixels"])
            wavg_rgb_ssim_score = np.average(
                merged_data[i]["rgb_ssim_score"], weights=merged_data[i]["pixels"])
            wavg_msssim_score = np.average(
                merged_data[i]["msssim_score"], weights=merged_data[i]["pixels"])
            wavg_psnrhvsm_score = np.average(
                merged_data[i]["psnrhvsm_score"], weights=merged_data[i]["pixels"])
            wavg_vmaf_score = np.average(
                merged_data[i]["vmaf_score"], weights=merged_data[i]["pixels"])

            final_data.loc[i] = [
                quality, avg_bpp, avg_compression_ratio, avg_space_saving,
                wavg_encode_fpm, wavg_decode_fpm, wavg_y_ssim_score,
                wavg_rgb_ssim_score, wavg_msssim_score, wavg_psnrhvsm_score,
                wavg_vmaf_score
            ]
                
        results_file = path + "/" + os.path.basename(
            path) + "." + format + "." + str(resolution) + ".lossy.out"
        final_data.to_csv(results_file, sep=":", index=False)
        print("Lossy results file for format {} successfully saved to {}.".format(
            format, results_file))


def main(argv):
    if sys.version_info[0] < 3 and sys.version_info[1] < 5:
        raise Exception("Python 3.5 or a more recent version is required.")

    if len(argv) < 1 or len(argv) > 2:
        print(
            "rd_average.py: Calculate a per format weighted averages of the results files generated by rd_collect.py"
        )
        print(
            "Arg 1: Path to the results of a subset generated by rd_collect.py")
        print("       For ex: rd_average.py \"results/subset1\"")
        return

    results_folder = os.path.normpath(argv[1])
    available_formats = next(os.walk(results_folder))[1]

    # Check is there is actually results files in the path provided
    if (not os.path.isdir(results_folder) or not available_formats
            or not glob.glob(results_folder + "/**/*.out", recursive=True)):
        print(
            "Could not find all results file. Please make sure the path provided is correct."
        )
        return

    Pool().map(get_lossy_average,
               [(results_folder, format)
                for format in next(os.walk(results_folder))[1]])


if __name__ == "__main__":
    main(sys.argv)
