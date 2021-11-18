import os
from collections import namedtuple

import requests
import pandas as pd

# secrests
dozuki_key = os.environ.get('DOZUKI_KEY')

# authorization
HEADERS = {'Authorization': f'api {dozuki_key}'}

EP = 'https://medifab.dozuki.com/api/2.0/guides'

# Some categories don't want to be touched.
UNWANTED = ['archive', 'example', 'getting started with dozuki']

Simply_guide = namedtuple(
    'Simply_guide',
    ['guideid', 'revisionid', 'time_required_min', 'time_required_max']
)

## It takes guideid and returns a dict.  You may need to specify key to use.
def get_url(guideid, whatever):

    d = {
        'guide': f'{EP}/{guideid}',
        'releases': f'{EP}/{guideid}/releases'
    }

    return d.get(whatever, '')

def get_json(guideid, whatever):

    r = requests.get(
        get_url(guideid, whatever),
        headers=HEADERS
    )

    if r.status_code == 200:
        return r.json()

def patch_authorid(guideid, revisionid, authorid):

    r = requests.patch(
        url=get_url(guideid, 'guide'),
        headers=HEADERS,
        params={'revisionid': revisionid},
        json={'author': authorid}
    )

def patch_leadtime(guideid, revisionid, time_required_max, time_required_min=0):

    r = requests.patch(
        url=get_url(guideid, 'guide'),
        headers=HEADERS,
        params={'revisionid': revisionid},
        json={
            'time_required_max': time_required_max,
            'time_required_min': time_required_min,
        }
    )

def yes_guide(a_guide):  # yes, Prime Minister

    # Determin if the guide is affected.

    return all([
        len(a_guide['steps'])>0,
        #guide['time_required'].lower() == 'no estimate',
        #guide['author']['userid'] == 10,
        #guide['category'].lower() not in unwanted,
    ])

def guide(guideid):
    # It returns a simplified 'guide'.

    a_guide = get_json(guideid, 'guide')
    
    if a_guide and yes_guide(a_guide):

        return Simply_guide(
            guideid,
            a_guide['revisionid'],
            a_guide['time_required_min'],
            a_guide['time_required_max'],
        )

def patch_leadtime_from_csv(input_file):
    
    input_df = pd.read_csv(input_file)

    for row in input_df.itertuples():

        #print(row.guideid, row.time_required_max)
        a_guide = guide(row.guideid)

        patch_leadtime(
            guideid=row.id,
            revisionid=a_guide.revisionid,
            time_required_max=row.time_required_max,
        )

patch_leadtime_from_csv('input_file.csv')
