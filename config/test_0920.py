""" Config for the REDD dataset """


# Windows (training, validation, testing)
WINDOWS = {
    'train': {
        1: ("2017-08-01", "2017-09-15"),
        2: ("2017-08-01", "2017-09-15"),
        3: ("2017-08-01", "2017-09-15"),
        4: ("2017-08-01", "2017-09-15"),
        5: ("2017-08-01", "2017-09-15"),
        6: ("2017-08-01", "2017-09-15"),
        7: ("2017-08-01", "2017-09-15"),
        8: ("2017-08-01", "2017-09-15")
    },
    'unseen_activations_of_seen_appliances': {
        1: ("2017-09-15", "2017-09-25"),
        2: ("2017-09-15", "2017-09-25"),
        3: ("2017-09-15", "2017-09-25"),
        4: ("2017-09-15", "2017-09-25"),
        5: ("2017-09-15", "2017-09-25"),
        6: ("2017-09-15", "2017-09-25"),
        7: ("2017-09-15", "2017-09-25"),
        8: ("2017-09-15", "2017-09-25")
    },
    'unseen_appliances': {
        6: ("2017-09-15", "2017-09-25"),
        7: ("2017-09-15", "2017-09-25"),
        8: ("2017-09-15", "2017-09-25")
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
        'train_buildings': [1, 2, 3 , 4, 5, 6],
        'unseen_buildings': [7,8],
    },
    'air conditioner': {
        'train_buildings': [1,2,3,4,5,6],
        'unseen_buildings': [7],
    },
    'bottle warmer': {
        'train_buildings': [1, 2, 3 , 4, 5, 6],
        'unseen_buildings': [7,8],
    },
    'washing machine': {
        'train_buildings': [1, 2, 3 , 4, 5, 6],
        'unseen_buildings': [7,8],
    },
    'fridge': {
        'train_buildings': [1, 2, 3 , 4, 5, 6],
        'unseen_buildings': [7,8],
    },
    'light': {
        'train_buildings': [1, 2, 3 , 4, 5, 6],
        'unseen_buildings': [7,8],
    },
}
