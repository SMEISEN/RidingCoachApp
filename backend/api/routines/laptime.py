import ezodf
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from datetime import datetime


def read_laptimesheet(spreadsheet):

    doc = ezodf.opendoc(spreadsheet)

    sheet_sectors = doc.sheets[0]
    sheet_channels = doc.sheets[2]
    channels_dict = {}
    channels_col_index = {}
    sectors_dict = {}
    sectors_col_index = {}
    session_start_str = 'undefined'
    session_start_dt = None
    location_str = 'undefined'
    application_str = 'undefined'

    for i, (row_sectors, row_channels) in enumerate(
        zip(sheet_sectors.rows(), sheet_channels.rows())):

        if i == 2:
            location_str = row_sectors[1].value
            continue
        if i == 4:
            application_str = row_sectors[1].value
            continue
        if i == 6:
            sectors_dict = {cell.value: [] for m, cell in enumerate(row_sectors) if m >= 3}
            sectors_col_index = {n: cell.value for n, cell in enumerate(row_sectors) if n >= 3}
            channels_dict = {cell.value: [] for k, cell in enumerate(row_channels) if k <= 3}
            channels_col_index = {l: cell.value for l, cell in enumerate(row_channels) if l <= 3}
            continue
        if i == 10:
            session_start_str = row_sectors[1].value
            session_start_dt = datetime.strptime(session_start_str, '%d/%m/%Y %H:%M')
        if i < 11:
            continue
        for j, (cell_channels, cell_sectors) in enumerate(zip(row_channels, row_sectors)):
            if j <= 3:
                cell_value = cell_channels.value
                if j == 0:
                    cell_value = int(cell_value)
                elif j == 1:
                    if ':' in cell_value:
                        cell_value = cell_value.replace(',', '.')
                        cell_value = (datetime.strptime(cell_value, '%M:%S.%f') -
                                        datetime.strptime('00:00.0', '%M:%S.%f')).total_seconds()
                    else:
                        cell_value = float(cell_value.replace(',', '.'))
                elif j == 2:
                    if ':' in cell_value:
                        cell_value = cell_value.replace(',', '.').replace('+', '')
                        cell_value = (datetime.strptime(cell_value, '%M:%S.%f') -
                                        datetime.strptime('00:00.0', '%M:%S.%f')).total_seconds()
                    else:
                        cell_value = cell_value.replace(',', '.').replace('+', '')
                        cell_value = (datetime.strptime(cell_value, '%S.%f') -
                                        datetime.strptime('00.0', '%S.%f')).total_seconds()
                elif j == 3:
                    cell_value = datetime\
                        .strptime(f"{session_start_str[0:10]} {cell_value}", '%d/%m/%Y %H:%M')
                else:
                    cell_value = cell_channels.value
                channels_dict[channels_col_index[j]].append(cell_value)
            if j >= 3:
                cell_value = cell_sectors.value
                if not cell_value.strip():
                    cell_value = float(0)
                else:
                    if ':' in cell_value:
                        cell_value = cell_value.replace(',', '.')
                        cell_value = (datetime.strptime(cell_value, '%M:%S.%f') -
                                        datetime.strptime('00:00.0', '%M:%S.%f')).total_seconds()
                    else:
                        cell_value = cell_value.replace(',', '.')
                        cell_value = (datetime.strptime(cell_value, '%S.%f') -
                                        datetime.strptime('00.0', '%S.%f')).total_seconds()
                sectors_dict[sectors_col_index[j]].append(cell_value)
    lap_numbers = channels_dict.get('Lap')
    laptime_seconds = channels_dict.get('Full')
    datetimes_display = channels_dict.get('Start')

    sector_seconds = [x for x in sectors_dict.values()]
    sector_names = [x for x in sectors_dict.keys()]
    data = [
        laptime_seconds,
        datetimes_display,
        [None for x in range(len(laptime_seconds))],
        [None for x in range(len(laptime_seconds))],
        [None for x in range(len(laptime_seconds))]
        ] + sector_seconds
    columns = [
        'laptime_seconds',
        'datetime_display',
        'offroad',
        'valid',
        'track_layout'] + sector_names

    laptime_data = pd.DataFrame(np.transpose(np.array(data)), index=lap_numbers, columns=columns)

    return session_start_dt, location_str, application_str, laptime_data


def validate_laptimes(laptime_data):

    def detect_outliers(laptimes, divider):
        rng = max(laptimes) - min(laptimes)
        outlier_detection = DBSCAN(min_samples = 2, eps = rng/divider)

        return outlier_detection.fit_predict(np.array(laptimes).reshape(-1, 1))

    laptime_data['valid'] = detect_outliers(laptimes=laptime_data['laptime_seconds'], divider=4)

    # 2 clusters - onroad AND offroad
    if 0 in laptime_data['valid'].to_list() and 1 in laptime_data['valid'].to_list():  
        onroad = laptime_data.loc[laptime_data['valid'] == 0].copy()
        onroad_clusters = detect_outliers(laptimes=onroad['laptime_seconds'], divider=8)
        onroad['valid'] = [x!=-1 for x in onroad_clusters]
        onroad['track_layout'] = ["A" for i in range(len(onroad_clusters))]

        offroad = laptime_data.loc[laptime_data['valid'] == 1].copy()
        onroad_clusters = detect_outliers(laptimes=offroad['laptime_seconds'], divider=8)
        offroad['valid'] = [x!=-1 for x in onroad_clusters]
        offroad['track_layout'] = ["B" for i in range(len(onroad_clusters))]

        laptime_data = pd.concat([onroad, offroad])

    # 1 cluster - onroad OR offroad
    else:
        laptime_data['valid'] = detect_outliers(laptimes=laptime_data['laptime_seconds'], divider=8)
        laptime_data['valid'] = [x!=-1 for x in laptime_data['valid']]
        laptime_data['track_layout'] = ["A" for i in range(len(laptime_data))]

    return laptime_data
