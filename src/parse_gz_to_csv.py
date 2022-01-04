'''parsing 5-core files from http://jmcauley.ucsd.edu/data/amazon/
new site: https://nijianmo.github.io/amazon/index.html'''


import simplejson as json
import gzip
import sys
import csv
import os

jsonFile_name = sys.argv[1] # File name end with .gz
outFile_name = sys.argv[2] # A file root name


def parse_review_file(path):
    review_objs = []
    with gzip.open(path,'rt') as f:
        for json_string in f:
            review_objs.append(json.loads(json_string))
    reviews = []
    vertices = dict()
    for r in review_objs:
        vertices[r['reviewerID']] = (True,'reviewer')
        vertices[r['asin']] = (False,'product')
        reviews.append((
            r['reviewerID'],r['asin']
        ))
    return(reviews,vertices)


if __name__ == '__main__':
    inpath = os.path.join("data_gz", jsonFile_name)
    outpath_edges = os.path.join("data_csv", outFile_name + "_edges.csv")
    outpath_nodes = os.path.join("data_csv", outFile_name + "_nodes.csv")
    reviews,reviewers = parse_review_file(inpath)
    with open(outpath_edges,'wt+') as f:
        writer = csv.writer(f)
        writer.writerow(('reviewer_id','product_id'))
        writer.writerows(reviews)
    with open(outpath_nodes,'wt+') as f:
        writer = csv.writer(f)
        writer.writerow(('vertex_id','type','vtype'))
        writer.writerows([(i,j,k) for (i,(j,k)) in reviewers.items()])
