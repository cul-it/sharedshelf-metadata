from argparse import ArgumentParser
import os
import requests
import json
import re

base_url = 'http://catalog.sharedshelf.artstor.org/'
url_rest = '/assets?with_meta=true&limit=5000000'
publ_re = re.compile("^publishing_status[.-]\d+")


def getCookies(args, parser):
    """Get cookies from authentication of SharedShelf API."""
    try:
        if args.email and args.password:
            data = {'email': args.email, 'password': args.password}
            cookies = requests.post(base_url + 'account', data=data).cookies
        elif not args.email or not args.password:
            email = os.environ['ArtStor email:']
            password = os.environ['ArtStor password:']
            data = {'email': email, 'password': password}
            cookies = requests.post(base_url + 'account', data=data).cookies
        return(cookies)
    except Exception:
        parser.print_help()
        parser.error("need a valid ArtStor user email and password.")


def getCollections(cookies):
    """Get + return data for all collections in SharedShelf."""
    projs_start = requests.get(base_url + 'projects', cookies=cookies)
    projs_start.encoding = 'utf8'
    return(projs_start.json())


def generateSingleCollDataDump(cookies, coll_id, filename):
    total = 0
    output = {}
    print("Retrieving project %s" % (coll_id))
    url = base_url + 'projects/' + str(coll_id) + url_rest
    data_resp = requests.get(url, cookies=cookies)
    data_resp.encoding = 'utf8'
    data = data_resp.json()
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
    with open(args.filename, 'w') as ofile:
        json.dump(output, ofile)
    print("Wrote out %d records" % total)


def generateDataDump(cookies, coll_id, filename):
    total = 0
    output = {}
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
    print("Wrote out %d records" % total)


def main():
    parser = ArgumentParser()

    parser.add_argument("-o", "--filename", dest="filename",
                        help="write to file", default="data/output.json")
    parser.add_argument("-e", "--email", dest="email",
                        help="Your SharedShelf User email. Required.")
    parser.add_argument("-p", "--password", dest="password",
                        help="Your SharedShelf User password. Required.")
    parser.add_argument("-c", "--collection", dest="coll",
                        help="A SharedShelf Collection ID if you only want to \
                              harvest a single SharedShelf Collection. \
                              Optional.")
    args = parser.parse_args()
    # Authenticating the User on the SharedShelf API.
    cookies = getCookies(args, parser)

    # Get All Projects/Collections in SharedShelf First.
    print("Writing metadata to %s from SharedShelf." % (args.filename))
    colls = {}
    projs = getCollections(cookies)
    if args.coll:
        coll_name = None
        for proj in projs['items']:
            if proj['id'] == int(args.coll):
                coll_id = args.coll
                coll_name = proj['name']
                colls[coll_id] = coll_name
        if not coll_name:
            print("We couldn't find a collection for that ID. Here's a list: ")
            print("==========================================================")
            for proj in projs['items']:
                print('Collection: %s || ID: %d' % (proj['name'], proj['id']))
            exit()
    else:
        for proj in projs['items']:
            coll_id = projs['items'][proj]['id']
            coll_name = projs['items'][proj]['name']
            colls[coll_id] = coll_name
    for n in colls:
        print(n)
    colls_num = len(colls)


if __name__ == "__main__":
    main()
