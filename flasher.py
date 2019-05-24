####################################################################################
# Author: João Loureiro
# Contact: joao.loureiro@altran.com or joao.loureiro-ext@continental-corporation.com
####################################################################################

import sys
import json
from collections import namedtuple

#import core.gui as gui
import core.shell as shell

########################################################

def load_config():
    config_file = open('config.json')
    config_dict = json.loads(config_file.read())

    return config_dict


def main(args):

    config_dict = load_config()

    arg = namedtuple("arg", "long short help")
    available_args = {
        "help":                 arg("--help", "-h", "print this help message"),
        #"user_interface":      arg("--user-interface",  "-i", "load the GUI"),
        "verbose":              arg("--verbose", "-v", "Print all debugging and error messages"),
        "force_dtb_load":       arg("--force_dtb_load", "-f", "Force loading the newly generated dtb file"),
        "flash_ac":             arg("--flash_ac", "-ac", "Flash the AC, including bootmanager, bootloader and application"),
        "flash_gc_bootloader":  arg("--flash_gc_bl", "-bl", "Flash the GC bootloader"),
        "flash_gc":             arg("--flash_gc", "-gc", "Flash GC with the integrity monolith"),
        "flash_ac_bringup_b1":  arg("--flash_bringup_ac", "-ab", "Flash the AC on the B1 sample with the bringup software")
    }

    if len(args) == 1:
        args.append('-gc') #if no otion is provided, use this as the default


    #Check if any args were passed at all
    if len(args) > 0:
        if available_args["help"].long in args or available_args["help"].short in args:
            print("Conti-Flahser usage instructions:")
            for name, e in available_args.items():
                print("{} or {}: {}".format(e.short, e.long, e.help))
            exit(1)

        # if available_args["user_interface"].long in args or available_args["user_interface"].short in args:
        #     gui.init(config_dict)

        if available_args["flash_ac"].long in args or available_args["flash_ac"].short in args:
            shell.flash_ac(config_dict, flash_booloader=True, flash_bootmanager=True, flash_software=True)

        elif available_args["flash_ac_bringup_b1"].long in args or available_args["flash_ac_bringup_b1"].short in args:
            shell.flash_ac(config_dict, flash_bringup=True)

        else:
            shell.connect_serial(config_dict)
            shell.send_board_to_linux()

            if available_args["flash_gc"].long in args or available_args["flash_gc"].short in args:
                print('\nFlashing integrity monolith\n')
                shell.load_binary(config_dict)

            if available_args["force_dtb_load"].long in args or available_args["force_dtb_load"].short in args:
                shell.send_dtb(config_dict)
                shell.load_dtb(config_dict)

            if available_args["flash_gc_bootloader"].long in args or available_args["flash_gc_bootloader"].short in args:
                print('\nFlashing bootloader\n')
                shell.load_bootloader(config_dict)

            print('Flashing process completed! Please reboot the target manually.')

            #Check if any of the args is not valid
            #print("Invalid argument. Use --help for help.\n")
            #exit(-1)


if __name__ == '__main__':
    main(sys.argv)
