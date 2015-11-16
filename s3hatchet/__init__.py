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

def loader(instream, output_dump, extractRegex, attributes, sField, sVar):
    attributes = [(str(a.split("=")[0]), str(a.split("=")[1])) for a in ['date=int', 'size=int'] + attributes]

    instream = split_load(instream, extractRegex, attributes)

    dataset = np.array([i for i in instream], dtype=attributes)

    for f in np.unique(dataset[sField]):
        idxs = np.where(dataset[sField] == f)
        click.echo('''FIELD:\t%s''' % (f))
        for v in sVar:
            click.echo('''[%s]\t\t\tCount:\t%s
    \t\t\tSum:\t%s
    \t\t\tMin:\t%s
    \t\t\tMean:\t%s
    \t\t\tMax:\t%s''' % (
                    v,
                    dataset[idxs].shape[0],
                    dataset[idxs][v].sum(),
                    dataset[idxs][v].min(),
                    np.mean(dataset[idxs][v]),
                    dataset[idxs][v].max()
                    ))
        click.echo('---------------------------------------------')


