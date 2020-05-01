import os

import pandas as pd

data_dir = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.isdir(data_dir):
    os.mkdir(data_dir)

MAX_SHIPS = 20


def download_source():
    # TODO: Implement grabbing data from https://www.marinecadastre.gov/ais/
    raise NotImplementedError


def parse_noaa_ships(year, month, zone='01'):
    ships = dict()

    fname = 'AIS_{}_{:02d}_Zone{}.csv'.format(year, month, zone)
    fpath = os.path.join(data_dir, fname)
    if not os.path.isfile(fpath):
        download_source(year, month, zone)

    reader = pd.read_csv(fpath, chunksize=100)
    for i, chunk in enumerate(reader):
        for imo, imo_df in chunk.groupby('IMO'):
            if imo in ships:
                ships[imo].append(imo_df)
            elif len(ships) >= MAX_SHIPS:
                continue
            else:
                ships[imo] = [imo_df]
        if i >= 10000:
            break
    reader.close()
    return {imo: pd.concat(imo_dfs) for imo, imo_dfs in ships.items()}


def pre_process_ship(ship_df):
    static_attrs = ['Length', 'Width', 'Draft', 'Cargo']
    # length, width, draft, cargo = ship_df[static_attrs].iloc[0]
    ship_df = ship_df.drop(static_attrs + ['IMO', 'Status']
                           + ['VesselName', 'MMSI', 'CallSign'], axis=1)
    ship_df['BaseDateTime'] = pd.to_datetime(ship_df['BaseDateTime'])
    ship_df = ship_df.sort_values('BaseDateTime').reset_index(drop=True)
    return ship_df


def parse_routes(ship_df):
    # TODO: Implement a softer condition,
    #  ship may register negligible SOG and very low LAT LON deltas
    #  which probably still means lack of moevement
    zero_sog = [0] + ship_df.index[ship_df['SOG'] == 0].tolist()
    if zero_sog == [0]:
        return []  # no stopping within data
    routes = list(zip(zero_sog, zero_sog[1:]))

    # get route with most amount of AIS messages
    # start, end = max(routes, key=lambda x: x[1] - x[0])
    # max_route = ship_df[start:end]
    return routes


def calc_complexity(ship_df, routes):
    upd_routes = []
    for route in routes:
        deltas = ship_df[route[0]:route[1]].diff(1).dropna()[['LAT', 'LON']]
        # TODO: calculate route complexity:
        #  mean(cos(angle between successive points))
        #  discard very complex trajectories, mean < 0.8
        pass

    return upd_routes


def main():
    ships = parse_noaa_ships(2017, 1, '01')
    for imo, ship_df in ships.items():
        ship_df = pre_process_ship(ship_df)
        routes = parse_routes(ship_df)
        if not routes:
            continue
        routes = calc_complexity(ship_df, routes)
        # TODO: Discard routes with complex and erratic shapes


if __name__ == '__main__':
    main()
