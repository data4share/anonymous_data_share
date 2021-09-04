import os
import pickle
import platform

TMP_IDR = "/tmp/bat_reports"
if platform.system() == "Windows":
    LINUX_TMP_DIR = "/mnt/e" + TMP_IDR
else:
    LINUX_TMP_DIR = TMP_IDR

def is_bat_result(file_name):
    if file_name.endswith("_bat.tar"):
        return file_name.replace("_bat.tar", "")
    elif file_name.endswith("_bat.tar.gz"):
        return file_name.replace("_bat.tar.gz", "")
    elif file_name.endswith(".tar.gz"):
        return file_name.replace(".tar.gz", "")
    else:
        return None

bat_result_file = "ssldump_bat.tar"
base_name = is_bat_result(bat_result_file)

def parse_one_result(bat_result_file):
    proc = os.popen('bash -c "tar -tf %s | grep filereports.*-filereport.pickle.gz"' % bat_result_file)
    report_gz_name = proc.read().strip()
    proc.close
    if not report_gz_name:
        print("Wrong !")
    bat_result_report_gz = "/".join([LINUX_TMP_DIR, report_gz_name])
    bat_result_report_pkl = "/".join([TMP_IDR, report_gz_name.replace(".gz", "")])
    os.system('bash -c "tar -zxvf {bat_tar} -C {linux_tmp_dir} {report_gz_name} && gzip -d -f {filereport_tar}"'.format(
                bat_tar=bat_result_file, linux_tmp_dir = LINUX_TMP_DIR, report_gz_name=report_gz_name, filereport_tar=bat_result_report_gz))
    fr = open(bat_result_report_pkl, 'rb')
    data = pickle.load(fr)
    ranking_detail = data['ranking'][0]
    brief_report = {}
    for report in ranking_detail['reports']:
        brief_report[report['rank']] = (report['package'], report['percentage'])
    return brief_report

def parse_avaliable_results():
    report_file = "report.pkl"
    if os.path.exists(report_file):
        with open(report_file, 'rb') as fr:
            report_collection = pickle.load(fr)
    else:
        report_collection = {}
    for bat_result_file in os.listdir("."):
        base_name = is_bat_result(bat_result_file)
        if base_name:
            brief_report = parse_one_result(bat_result_file)
            report_collection[base_name] = brief_report
    with open(report_file, 'wb') as fw:
        pickle.dump(report_collection, fw)
    return report_collection

def refine_report_collection(report_collection):
    report_file = "fine_report.pkl"
    if os.path.exists(report_file):
        with open(report_file, 'rb') as fr:
            fine_report_collection = pickle.load(fr)
    else:
        fine_report_collection = {}
    # main
    for pkg_and_bin in report_collection.keys():
        if "---" not in pkg_and_bin:
            print("%s seems no need to re-fine" % pkg_and_bin)
            return -1
        pkg_name, bin_name = pkg_and_bin.split("---")
        if pkg_name not in fine_report_collection:
            fine_report_collection[pkg_name] = {}
        fine_report_collection[pkg_name][bin_name] = report_collection[pkg_and_bin]
    # save
    with open(report_file, 'wb') as fw:
        pickle.dump(fine_report_collection, fw)
    return fine_report_collection

if __name__ == "__main__":
    rc = parse_avaliable_results()
    frc = refine_report_collection(rc)
    print("All is done.")

