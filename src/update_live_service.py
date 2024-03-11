<<<<<<< HEAD
import pandas as pd
from livepopulartimes import get_populartimes_by_address
from datetime import datetime
=======
import os
import pandas as pd
from livepopulartimes import get_populartimes_by_address
from datetime import datetime, timedelta
from time import sleep

from scrape_services_data import places_seach, location, location_types
from preprocess_service_data import preprocess_data
>>>>>>> master


basic_attributes = ['name', 'formatted_address']
live_attributes = ['place_id', 'name', 'datetime', 'rating', 'rating_n',
                   'populartimes', 'usual_popularity', 'current_popularity']

<<<<<<< HEAD
def get_basical_data(file_path, attributes):
=======
def get_basic_data(file_path, attributes):
>>>>>>> master
    df = pd.read_csv(file_path)

    return df.loc[:, attributes].to_dict()


def map_weekday(origin):
    if origin:
        return origin - 1
    return 6


<<<<<<< HEAD
def update_live_data(basic_file_path, basic_attributes, attributes, file_path=None, write_csv=False):
    basic_data_dict = get_basical_data(basic_file_path, basic_attributes)

    # define live data dictionary
    live_data_dict = {attr: [] for attr in attributes}
=======
def update_live_data(basic_file_path, basic_attributes, attributes, file_dir=None, write_csv=False):
    basic_data_dict = get_basic_data(basic_file_path, basic_attributes)

    # define live data dictionary
    live_data_dict = {attr: [] for attr in attributes}
    live_data_dict.update({'datetime': []})
>>>>>>> master
    name_dict, addr_dict = basic_data_dict[basic_attributes[0]], basic_data_dict[basic_attributes[1]]

    # get datetime
    dt_obj = datetime.now()
    dt = dt_obj.strftime("%d-%m-%Y %H:%M")
    weekday = int(dt_obj.strftime('%w'))
    hour = int(dt_obj.strftime('%H'))

    # not live objects
    not_livetime_places = []

<<<<<<< HEAD
=======
    # get live data
>>>>>>> master
    for name, addr in zip(list(name_dict.values()), list(addr_dict.values())):
        live_response = get_populartimes_by_address(f'({name}) {addr}')

        if 'populartimes' in live_response:
            live_data_dict['usual_popularity'].append(live_response['populartimes'][map_weekday(weekday)]['data'][hour])
        else:
            not_livetime_places.append(name)
            continue

        live_data_dict['datetime'].append(dt)
        for attr in attributes:
            if attr not in ['datetime', 'usual_popularity']:
                live_data_dict[attr].append(live_response.get(attr, None))

    df = pd.DataFrame(live_data_dict)
<<<<<<< HEAD
    if file_path and write_csv:
        df.to_csv(file_path, sep=',')
=======
    filename = ' '.join(['live services', dt])
    filename += '.csv'
    if file_dir and write_csv:
        df.to_csv(os.path.join(file_dir, filename), sep=',')

>>>>>>> master

    return df, not_livetime_places


<<<<<<< HEAD
df, not_livetime_places = update_live_data(r'../data/services.csv',
                                             basic_attributes=basic_attributes,
                                             attributes=live_attributes,
                                             file_path=r'../data/live_services.csv',
                                             write_csv=True)

with open(r'../data/not_livetime_places.txt', 'w', encoding='utf-8') as file:
    for p in not_livetime_places:
        file.write(f'p\n')
=======
if __name__ == "__main__":
    # check if scraping basic data yet
    if not os.path.isfile(r'../data/services.csv'):
        service_list = places_seach(location_types, location,
                                    r'../data/searching_progress.txt',
                                    r'../data/services.json',
                                    max_pages=10)

        preprocess_data(r'../data/services.json',
                        included_pattern=r'(Cách Mạng Tháng 8|CMT8).*(Hồ Chí Minh|HCM)',
                        file_out=r'../data/services.csv')

    # update live data

    while int(datetime.now().strftime('%d')) < 4:
        # calculate next time
        next_time = datetime.now() + timedelta(minutes=15)

        # update live time
        df, not_live_places = update_live_data(r'../data/services.csv',
                                               basic_attributes=basic_attributes,
                                               attributes=live_attributes,
                                               file_dir=r'../data/live_data/',
                                               write_csv=True)

        with open(r'../data/not_livetime_places.txt', 'w', encoding='utf-8') as file:
            for p in not_live_places:
                file.write(f'{p}\n')

        # sleep to next time
        sleeping_time = max(0, int((next_time - datetime.now()).total_seconds()))
        sleep(sleeping_time)
>>>>>>> master
