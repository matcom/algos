def gale_shapley_incomplete(proposers, receivers, prop_prefs, rec_prefs):
    free_proposers = list(proposers)
    next_choice_idx = {p: 0 for p in proposers}
    matches = {} 
    prop_matches = {}  
    
    while free_proposers:
        p = free_proposers.pop(0)
        
        if next_choice_idx[p] >= len(prop_prefs[p]):
            continue 
            
        r = prop_prefs[p][next_choice_idx[p]]
        next_choice_idx[p] += 1
        
        if r not in rec_prefs or p not in rec_prefs[r]:
            free_proposers.append(p)  
            continue
            
        current_p = matches.get(r)
        
        if current_p is None:
            matches[r] = p
            prop_matches[p] = r
        else:
            if rec_prefs[r].index(p) < rec_prefs[r].index(current_p):
                matches[r] = p
                prop_matches[p] = r
                if current_p in prop_matches:
                    del prop_matches[current_p]
                free_proposers.append(current_p)
            else:
                free_proposers.append(p)
                
    return prop_matches

if __name__ == "__main__":
    P = ['p1', 'p2', 'p3']
    R = ['r1', 'r2', 'r3']
    prop_prefs = {
        'p1': ['r1', 'r2'],
        'p2': ['r1'],
        'p3': ['r2', 'r3']
    }
    rec_prefs = {
        'r1': ['p2', 'p1'],
        'r2': ['p1', 'p3'],
        'r3': ['p3']
    }
    
    result = gale_shapley_incomplete(P, R, prop_prefs, rec_prefs)
    print("Emparejamientos (Proponente -> Receptor):")
    for p, r in result.items():
        print(f"{p} -> {r}")