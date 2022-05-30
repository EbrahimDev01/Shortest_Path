import graphs


GRAPH = graphs.graph_large
FIRST_ORIGIN_LOCATION = 0
DESTINATION_LOCATION = 4

def get_len_path(possible_path):
    sum_len_path = 0
    for i, possible_location  in enumerate(possible_path[:-1]):
        sum_len_path += GRAPH[possible_location][possible_path[i+1]]
    return sum_len_path

def get_previous_path(previous_location):
    return tuple(previous_location) if len(previous_location) > 1 else (-1, FIRST_ORIGIN_LOCATION)

def find_next_location(origin_location, available_path, previous_locations, wrong_paths):
    for next_location, len_origin_path in enumerate(available_path):
        if 0 < float(len_origin_path) < float('inf') and next_location != origin_location and\
            next_location not in previous_locations and\
            next_location not in wrong_paths.get(get_previous_path(previous_locations + [origin_location]), []):
                previous_locations.append(origin_location)
                origin_location = next_location
                break
    return origin_location

def add_path_to_wrong_paths(origin_location, previous_path, wrong_paths):
    wrong_location = wrong_paths.get(previous_path, False)
    
    if wrong_location:
        wrong_paths[previous_path].append(origin_location)
    else:
        wrong_paths[previous_path] = [origin_location,]

def add_path_to_possible_paths(origin_location, previous_locations, all_right_paths):
    access_path = tuple(previous_locations + [origin_location])
    all_right_paths[access_path] = get_len_path(access_path)

def get_right_paths():
    len_graph = len(GRAPH)    
    if DESTINATION_LOCATION > len_graph:
        raise ValueError(f'pleas enter DESTINATION_LOCATION <= length GRAPH "{len_graph-1}"')
    
    origin_location = FIRST_ORIGIN_LOCATION
    previous_locations = []
    all_right_paths = {}
    wrong_paths = {}
    
    while True:
        available_path = GRAPH[origin_location]
        last_location = origin_location
        
        origin_location = find_next_location(origin_location, available_path, previous_locations, wrong_paths)
            
        if not previous_locations: 
            break
        
        if origin_location in (DESTINATION_LOCATION, last_location):
            previous_location = previous_locations[-1]
            previous_path = get_previous_path(previous_locations)
            
            add_path_to_wrong_paths(origin_location, previous_path, wrong_paths)
            
            if origin_location == DESTINATION_LOCATION:
                add_path_to_possible_paths(origin_location, previous_locations, all_right_paths)
            
            origin_location = previous_location
            del previous_locations[-1]
            
        
    
    return all_right_paths

def get_shortest_paths(all_right_paths):
    min_lne_path = min(all_right_paths.values())
    
    for path, len_path in all_right_paths.items():
        if min_lne_path == len_path:
            yield path, len_path
            
def get_path_between_two_lne(all_right_paths, min_len_path=None, max_len_path=None):
    if not min_len_path and not max_len_path:
        raise ValueError('Pleas enter max len or min len or both')
    elif min_len_path == None:
        min_len_path = min(all_right_paths.values())
    elif max_len_path == None:
        max_len_path = max(all_right_paths.values())
        
    for path, len_path in all_right_paths.items():
        if min_len_path <= len_path <= max_len_path:
            yield path, len_path

    
if __name__ == '__main__':
    all_paths = get_right_paths()
    if isinstance(all_paths, dict):
        print('\n', 'all possible path:', sep='')
        for len_path, path in all_paths.items():
            print(f'{len_path}: {path}')
            
        print('\n', 'path between 28 to 35 path:', sep='')
        for path, len_path in get_path_between_two_lne(all_paths, 28, 35):
            print(f'{path}: {len_path}')
            
        print('\n', 'shortest path:', sep='')
        for path, len_path in get_shortest_paths(all_paths):
            print(f'{path}: {len_path}')
                        
    else:
        print(all_paths[-1])
