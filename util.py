from __future__ import print_function

import os
import sys
import requests
import json


from dnac import get_auth_token, create_url, wait_on_task

def get_url(url,version=1):

    url = create_url(path=url, version=version)
    print(url)
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()


def tagmapping(tagname):
    if tagname is None:
        return []
    # get tag_id
    response = get_url("dna/intent/api/v1/tag?name={}".format(tagname))
    tag_id =  response['response'][0]['id']
    if tag_id is None:
        return []
    response = get_url('dna/intent/api/v1/tag/{}/member?memberType=networkdevice'.format(tag_id))
    return [association['instanceUuid'] for association in response['response']]

def device2id(device):
        response = get_url('dna/intent/api/v1/network-device?managementIpAddress={0}'.format(device))
        return (response['response'][0]['id'])

def ipmapping(iplist):
    deviceIds = map (device2id, iplist)
    return list(deviceIds)

def find_ids(tagname, ipList):
    if tagname:
        tagids = tagmapping(tagname)
    else:
        tagids = []
    if ipList:
        ipids = ipmapping(ipList)
    else:
        ipids = []
    ipids.extend(tagids)
    # make them unique
    return list(set(ipids))

def post_and_wait(url, data):

    token = get_auth_token()
    url = create_url(path=url)
    print(url)
    headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)

    taskid = response.json()['response']['taskId']
    print ("Waiting for Task %s" % taskid)
    task_result = wait_on_task(taskid, token, timeout=3600, retry_interval=60)

    return task_result

def put_and_wait(url, data):

    token = get_auth_token()
    url = create_url(path=url)
    headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}

    try:
        response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)

    taskid = response.json()['response']['taskId']
    print ("Waiting for Task %s" % taskid)
    task_result = wait_on_task(taskid, token, timeout=900, retry_interval=60)

    return task_result

def delete_and_wait(url):
    token = get_auth_token()
    url = create_url(path=url)
    headers= { 'x-auth-token': token['token'], 'content-type' : 'application/json'}

    try:
        response = requests.delete(url, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print ("Error processing request", cerror)
        sys.exit(1)

    taskid = response.json()['response']['taskId']
    print ("Waiting for Task %s" % taskid)
    task_result = wait_on_task(taskid, token, timeout=60, retry_interval=3)

    return task_result
