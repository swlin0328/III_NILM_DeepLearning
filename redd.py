""" Config for the III dataset """


# Windows (training, validation, testing)
WINDOWS = {
    'train': {
        1: ("2011-04-01", "2011-05-25"),
        2: ("2011-04-01", "2011-05-25"),
        #3: ("2011-04-01", "2011-05-25"),
        4: ("2011-04-01", "2011-05-25"),
        5: ("2011-04-01", "2011-05-25")
    },
    'unseen_activations_of_seen_appliances': {
        1: ("2011-05-26", "2011-05-30"),
        2: ("2011-05-26", "2011-05-30"),
        #3: ("2011-05-26", "2011-05-30"),
        4: ("2011-05-26", "2011-05-30"),
        5: ("2011-05-26", "2011-05-30")
    },
    'unseen_appliances': {
        2: ("2011-04-01", None),
        5: ("2011-04-01", None),
    }
}
# Appliances
APPLIANCES = [
    'kettle',
    'microwave',
    'dish washer',
    'washing machine',
    'fridge',
]


# Training & validation buildings, and testing buildings
BUILDINGS = {
    'kettle': {
        'train_buildings': [1, 2 , 4],
        'unseen_buildings': [5],
    },
    'microwave': {
        'train_buildings': [ 1,2],
        'unseen_buildings': [5],
    },
    'washing machine': {
        'train_buildings': [1, 5],
        'unseen_buildings': [2],
    },
    'dish washer': {
        'train_buildings': [1,2],
        'unseen_buildings': [5],
    },
    'fridge': {
        'train_buildings': [ 1,],
        'unseen_buildings': [2],
    },
}
