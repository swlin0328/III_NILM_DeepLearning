""" Config for the REDD dataset """


# Windows (training, validation, testing)
WINDOWS = {
    'train': {
        1: ("2017-08-01", "2017-10-25"),
        2: ("2017-08-01", "2017-10-25"),
        3: ("2017-08-01", "2017-10-25"),
        4: ("2017-08-01", "2017-10-25"),
        5: ("2017-08-01", "2017-10-25"),
        6: ("2017-08-01", "2017-10-25"),
        7: ("2017-08-01", "2017-10-25"),
        8: ("2017-08-01", "2017-10-25")
    },
    'unseen_activations_of_seen_appliances': {
        1: ("2017-08-01", "2017-10-25"),
        2: ("2017-08-01", "2017-10-25"),
        3: ("2017-08-01", "2017-10-25"),
        4: ("2017-08-01", "2017-10-25"),
        5: ("2017-08-01", "2017-10-25"),
        6: ("2017-08-01", "2017-10-25"),
        7: ("2017-08-01", "2017-10-25"),
        8: ("2017-08-01", "2017-10-25") 
    },
    'unseen_appliances': {
        4: ("2017-08-01", None),
        6: ("2017-08-01", None),
        7: ("2017-08-01", None),
        8: ("2017-08-01", None)
    }
}


# Appliances
APPLIANCES = [
    'television',
    'air conditioner',
    'bottle warmer',
    'washing machine',
    'fridge',
    'light',
]


# Training & validation buildings, and testing buildings
BUILDINGS = {
    'television': {
        'train_buildings': [1, 2 , 4, 6],
        'unseen_buildings': [7],
    },
    'air conditioner': {
        'train_buildings': [ 2, 3, 4, 5, 8],
        'unseen_buildings': [6,7],
    },
    'bottle warmer': {
        'train_buildings': [1, 2, 3],
        'unseen_buildings': [4],
    },
    'washing machine': {
        'train_buildings': [2, 3 , 4, 5],
        'unseen_buildings': [6,7],
    },
    'fridge': {
        'train_buildings': [1, 2, 3 , 4, 5],
        'unseen_buildings': [6,7],
    },
}
