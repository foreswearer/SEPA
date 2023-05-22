import os


# list of parameters from que query
def extract_parameter_list_from_files(all_dir: str):
    # the list to be filled
    p_list = []

    # loop all the files to get parameters
    for filename in sorted(os.listdir(all_dir)):
        f = os.path.join(all_dir, filename)

        # we are assuming useful files if they are bigger than 1k
        if os.path.isfile(f) and os.path.getsize(f) > 1000:
            p = get_parameter(f)
            if p not in p_list:
                p_list.append(p)

    return p_list


def get_parameter(filename: str):
    filename = filename.replace('../', '')
    return filename.split('.')[0].split('_')[-1]


def get_station_name(filename: str):
    filename = filename.replace('../', '')
    return ' '.join(filename.split('.')[0].split('_')[:-3]).split('/')[-1]
