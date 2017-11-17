""" Config for the III dataset """


# Windows (training, validation, testing)
WINDOWS = {
    'train': {
        1: ("2017-08-01", "2017-10-31"),
        2: ("2017-08-01", "2017-10-31"),
        3: ("2017-08-01", "2017-10-31"),
        4: ("2017-08-01", "2017-10-31"),
        5: ("2017-08-01", "2017-10-31"),
        6: ("2017-08-01", "2017-10-31"),
        7: ("2017-08-01", "2017-10-31"),
        8: ("2017-08-01", "2017-10-31")
    },
    'unseen_activations_of_seen_appliances': {
        1: ("2017-11-01", "2017-11-30"),
        2: ("2017-11-01", "2017-11-30"),
        3: ("2017-11-01", "2017-11-30"),
        4: ("2017-11-01", "2017-11-30"),
        5: ("2017-11-01", "2017-11-30"),
        6: ("2017-11-01", "2017-11-30"),
        7: ("2017-11-01", "2017-11-30"),
        8: ("2017-11-01", "2017-11-30")
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
        'train_buildings': [ 2, 3, 4, 5],
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
        'train_buildings': [1, 2, 3, 4, 5],
        'unseen_buildings': [6,7],
    },
}
