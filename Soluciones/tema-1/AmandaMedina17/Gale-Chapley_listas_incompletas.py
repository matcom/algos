def gale_shapley_incomplete_lists(proposer_preferences, receiver_preferences):
    """
    Algoritmo de Gale-Shapley adaptado para listas de preferencia incompletas.
    
    :param proposer_preferences: dict {proposer: [lista de receptores aceptables ordenados]}
    :param receiver_preferences: dict {receiver: [lista de proponentes aceptables ordenados]}
    :return: dict con los apareamientos finales {proposer: receiver} y {receiver: proposer}
    """
    # Inicialización de listas de proponentes libres
    free_proposers = list(proposer_preferences.keys())
    
    # Parejas actuales (None significa que están libres / solteros)
    proposer_match = {p: None for p in proposer_preferences}
    receiver_match = {r: None for r in receiver_preferences}
    
    # Seguimiento del índice del próximo receptor al que el proponente va a proponer
    next_proposal_index = {p: 0 for p in proposer_preferences}

    while free_proposers:
        current_proposer = free_proposers[0]
        proposer_list = proposer_preferences[current_proposer]
        current_index = next_proposal_index[current_proposer]

        # Si el proponente ya propuso a todos en su lista de aceptables, queda soltero
        if current_index >= len(proposer_list):
            free_proposers.pop(0)
            continue

        # Receptor al que se le hará la propuesta actual
        target_receiver = proposer_list[current_index]
        next_proposal_index[current_proposer] += 1  # Avanza el puntero en la lista

        # Verificar si el proponente es aceptable para el receptor
        receiver_list = receiver_preferences.get(target_receiver, [])
        if current_proposer not in receiver_list:
            # El receptor rechaza inmediatamente si el proponente no es aceptable
            continue

        current_partner = receiver_match[target_receiver]

        # Caso A: El receptor está libre
        if current_partner is None:
            receiver_match[target_receiver] = current_proposer
            proposer_match[current_proposer] = target_receiver
            free_proposers.pop(0)

        # Caso B: El receptor ya tiene pareja, se evalúa la preferencia
        else:
            rank_current = receiver_list.index(current_partner)
            rank_new = receiver_list.index(current_proposer)

            # Si el receptor prefiere al nuevo proponente (índice menor = mayor preferencia)
            if rank_new < rank_current:
                # La pareja anterior vuelve a estar libre
                proposer_match[current_partner] = None
                free_proposers.append(current_partner)

                # El receptor se empareja temporalmente con el nuevo proponente
                receiver_match[target_receiver] = current_proposer
                proposer_match[current_proposer] = target_receiver
                free_proposers.pop(0)
            
            # Caso C: Rechazo (si prefiere a su pareja actual, no hace nada y el ciclo continúa)

    return proposer_match, receiver_match


if __name__ == "__main__":
    # Proponentes y sus listas de aceptables en orden de preferencia
    proposers = {
        'm1': ['w1', 'w2'],        # m1 solo acepta a w1 y w2
        'm2': ['w2', 'w1', 'w3'],  # m2 acepta a w2, w1, w3
        'm3': ['w1']               # m3 solo acepta a w1
    }

    # Receptores y sus listas de aceptables en orden de preferencia
    receivers = {
        'w1': ['m2', 'm1'],        # w1 no acepta a m3
        'w2': ['m1', 'm2'],        # w2 acepta a m1 y m2
        'w3': ['m3']               # w3 solo acepta a m3
    }

    matches_p, matches_r = gale_shapley_incomplete_lists(proposers, receivers)

    print("--- Resultado de Apareamientos ---")
    for proposer, receiver in matches_p.items():
        status = receiver if receiver is not None else "Single (Soltero)"
        print(f"Proposer {proposer} -> Partner: {status}")