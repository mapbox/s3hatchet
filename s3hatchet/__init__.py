import numpy as np
import re, time, cPickle

import click


def split_load(instream, extractRegex, attributes):
    timePad = [0, 0, 0]

    matcher = re.compile(extractRegex)
    for row in instream:
        trow = [l.rstrip() for l in reversed(row.split(" ")) if len(l) != 0]
        date = time.mktime([
            int(d) for d in trow.pop().split('-')
            ] + [
            int(t) for t in trow.pop().split(':')
            ] + timePad)
        filesize = int(trow[1])
        try:
            extract = [m for m in matcher.match(trow[0]).groups()]
        except:
            print trow
            exit(0)

        yield tuple([date] + [filesize] + extract)

def loader(instream, output_dump, extractRegex, attributes, summarize):
    attributes = [(str(a.split("=")[0]), str(a.split("=")[1])) for a in ['date=int', 'size=int'] + attributes]

    instream = split_load(instream, extractRegex, attributes)

    dataset = np.array([i for i in instream], dtype=attributes)

    sField, sVar = summarize


    for f in np.unique(dataset[sField]):
        idxs = np.where(dataset[sField] == f)
        click.echo('''FIELD:\t%s
COUNT:\t%s
MIN:\t%s
MEAN:\t%s
MAX:\t%s
---------------------''' % (
                f,
                dataset[idxs].shape[0],
                dataset[idxs][sVar].min(),
                np.mean(dataset[idxs][sVar]),
                dataset[idxs][sVar].max()
                ))


