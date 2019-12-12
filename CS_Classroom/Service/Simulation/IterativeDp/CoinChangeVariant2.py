import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp import CoinChangeVariant2 as ccv2
from pattern.SimulationStrategy.Context import SimulationContext


def coin_change_variant2_entry_data(data):
    data = {'coin_array_variant2' : data['coin_array_variant2'],'payment_variant2' : data['payment_variant2']}
    posts = db.coin_change_variant2
    post_id = posts.insert_one(data).inserted_id
    return post_id


def coin_change_variant2_simulation(name):
    data = db.coin_change_variant2.find_one({"_id": ObjectId(name)})
    #arr = data['lis_array']
    coin_array1 = ast.literal_eval(data['coin_array_variant2'])
    coin_array2 = []
    coin_array2.append(0)
    for i in range(len(coin_array1)):
        coin_array2.append(int(coin_array1[i]))

    k = len(coin_array1)
    payment = data['payment_variant2']
    dp_simulation_strategy = ccv2.CoinChangeVariant2(int(payment), k , coin_array2)
    dp_simulation_context = SimulationContext(dp_simulation_strategy)
    data = dp_simulation_context.get_data()
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "coin_change_variant2"})
        if key is not None:
            saved = 1
    return data , saved
