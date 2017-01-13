import codecs
from argparse import ArgumentParser
import os
import requests
import json
import re

base_url = 'http://catalog.sharedshelf.artstor.org/'
url_rest = '/assets?with_meta=true&limit=500000'


def main():
    parser = ArgumentParser()

    parser.add_argument("-o", "--filename", dest="filename", help="write to file", default="ArtStorOutput.json")
    parser.add_argument("-e", "--email", dest="email", help="your ArtStor email")
    parser.add_argument("-p", "--password", dest="password", help="your ArtStor password")
    parser.add_argument("-c", "--collection", dest="coll", help="Artstor Collection ID")

    args = parser.parse_args()

    try:
        if args.email and args.password:
            data = {'email': args.email, 'password': args.password}
            cookies = requests.post(base_url + 'account', data=data).cookies
        elif not args.email or not args.password:
            email = os.environ['ArtStor email:']
            password = os.environ['ArtStor password:']
            data = {'email': email, 'password': password}
            cookies = requests.post(base_url + 'account', data=data).cookies
    except Exception as e:
        print(e)
        parser.print_help()
        parser.error("need a valid ArtStor user email and password.")

    # get projects
    print("Writing records to %s from SharedShelf." % (args.filename))
    projs_start = requests.get(base_url + 'projects', cookies=cookies)
    projs_start.encoding = 'utf8'
    if args.coll:
        projs = projs_start.json()
        proj_id = args.coll

        total = 0
        output = {}
        publ_re = re.compile("^publishing_status[.-]\d+")
        print("Retrieving project %s" % (proj_id))
        url = base_url + 'projects/' + str(proj_id) + url_rest
        data_start = requests.get(url, cookies=cookies)
        data_start.encoding = 'utf8'
        data = data_start.json()
        fields_ss = data['metaData']['columns']
        assets = data['assets']
        fields = {}
        for n in range(len(fields_ss)):
            if publ_re.match(fields_ss[n]['dataIndex']) and 'publishing_status' not in fields:
                fields['publishing_status'] = ('publishing_status')
            else:
                fields[(fields_ss[n]['dataIndex'])] = (fields_ss[n]['header'])
        for item in range(len(assets)):
            for field in assets[item]:
                if field not in fields and field.replace('_multi_s', '_mfcl_lookup') in fields:
                    fields[field] = fields[field.replace('_multi_s', '_mfcl_lookup')] + "_facet"
                elif field not in fields:
                    fields[field] = field
        for item in range(len(assets)):
            record_id = assets[item]['id']
            output[record_id] = {}
            total += 1
            for field in assets[item]:
                if field in fields:
                    field_label = fields[field]
                    output[record_id][field_label] = assets[item][field]
                else:
                    output[record_id][field] = assets[item][field]
                    print("MISSING FIELD: " + field + ": " + data['assets'][item][field])

        ofile = open(args.filename, 'w')
        json.dump(output, ofile)
        ofile.close()
        print "Wrote out %d records" % total
    else:
        projs = projs_start.json()
        projs_ids = {}
        for proj in range(len(projs['items'])):
            if projs['items'][proj]['type_id'] == 200:
                projs_ids[(projs['items'][proj]['id'])] = projs['items'][proj]['name']
        projs_num = len(projs_ids)

        total = 0
        output = {}
        publ_re = re.compile("^publishing_status[.-]\d+")
        for proj in projs_ids:
            print("Retrieving project %s" % ((projs_ids[proj])))
            url = base_url + 'projects/' + str(proj) + url_rest
            data_start = requests.get(url, cookies=cookies)
            data_start.encoding = 'utf8'
            data = data_start.json()
            fields_ss = data['metaData']['columns']
            assets = data['assets']
            fields = {}
            for n in range(len(fields_ss)):
                if publ_re.match(fields_ss[n]['dataIndex']) and 'publishing_status' not in fields:
                    fields['publishing_status'] = ('publishing_status')
                else:
                    fields[(fields_ss[n]['dataIndex'])] = (fields_ss[n]['header'])
            for item in range(len(assets)):
                for field in assets[item]:
                    if field not in fields and field.replace('_multi_s', '_mfcl_lookup') in fields:
                        fields[field] = fields[field.replace('_multi_s', '_mfcl_lookup')] + "_facet"
                    elif field not in fields:
                        fields[field] = field
            for item in range(len(assets)):
                record_id = assets[item]['id']
                output[record_id] = {}
                total += 1
                for field in assets[item]:
                    if field in fields:
                        field_label = fields[field]
                        output[record_id][field_label] = assets[item][field]
                    else:
                        output[record_id][field] = assets[item][field]
                        print("MISSING FIELD: " + field + ": " + data['assets'][item][field])

        ofile = open(args.filename, 'w')
        json.dump(output, ofile)
        ofile.close()
        print "Wrote out %d records" % total


if __name__ == "__main__":
    main()
