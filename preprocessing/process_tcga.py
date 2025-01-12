import os
import argparse
import pandas as pd
from utils import wsi_to_tiles

parser = argparse.ArgumentParser(description='Process TCGA')

parser.add_argument('--followup_path', default='./clinical_follow_up_v1.0_lusc.xlsx', type=str)
parser.add_argument('--wsi_path', default='../TCGA_WSI', type=str)
parser.add_argument('--refer_img', default='./colorstandard.png', type=str)
parser.add_argument('--s', default=0.9, type=float, help='The proportion of tissues')


args = parser.parse_args()

followupTable = pd.read_excel(args.followup_path, skiprows=[1,2], engine='openpyxl')
followupTable = followupTable.loc[followupTable['new_tumor_event_dx_indicator'].isin({'YES', 'NO'})]
followupTable['recurrence'] = ((followupTable['new_tumor_event_dx_indicator'] == 'YES') &
                    (followupTable['new_tumor_event_type'] != 'New Primary Tumor'))
followupTable = followupTable.sort_values(['bcr_patient_barcode', 'form_completion_date']).drop_duplicates('bcr_patient_barcode', keep='last')
LUSC_patientids = set(followupTable['bcr_patient_barcode'])


wsi_list = os.popen("find {} -name '*.svs'".format(wsi_path)).read().strip('\n').split('\n')
wsi_list_LUSC = []
for idx in range(len(wsi_list)):
    slide_id = wsi_list[idx].rsplit('/', 1)[1].split('.')[0]
    patient_id = '-'.join(slide_id.split('-', 3)[:3])
    tile_path = os.path.join('./tiles', slide_id)
    if patient_id in LUSC_patientids:
        if not os.path.exists(tile_path):
            os.mkdir(tile_path)
        wsi_list_LUSC.append(wsi_list[idx])

for idx, wsi in enumerate(wsi_list_LUSC):
    wsi_to_tiles(idx, wsi, args.refer_img, args.s)


