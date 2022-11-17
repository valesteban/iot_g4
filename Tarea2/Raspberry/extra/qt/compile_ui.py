import os
import os.path
import glob
import time
import argparse
import sys

from PyQt5.uic import compileUi

UI_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.sep.join([UI_DIR, "..","..", "gui", "forms"])


def touch_file(file_path):
    open(file_path, 'a').close()


def get_ui_files(ui_dir):
    full_path_files = glob.glob(os.path.join(ui_dir, '*.ui'))
    res = map(os.path.basename, full_path_files)
    return res


def compile_uis_from_dir(ui_dir, out_dir, should_force=False):
    try:
        #mkdir -p $ui_dir
        if not os.access(out_dir, os.F_OK):
            os.mkdir(out_dir)

        #touch $FORM_DIR/__init__.py
        touch_file(out_dir+'/__init__.py')

        #processing ui
        files = glob.glob(os.path.join(ui_dir, '*.ui'))
        for ui_file_path in files:
            ui_fname = ui_file_path.split(os.path.sep)[-1]

            ui_stats = os.stat(ui_file_path)
            ui_last_mod_time = time.localtime(ui_stats[8])

            fname_no_ext = ''.join(ui_fname.split('.')[:-1])
            out_file_path = os.path.join(out_dir, fname_no_ext + '.py')

            out_file_exists = os.path.exists(out_file_path)
            if os.path.exists(out_file_path):
                out_stats = os.stat(out_file_path)
                out_last_mod_time = time.localtime(out_stats[8])

            if should_force or (not out_file_exists) or (ui_last_mod_time > out_last_mod_time):
                print('Building {0}'.format(out_file_path))
                out_file = open(out_file_path, 'w')
                compileUi(ui_file_path, out_file, from_imports="raquis")
                out_file.close()

        #processing qrc
        files = glob.glob(ui_dir+'/*.qrc')
        for ui_file_path in files:
            ui_fname = ui_file_path.split(os.path.sep)[-1]

            ui_stats = os.stat(ui_file_path)
            ui_last_mod_time = time.localtime(ui_stats[8])

            fname_no_ext = ''.join(ui_fname.split('.')[:-1])
            out_file_path = out_dir+'/'+fname_no_ext+'_rc.py'

            #execute pyrcc4 -o resources_rc.py resources.qrc
            command = "pyrcc5 -o {0} {1}".format(out_file_path, ui_file_path)
            print(command)
            os.system(command)

        if len(files) > 0:
            print('All ({0}) ui files compiled'.format(len(files)))
        else:
            print('No ui files in located at {0}'.format(ui_dir), file=sys.stderr)

    except OSError as err:
        print(err, file=sys.stderr)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--force", action="store_true",
                        help="Force compile existing ui files")

    parser.add_argument("-i", "--ui-dir", dest="ui_dir", default=UI_DIR,
                        help="Input directory containing ui files")

    parser.add_argument("-o", "--out-dir", dest="out_dir", default=OUT_DIR,
                        help="Output directory to store compiled forms")

    parser.add_argument("-s", "--sip-version", dest="sip_version", default=2,
                        type=int, help="Specify SIP API version")

    parser.add_argument("-e", "--execute", dest="execute",
                        action='store_true', help="Make the output py file executable")

    args = parser.parse_args()

    # ni idea si esto es importante uwu
    #import sip
    #sip.setapi('QString', args.sip_version)
    #sip.setapi('QVariant', args.sip_version)
    #print('Using SIP api v{0}'.format(args.sip_version))

    compile_uis_from_dir(args.ui_dir, args.out_dir, should_force=args.force)
