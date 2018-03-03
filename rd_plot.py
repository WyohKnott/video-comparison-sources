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
import six
import pytablewriter
import matplotlib
matplotlib.use('Cairo')
import matplotlib.pyplot as plt


def generate_plots(path, requested_formats):

    # Get list of resolutions
    rawdata = []
    resolution_list = []
    
    data_path = path + "/" + requested_formats[0] + "/lossy/"
    
    for f in glob.glob(data_path + "*.out"):
        rawdata.append(pd.read_csv(f, sep=":"))

    for data in rawdata:
        resolution_list = resolution_list + data["height"][data.index == 1].tolist()
    resolution_list = list(set(resolution_list)) + ["any"]
    rawdata = []
    
    subset_name = os.path.basename(path)
    
    for resolution in resolution_list:
        data = {}
        
        for format in requested_formats:
            file = path + "/" + subset_name  + "." + format + "." + str(resolution) + ".lossy.out"
            data[format] = pd.read_csv(file, sep=":")

        plt.rcParams['svg.fonttype'] = 'svgfont'
        plt.rcParams['axes.axisbelow'] = True

        # Y-SSIM
        fig = plt.figure()
        plt.figure(figsize=(25, 15))
        plt.title(
            "Quality according to Y-SSIM in function of number of bits per pixel")
        plt.suptitle(subset_name + ", resolution: " + str(resolution))
        plt.xlabel("Bits per pixels")
        plt.ylabel("dB (Y-SSIM)")
        plt.xscale("log")
        plt.xlim([0.01, 0.6])
        plt.ylim([10, 20])
        plt.minorticks_on()
        plt.grid(b=True, which='both', color='0.65', linestyle='--')
        for format in data:
            plt.plot(
                data[format]["avg_bpp"],
                data[format]["wavg_y_ssim_score"],
                '+-',
                label=format)
        plt.legend()
        plt.savefig(path + "/" + subset_name + ".y-ssim." + str(resolution) +
                    ".(" + ','.join(requested_formats) + ").svg")
        plt.close(fig)

        # RGB-SSIM
        fig = plt.figure()
        plt.figure(figsize=(25, 15))
        plt.title(
            "Quality according to RGB-SSIM in function of number of bits per pixel"
        )
        plt.suptitle(subset_name + ", resolution: " + str(resolution))
        plt.xlabel("Bits per pixels")
        plt.ylabel("dB (RGB-SSIM)")
        plt.xscale("log")
        plt.xlim([0.01, 0.6])
        plt.ylim([10, 20])
        plt.minorticks_on()
        plt.grid(b=True, which='both', color='0.65', linestyle='--')
        for format in data:
            plt.plot(
                data[format]["avg_bpp"],
                data[format]["wavg_rgb_ssim_score"],
                '+-',
                label=format)
        plt.legend()
        plt.savefig(path + "/" + subset_name + ".rgb-ssim." + str(resolution) +
                    ".(" + ','.join(requested_formats) + ").svg")
        plt.close(fig)

        # MS-SSIM
        fig = plt.figure()
        plt.figure(figsize=(25, 15))
        plt.title(
            "Quality according to MS-SSIM in function of number of bits per pixel")
        plt.suptitle(subset_name + ", resolution: " + str(resolution))
        plt.xlabel("Bits per pixels")
        plt.ylabel("dB (MS-SSIM)")
        plt.xscale("log")
        plt.xlim([0.01, 0.6])
        plt.ylim([10, 30])
        plt.minorticks_on()
        plt.grid(b=True, which='both', color='0.65', linestyle='--')
        for format in data:
            plt.plot(
                data[format]["avg_bpp"],
                data[format]["wavg_msssim_score"],
                '+-',
                label=format)
        plt.legend()
        plt.savefig(path + "/" + subset_name + ".ms-ssim." + str(resolution) +
                    ".(" + ','.join(requested_formats) + ").svg")
        plt.close(fig)

        # PSNR-HVS-M
        fig = plt.figure()
        plt.figure(figsize=(25, 15))
        plt.title(
            "Quality according to PSNR-HVS-M in function of number of bits per pixel"
        )
        plt.suptitle(subset_name + ", resolution: " + str(resolution))
        plt.xlabel("Bits per pixels")
        plt.ylabel("dB (PSNR-HVS-M)")
        plt.xscale("log")
        plt.xlim([0.01, 0.6])
        plt.ylim([25, 50])
        plt.minorticks_on()
        plt.grid(b=True, which='both', color='0.65', linestyle='--')
        for format in data:
            plt.plot(
                data[format]["avg_bpp"],
                data[format]["wavg_psnrhvsm_score"],
                '+-',
                label=format)
        plt.legend()
        plt.savefig(path + "/" + subset_name + ".psnr-hvs-m." +
                    str(resolution) + ".(" + ','.join(requested_formats) +
                    ").svg")
        plt.close(fig)

        # VMAF
        fig = plt.figure()
        plt.figure(figsize=(25, 15))
        plt.title(
            "Quality according to VMAF in function of number of bits per pixel")
        plt.suptitle(subset_name + ", resolution: " + str(resolution))
        plt.xlabel("Bits per pixels")
        plt.ylabel("Score (VMAF)")
        plt.xscale("log")
        plt.xlim([0.01, 0.6])
        plt.ylim([80, 100])
        plt.minorticks_on()
        plt.grid(b=True, which='both', color='0.65', linestyle='--')
        for format in data:
            plt.plot(
                data[format]["avg_bpp"],
                data[format]["wavg_vmaf_score"],
                '+-',
                label=format)
        plt.legend()
        plt.savefig(path + "/" + subset_name + ".vmaf." + str(resolution) +
                    ".(" + ','.join(requested_formats) + ").svg")
        plt.close(fig)

        # Speed
        fig = plt.figure()
        plt.figure(figsize=(25, 15))
        plt.title("Speed in function of average bpp")
        plt.suptitle(subset_name + ", resolution: " + str(resolution))
        plt.xlabel("Bits per pixel")
        plt.ylabel("Frames per minute")
        plt.xscale("log")
        plt.xlim([0.01, 0.6])
        plt.ylim([0, 600])
        plt.minorticks_on()
        plt.grid(b=True, which='both', color='0.65', linestyle='--')
        for format in data:
            plt.plot(
                data[format]["avg_bpp"],
                data[format]["wavg_encode_fpm"],
                '+-',
                label=format)
        plt.legend()
        plt.savefig(path + "/" + subset_name + ".encoding_fpm." +
                    str(resolution) + ".(" + ','.join(requested_formats) +
                    ").svg")
        plt.close(fig)

        fig = plt.figure()
        plt.figure(figsize=(25, 15))
        plt.title("Encoding time in function of VMAF quality")
        plt.suptitle(subset_name + ", resolution: " + str(resolution))
        plt.xlabel("Score (VMAF)")
        plt.ylabel("Frames per minute")
        plt.xlim([80, 100])
        plt.ylim([0, 600])
        plt.minorticks_on()
        plt.grid(b=True, which='both', color='0.65', linestyle='--')
        for format in data:
            plt.plot(
                data[format]["wavg_vmaf_score"],
                data[format]["wavg_encode_fpm"],
                '+-',
                label=format)
        plt.legend()
        plt.savefig(path + "/" + subset_name + ".encoding_fpm_to_vmaf." +
                    str(resolution) + ".(" + ','.join(requested_formats) +
                    ").svg")
        plt.close(fig)

        fig = plt.figure()
        plt.figure(figsize=(25, 15))
        plt.title("VMAF in function of crf")
        plt.suptitle(subset_name + ", resolution: " + str(resolution))
        plt.xlabel("Quality (crf)")
        plt.ylabel("VMAF score")
        plt.xlim([10, 60])
        plt.ylim([90, 100])
        plt.minorticks_on()
        plt.grid(b=True, which='both', color='0.65', linestyle='--')
        for format in data:
            z = np.polyfit(data[format]["quality"], data[format]["wavg_vmaf_score"], 4)
            p = np.poly1d(z)
            xp = np.linspace(10, 60, 100)
            plt.plot(data[format]["quality"], data[format]["wavg_vmaf_score"], "+", xp, p(xp), "-",
                label=format)
        plt.legend()
        plt.savefig(path + "/" + subset_name + ".vmaf_to_crf." +
                    str(resolution) + ".(" + ','.join(requested_formats) +
                    ").svg")
        plt.close(fig)
        
        plt.close("all")
        
        if resolution == 1080:
            # crf conversion
            results_x264 = pd.DataFrame({"x264 crf": range(16, 25)})
            p = np.poly1d(np.polyfit(data["x264"]["quality"], data["x264"]["avg_bpp"], 4))
            results_x264["x264 bpp"] = results_x264.apply(lambda row: p(row["x264 crf"]), axis=1)
            p = np.poly1d(np.polyfit(data["x264"]["quality"], data["x264"]["wavg_y_ssim_score"], 4))
            results_x264["x264 y-ssim"] = results_x264.apply(lambda row: p(row["x264 crf"]), axis=1)
            p = np.poly1d(np.polyfit(data["x264"]["quality"], data["x264"]["wavg_rgb_ssim_score"], 4))
            results_x264["x264 rgb-ssim"] = results_x264.apply(lambda row: p(row["x264 crf"]), axis=1)
            p = np.poly1d(np.polyfit(data["x264"]["quality"], data["x264"]["wavg_msssim_score"], 4))
            results_x264["x264 ms-ssim"] = results_x264.apply(lambda row: p(row["x264 crf"]), axis=1)
            p = np.poly1d(np.polyfit(data["x264"]["quality"], data["x264"]["wavg_psnrhvsm_score"], 4))
            results_x264["x264 psnr-hvs-m"] = results_x264.apply(lambda row: p(row["x264 crf"]), axis=1)
            p = np.poly1d(np.polyfit(data["x264"]["quality"], data["x264"]["wavg_vmaf_score"], 4))
            results_x264["x264 vmaf"] = results_x264.apply(lambda row: p(row["x264 crf"]), axis=1)

            results_file = path + "/" + os.path.basename(path) + ".crf_conversion.x264.1080.lossy.out"
            results_x264.to_csv(results_file, sep=":")
            file = open(path + "/" + os.path.basename(path) + ".crf_conversion.x264.1080.lossy.md", "w")
            markdown_writer = pytablewriter.MarkdownTableWriter()
            markdown_writer.from_dataframe(results_x264)
            markdown_writer.stream = six.StringIO()
            markdown_writer.write_table()
            file.write(markdown_writer.stream.getvalue())
            file.close()
            
            # vp9 crf
            results_vp9 = pd.DataFrame({"x264 crf": range(16, 25)})
            p = np.poly1d(np.polyfit(data["x264"]["quality"], data["x264"]["avg_bpp"], 4))
            results_vp9["x264 bpp"] = results_x264.apply(lambda row: p(row["x264 crf"]), axis=1)
            p = np.poly1d(np.polyfit(data["vp9"]["wavg_y_ssim_score"], data["vp9"]["quality"], 4))
            results_vp9["vp9 crf according to y-ssim"] = results_x264.apply(lambda row: p(row["x264 y-ssim"]), axis=1)
            p = np.poly1d(np.polyfit(data["vp9"]["quality"], data["vp9"]["avg_bpp"], 4))
            results_vp9["vp9 bpp according to y-ssim"] = results_vp9.apply(lambda row: p(row["vp9 crf according to y-ssim"]), axis=1)
            results_vp9["vp9 % reduction according to y-ssim"] = results_vp9.apply(lambda row: (row["vp9 bpp according to y-ssim"] / row["x264 bpp"] -1) * 100, axis=1)
            
            p = np.poly1d(np.polyfit(data["vp9"]["wavg_rgb_ssim_score"], data["vp9"]["quality"], 4))
            results_vp9["vp9 crf according to rgb-ssim"] = results_x264.apply(lambda row: p(row["x264 rgb-ssim"]), axis=1)
            p = np.poly1d(np.polyfit(data["vp9"]["quality"], data["vp9"]["avg_bpp"], 4))
            results_vp9["vp9 bpp according to rgb-ssim"] = results_vp9.apply(lambda row: p(row["vp9 crf according to rgb-ssim"]), axis=1)
            results_vp9["vp9 % reduction according to rgb-ssim"] = results_vp9.apply(lambda row: (row["vp9 bpp according to rgb-ssim"] / row["x264 bpp"] -1) * 100, axis=1)
            
            p = np.poly1d(np.polyfit(data["vp9"]["wavg_msssim_score"], data["vp9"]["quality"], 4))
            results_vp9["vp9 crf according to ms-ssim"] = results_x264.apply(lambda row: p(row["x264 ms-ssim"]), axis=1)
            p = np.poly1d(np.polyfit(data["vp9"]["quality"], data["vp9"]["avg_bpp"], 4))
            results_vp9["vp9 bpp according to ms-ssim"] = results_vp9.apply(lambda row: p(row["vp9 crf according to ms-ssim"]), axis=1)
            results_vp9["vp9 % reduction according to ms-ssim"] = results_vp9.apply(lambda row: (row["vp9 bpp according to ms-ssim"] / row["x264 bpp"] -1) * 100, axis=1)
            
            p = np.poly1d(np.polyfit(data["vp9"]["wavg_psnrhvsm_score"], data["vp9"]["quality"], 4))
            results_vp9["vp9 crf according to psnr-hvs-m"] = results_x264.apply(lambda row: p(row["x264 psnr-hvs-m"]), axis=1)
            p = np.poly1d(np.polyfit(data["vp9"]["quality"], data["vp9"]["avg_bpp"], 4))
            results_vp9["vp9 bpp according to psnr-hvs-m"] = results_vp9.apply(lambda row: p(row["vp9 crf according to psnr-hvs-m"]), axis=1)
            results_vp9["vp9 % reduction according to psnr-hvs-m"] = results_vp9.apply(lambda row: (row["vp9 bpp according to psnr-hvs-m"] / row["x264 bpp"] -1) * 100, axis=1)
            
            p = np.poly1d(np.polyfit(data["vp9"]["wavg_vmaf_score"], data["vp9"]["quality"], 4))
            results_vp9["vp9 crf according to vmaf"] = results_x264.apply(lambda row: p(row["x264 vmaf"]), axis=1)
            p = np.poly1d(np.polyfit(data["vp9"]["quality"], data["vp9"]["avg_bpp"], 4))
            results_vp9["vp9 bpp according to vmaf"] = results_vp9.apply(lambda row: p(row["vp9 crf according to vmaf"]), axis=1)
            results_vp9["vp9 % reduction according to vmaf"] = results_vp9.apply(lambda row: (row["vp9 bpp according to vmaf"] / row["x264 bpp"] -1) * 100, axis=1)

            results_file = path + "/" + os.path.basename(path) + ".crf_conversion.vp9.1080.lossy.out"
            results_vp9.to_csv(results_file, sep=":")
            file = open(path + "/" + os.path.basename(path) + ".crf_conversion.vp9.1080.lossy.md", "w")
            markdown_writer = pytablewriter.MarkdownTableWriter()
            markdown_writer.from_dataframe(results_vp9)
            markdown_writer.stream = six.StringIO()
            markdown_writer.write_table()
            file.write(markdown_writer.stream.getvalue())
            file.close()
            
            # x265 crf
            results_x265 = pd.DataFrame({"x264 crf": range(16, 25)})
            p = np.poly1d(np.polyfit(data["x264"]["quality"], data["x264"]["avg_bpp"], 4))
            results_x265["x264 bpp"] = results_x264.apply(lambda row: p(row["x264 crf"]), axis=1)
            p = np.poly1d(np.polyfit(data["x265"]["wavg_y_ssim_score"], data["x265"]["quality"], 4))
            results_x265["x265 crf according to y-ssim"] = results_x264.apply(lambda row: p(row["x264 y-ssim"]), axis=1)
            p = np.poly1d(np.polyfit(data["x265"]["quality"], data["x265"]["avg_bpp"], 4))
            results_x265["x265 bpp according to y-ssim"] = results_x265.apply(lambda row: p(row["x265 crf according to y-ssim"]), axis=1)
            results_x265["x265 % reduction according to y-ssim"] = results_x265.apply(lambda row: (row["x265 bpp according to y-ssim"] / row["x264 bpp"] -1) * 100, axis=1)
            
            p = np.poly1d(np.polyfit(data["x265"]["wavg_rgb_ssim_score"], data["x265"]["quality"], 4))
            results_x265["x265 crf according to rgb-ssim"] = results_x264.apply(lambda row: p(row["x264 rgb-ssim"]), axis=1)
            p = np.poly1d(np.polyfit(data["x265"]["quality"], data["x265"]["avg_bpp"], 4))
            results_x265["x265 bpp according to rgb-ssim"] = results_x265.apply(lambda row: p(row["x265 crf according to rgb-ssim"]), axis=1)
            results_x265["x265 % reduction according to rgb-ssim"] = results_x265.apply(lambda row: (row["x265 bpp according to rgb-ssim"] / row["x264 bpp"] -1) * 100, axis=1)
            
            p = np.poly1d(np.polyfit(data["x265"]["wavg_msssim_score"], data["x265"]["quality"], 4))
            results_x265["x265 crf according to ms-ssim"] = results_x264.apply(lambda row: p(row["x264 ms-ssim"]), axis=1)
            p = np.poly1d(np.polyfit(data["x265"]["quality"], data["x265"]["avg_bpp"], 4))
            results_x265["x265 bpp according to ms-ssim"] = results_x265.apply(lambda row: p(row["x265 crf according to ms-ssim"]), axis=1)
            results_x265["x265 % reduction according to ms-ssim"] = results_x265.apply(lambda row: (row["x265 bpp according to ms-ssim"] / row["x264 bpp"] -1) * 100, axis=1)
            
            p = np.poly1d(np.polyfit(data["x265"]["wavg_psnrhvsm_score"], data["x265"]["quality"], 4))
            results_x265["x265 crf according to psnr-hvs-m"] = results_x264.apply(lambda row: p(row["x264 psnr-hvs-m"]), axis=1)
            p = np.poly1d(np.polyfit(data["x265"]["quality"], data["x265"]["avg_bpp"], 4))
            results_x265["x265 bpp according to psnr-hvs-m"] = results_x265.apply(lambda row: p(row["x265 crf according to psnr-hvs-m"]), axis=1)
            results_x265["x265 % reduction according to psnr-hvs-m"] = results_x265.apply(lambda row: (row["x265 bpp according to psnr-hvs-m"] / row["x264 bpp"] -1) * 100, axis=1)
            
            p = np.poly1d(np.polyfit(data["x265"]["wavg_vmaf_score"], data["x265"]["quality"], 4))
            results_x265["x265 crf according to vmaf"] = results_x264.apply(lambda row: p(row["x264 vmaf"]), axis=1)
            p = np.poly1d(np.polyfit(data["x265"]["quality"], data["x265"]["avg_bpp"], 4))
            results_x265["x265 bpp according to vmaf"] = results_x265.apply(lambda row: p(row["x265 crf according to vmaf"]), axis=1)
            results_x265["x265 % reduction according to vmaf"] = results_x265.apply(lambda row: (row["x265 bpp according to vmaf"] / row["x264 bpp"] -1) * 100, axis=1)

            results_file = path + "/" + os.path.basename(path) + ".crf_conversion.x265.1080.lossy.out"
            results_x265.to_csv(results_file, sep=":")
            file = open(path + "/" + os.path.basename(path) + ".crf_conversion.x265.1080.lossy.md", "w")
            markdown_writer = pytablewriter.MarkdownTableWriter()
            markdown_writer.from_dataframe(results_x265)
            markdown_writer.stream = six.StringIO()
            markdown_writer.write_table()
            file.write(markdown_writer.stream.getvalue())
            file.close()


def main(argv):
    if sys.version_info[0] < 3 and sys.version_info[1] < 5:
        raise Exception("Python 3.5 or a more recent version is required.")

    if len(argv) < 2 or len(argv) > 3:
        print(
            "Arg 1: Path to a subset with results generated by rd_average.py")
        print("       For ex: rd_average.py \"results/subset1\"")
        print("Arg 2: Comma-separated list of format to plot.")
        print(
            "       For ex: rd_average.py \"results/subset1\" \"av1,vp9,x264,x265\""
        )

    results_folder = os.path.normpath(argv[1])

    if (not os.path.isdir(results_folder)
            or not glob.glob(results_folder + "/*.lossy.out")):
        print(
            "Could not find all results file. Please make sure the path provided is correct."
        )
        return

    available_formats = []
    for f in glob.glob(results_folder + "/*.lossy.out"):
        available_formats.append(os.path.basename(f).split(".")[1])

    try:
        requested_formats = [format.strip() for format in argv[2].split(",")]
    except IndexError:
        requested_formats = available_formats

    for format in requested_formats:
        if format not in available_formats:
            print("The format {} is not in the list of available formats {}".
                  format(format, available_formats))
            return

    generate_plots(results_folder, requested_formats)


if __name__ == "__main__":
    main(sys.argv)
