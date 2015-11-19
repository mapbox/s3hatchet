import click, json, re

import numpy as np

def getRange(xyz):
    return xyz[:, 0].min(), xyz[:, 0].max(), xyz[:, 1].min(), xyz[:, 1].max()

def getIdx():
    tt = np.zeros((3, 3), dtype=bool)
    tt[1, 1] = True

    return np.dstack(np.where(tt != True))[0] - 1

def parseString(tilestring, matcher):
    tile = [int(r) for r in matcher.match(tilestring).group().split('-')]
    tile.append(tile.pop(0))
    return tile

@click.command('findedges')
@click.argument('inputtiles', default='-', required=False)
@click.option('--parsenames', is_flag=True)
def findedges(inputtiles, parsenames):
    try:
        inputtiles = click.open_file(inputtiles).readlines()
    except IOError:
        inputtiles = [inputtiles]

    # parse the input stream into an array
    if parsenames:
        tMatch = re.compile(r"[\d]+-[\d]+-[\d]+")
        tiles = np.array([parseString(t, tMatch) for t in inputtiles])
    else:
        tiles = np.array([json.loads(t) for t in inputtiles])

    if inputtiles[:, 2].min() != inputtiles[:, 2].max():
        raise ValueError("All tile zooms must be the same")

    zoom = inputtiles[0, -1]

    xmin, xmax, ymin, ymax = getRange(inputtiles)

    # make an array of shape (xrange + 3, yrange + 3)
    burn = np.zeros((xmax - xmin + 3, ymax - ymin + 3), dtype=bool)

    # using the tile xys as indicides, burn in True where a tile exists
    burn[(inputtiles[:,0] - xmin + 1, inputtiles[:, 1] - ymin + 1)] = True

    # Create the indixes for rolling
    idxs = getIdx()

    # Using the indices to roll + stack the array, find the minimum along the rolled / stacked axis
    xys_edge = (np.min(np.dstack((
        np.roll(np.roll(burn, i[0], 0), i[1], 1) for i in idxs
        )), axis=2) - burn)

    # Set missed non-tiles to False
    xys_edge[burn == False] = False

    # Recreate the tile xyzs, and add the min vals
    xys_edge = np.dstack(np.where(xys_edge))
    xys_edge[0, :, 0] += xmin - 1
    xys_edge[0, :, 1] += ymin - 1

    # Echo out the results
    for t in xys_edge[0]:
        click.echo(t.tolist() + [zoom])


if __name__ == '__main__':
    findedges()