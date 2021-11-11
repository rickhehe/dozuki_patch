import os

import requests
import pandas as pd


# secrests
dozuki_key = os.environ.get('DOZUKI_KEY')

# authorization
HEADERS = {'Authorization': f'api {dozuki_key}'}

EP = 'https://medifab.dozuki.com/api/2.0/guides'

# Some categories don't want to be touched.
UNWANTED = ['archive', 'example', 'getting started with dozuki']

## It takes guideid and returns a dict.  You may need to specify key to use.
def get_url(guideid, whatever):

    d = {
        'guide': f'{ep}/{guideid}',
        'releases': f'{ep}/{guideid}/releases'
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
        #url=get_url(20, 'guide'),
        params={
            'revisionid': revisionid,
            #'revisionid': 11311,
        },
        headers=HEADERS,
        json={
            #'title':'1259-2200-100 (Dual Mount)'
            'author': authorid
        }
    )

def patch_leadtime(guideid, revisionid, time_required_max, time_required_min=0):

    r = requests.patch(
        url=get_url(guideid, 'guide'),
        params={
            'revisionid': revisionid,
        },
        headers=HEADERS,
        json={
            'time_required_max': time_required_max,
            'time_required_min': time_required_min,
        }
    )

'''
Check if steps exist and guide available.
'''
def guide(guideid):
    # It returns a simplified 'guide'.

    guide = get_json(guideid, 'guide')
    
    if guide:

        if all([
            #guide,
            len(guide['steps'])>0,
            #guide['author']['userid'] == 10,
            #guide['time_required'].lower() == 'no estimate',
            #guide['author']['userid'] == 10,
            #guide['category'].lower() not in unwanted,
            ]):

            o = {'id': guideid}

            o['revisionid'] = guide['revisionid']
            o['authorid'] = guide['author']['userid']

            o['time_required'] = guide['time_required']
            o['time_required_min'] = guide['time_required_min']
            o['time_required_max'] = guide['time_required_max']

            return o

def xxx():
    
    input_df = pd.read_csv(input_file)

    for row in itertuples(input_df):

        #print(row.guideid, row.time_required_max)
        
        a_guide = guide(row.guideid)

        if a_guide:
    
            pass

            #patch_leadtime(
            #    guideid=a_guide['id'],
            #    revisionid=a_guide['revisionid'],
            #    time_required_max=row.time_required_max,
            #)
