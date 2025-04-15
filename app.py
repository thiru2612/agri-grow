from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import random

app = Flask(__name__)

# Load datasets
soil_data = pd.read_csv("data/SoilData.csv")
weather_data = pd.read_csv("data/WeatherData.csv")
cost_data = pd.read_csv("data/CostData.csv")
market_price_data = pd.read_csv("data/MarketPrice.csv")
accepted_suggestions = pd.read_csv("data/AcceptedSuggestions.csv")

# Adjust prices dynamically based on saturation
def dynamic_price_adjustment(market_price_data, accepted_suggestions, district):
    adjusted_prices = market_price_data.copy()
    for crop in market_price_data['Crop'].unique():
        count = accepted_suggestions[
            (accepted_suggestions['Crop'] == crop) &
            (accepted_suggestions['District'] == district)
        ].shape[0]
        adjustment_factor = max(0.5, 1 - 0.1 * count)  # Minimum 50% of base price
        adjusted_prices.loc[
            (adjusted_prices['Crop'] == crop) & (adjusted_prices['District'] == district),
            'PricePerAcre'
        ] *= adjustment_factor
    return adjusted_prices

# Filter crops based on soil, weather, and cost constraints
def filter_crops(farmer_input):
    suitable_crops = soil_data[
        (soil_data['SoilType'] == farmer_input['SoilType']) &
        (soil_data['N'] <= farmer_input['N'] + 10) &
        (soil_data['P'] <= farmer_input['P'] + 10) &
        (soil_data['S'] <= farmer_input['S'] + 10)
    ]['Crop'].tolist()

    suitable_crops = weather_data[
        (weather_data['Crop'].isin(suitable_crops))
    ]['Crop'].unique().tolist()

    affordable_crops = [
        crop for crop in suitable_crops
        if crop in cost_data['Crop'].values and
        cost_data[cost_data['Crop'] == crop]['Cost'].values[0] * farmer_input['Acres'] <= farmer_input['Budget']
    ]
    return affordable_crops

# Fitness function: Evaluate total profit and diversity
def fitness_function(candidate, crops, adjusted_prices, farmer_input):
    total_profit = 0
    total_cost = 0
    crop_count = 0

    for i, acres in enumerate(candidate):
        if acres > 0:
            crop = crops[i]
            matching_rows = adjusted_prices[
                (adjusted_prices['Crop'] == crop) & (adjusted_prices['District'] == farmer_input['District'])
            ]
            if matching_rows.empty:
                continue

            price_per_acre = matching_rows['PricePerAcre'].values[0]
            cost_per_acre = cost_data[cost_data['Crop'] == crop]['Cost'].values[0]
            profit_per_acre = price_per_acre - cost_per_acre

            total_profit += profit_per_acre * acres
            total_cost += cost_per_acre * acres
            crop_count += 1

    penalty = 0
    if total_cost > farmer_input['Budget']:
        penalty += (total_cost - farmer_input['Budget']) * 10

    diversity_bonus = crop_count * 1000
    return total_profit + diversity_bonus - penalty

# Generate initial population
def initialize_population(pop_size, crops, acres):
    return [np.random.randint(0, acres // 2 + 1, size=len(crops)).tolist() for _ in range(pop_size)]

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(candidate, max_acres):
    index = random.randint(0, len(candidate) - 1)
    candidate[index] = random.randint(0, max_acres // 2)
    return candidate

def genetic_algorithm(farmer_input, crops, adjusted_prices, generations=50, pop_size=20):
    population = initialize_population(pop_size, crops, farmer_input['Acres'])
    max_acres = farmer_input['Acres']

    for gen in range(generations):
        fitness_scores = [fitness_function(candidate, crops, adjusted_prices, farmer_input) for candidate in population]
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
        population = sorted_population[:pop_size // 2]

        new_population = []
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1, max_acres), mutate(child2, max_acres)])
        population = new_population

    best_candidate = max(population, key=lambda x: fitness_function(x, crops, adjusted_prices, farmer_input))
    return best_candidate

@app.route("/")
def index():
    unique_districts = sorted(weather_data['District'].unique())
    return render_template("index.html", districts=unique_districts)

@app.route("/predict", methods=["POST"])
def predict():
    soil_type = request.form["soil_type"].capitalize()
    n = int(request.form["nitrogen"])
    p = int(request.form["phosphorous"])
    s = int(request.form["sulfur"])
    district = request.form["district"]
    acres = int(request.form["acres"])
    budget = int(request.form["budget"])

    farmer_input = {
        "SoilType": soil_type,
        "N": n,
        "P": p,
        "S": s,
        "District": district,
        "Acres": acres,
        "Budget": budget,
    }

    adjusted_prices = dynamic_price_adjustment(market_price_data, accepted_suggestions, district)
    crops = filter_crops(farmer_input)

    if not crops:
        return render_template("results.html", error="No suitable crops found!")

    best_allocation = genetic_algorithm(farmer_input, crops, adjusted_prices)
    results = []
    for i, allocated_acres in enumerate(best_allocation):
        if allocated_acres > 0:
            crop = crops[i]
            matching_rows = adjusted_prices[
                (adjusted_prices["Crop"] == crop) & (adjusted_prices["District"] == district)
            ]
            if matching_rows.empty:
                continue
            price_per_acre = matching_rows["PricePerAcre"].values[0]
            cost_per_acre = cost_data[cost_data["Crop"] == crop]["Cost"].values[0]
            profit = (price_per_acre - cost_per_acre) * allocated_acres

            results.append({
                "crop": crop,
                "acres": int(allocated_acres),
                "profit": round(profit, 2)
            })

    return render_template("results.html", results=results, farmer_input=farmer_input)

import json

@app.route("/accept", methods=["POST"])
def accept():
    try:
        selected_crops = request.form.getlist("results")  # Get selected crops
        farmer_input = json.loads(request.form["farmer_input"])  # Deserialize JSON string

        if not selected_crops:
            return "No crops selected. Please select crops and try again.", 400

        next_farmer_id = accepted_suggestions["FarmerID"].max() + 1 if not accepted_suggestions.empty else 1

        for selection in selected_crops:
            crop, acres = selection.split(":")
            accepted_suggestions.loc[len(accepted_suggestions)] = [next_farmer_id, crop, farmer_input["District"], int(acres)]

        accepted_suggestions.to_csv("data/AcceptedSuggestions.csv", index=False)

        return render_template("success.html", message="Your selections have been saved successfully!")
    except Exception as e:
        print(f"Error processing request: {e}")
        return "Bad Request: Unable to process your selection.", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)