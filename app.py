from flask import Flask, request, render_template, jsonify
import numpy as np
import pickle
from scipy.stats import norm

app = Flask(__name__)

# Load saved model data and parameters
F = np.load(r'C:\Users\arjun sagar\PDF\OneDrive\Desktop\iso2\models\F.npy')  # Loaded cumulative distribution
px = np.load(r'C:\Users\arjun sagar\PDF\OneDrive\Desktop\iso2\models\px.npy')  # Probability of extras

# Load the parameters for the models from pickle files
with open(r'C:\Users\arjun sagar\PDF\OneDrive\Desktop\iso2\models\wicket_params.pkl', 'rb') as f:
    wicket_params = pickle.load(f)
with open(r'C:\Users\arjun sagar\PDF\OneDrive\Desktop\iso2\models\runs_params.pkl', 'rb') as f:
    runs_params = pickle.load(f)

# Wicket model class using loaded parameters
class WicketProbit:
    def __init__(self, params):
        self.a0 = params['a0']
        self.a1 = params['a1']
        self.a2 = params['a2']
        self.a3 = params['a3']

    def predict(self, balls_remaining, wickets_remaining):
        x = -self.a0 - self.a1 * balls_remaining - self.a2 * wickets_remaining + self.a3 * (balls_remaining ** 2)
        return norm.cdf(x)

# Runs model class using loaded parameters
class RunsOProbit:
    def __init__(self, params):
        self.a0 = params['a0']
        self.a1 = params['a1']
        self.a2 = params['a2']
        self.a3 = params['a3']
        self.mu0 = 0
        self.mu1 = params['mu1']
        self.mu2 = params['mu2']
        self.mu3 = params['mu3']
        self.mu4 = params['mu4']
        self.mu5 = params['mu5']

    def predict(self, runs, balls_remaining, wickets_remaining):
        x = self.a0 + self.a1 * balls_remaining + self.a2 * wickets_remaining + self.a3 * (balls_remaining ** 2)
        thresholds = [self.mu0, self.mu1, self.mu2, self.mu3, self.mu4, self.mu5]
        if runs == 0:
            return norm.cdf(thresholds[0] - x)
        elif runs <= 5:
            return norm.cdf(thresholds[runs] - x) - norm.cdf(thresholds[runs - 1] - x)
        else:
            return 1 - norm.cdf(thresholds[5] - x)

# Instantiate models using saved parameters
wicket_model = WicketProbit(wicket_params)
runs_model = RunsOProbit(runs_params)

# Utility function to calculate win probability and run outcomes
def game_state_info(F, runs_model, wicket_model, runs_remaining, balls_left, wickets_left):
    # Set a default probability of extras (e.g., 5%)
    px = 0.05  # Default probability of an extra (like a wide or no-ball)

    # Probability of winning given the game state
    win_prob = 1 - F[runs_remaining, balls_left, wickets_left]

    # Probability of an extra and a wicket
    prob_extra = px
    prob_wicket = (1 - px) * wicket_model.predict(balls_left, wickets_left)
    
    # Calculate probabilities for runs from 0 to 6 with equal likelihood if no extra or wicket occurs
    remaining_prob = 1 - px - prob_wicket
    equal_run_prob = remaining_prob / 7  # Divide remaining probability equally across 0 to 6 runs

    prob_0run = equal_run_prob
    prob_1run = equal_run_prob
    prob_2run = equal_run_prob
    prob_3run = equal_run_prob
    prob_4run = equal_run_prob
    prob_5run = equal_run_prob
    prob_6run = equal_run_prob

    return win_prob, prob_extra, prob_wicket, prob_0run, prob_1run, prob_2run, prob_3run, prob_4run, prob_5run, prob_6run

# Route to calculate probabilities
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    runs_remaining = int(data['runs_remaining'])
    balls_left = int(data['balls_left'])
    wickets_left = int(data['wickets_left'])
    
    results = game_state_info(F, runs_model, wicket_model, runs_remaining, balls_left, wickets_left)

    return jsonify({
        "win_prob": results[0],
        "prob_extra": results[1],
        "prob_wicket": results[2],
        "prob_0run": results[3],
        "prob_1run": results[4],
        "prob_2run": results[5],
        "prob_3run": results[6],
        "prob_4run": results[7],
        "prob_5run": results[8],
        "prob_6run": results[9],
    })

@app.route('/')
def index():
    return render_template('index.html')


def find_modified_target(F, runs_remaining, balls_left_init, wickets_left, balls_left_fin):
    # Computes the adjusted runs to get when the second innings is shortened
    reference = F[runs_remaining, balls_left_init, wickets_left]
    
    closest_target = None
    min_diff = float('inf')
    
    max_r = F.shape[0]
    for r in range(max_r):
        diff = abs(F[r, balls_left_fin, wickets_left] - reference)
        
        if diff < min_diff:
            min_diff = diff
            closest_target = r
    
    # Debugging: Print out values to check function behavior
    print(f"Reference: {reference}, Closest Target: {closest_target}, Min Diff: {min_diff}")
    
    return closest_target



# New route to calculate revised target score
@app.route('/revised_score', methods=['POST'])
def revised_score():
    data = request.get_json()
    
    # Extract required values from the JSON data
    runs_remaining = int(data.get('runs_remaining'))
    balls_left_init = int(data.get('balls_left_init'))
    wickets_left = int(data.get('wickets_left'))
    balls_left_fin = int(data.get('balls_left_fin'))
    
    # Call the find_modified_target function with the provided values
    revised_target = find_modified_target(F, runs_remaining, balls_left_init, wickets_left, balls_left_fin)
    
    return jsonify({'revised_target': revised_target})



import sys
sys.setrecursionlimit(2000)  # Adjust as needed


# Initialize score and overs tracking
current_score = {'runs': 0, 'wickets': 0, 'balls': 0, 'overs': 0}
predictions = ["wide", "no ball", "wicket"] + [str(i) for i in range(1, 7)]



@app.route('/scorecard')
def scorecard():
    return render_template('scorecard.html', current_score=current_score, predictions=predictions)

# Route to update score
@app.route('/update_score', methods=['POST'])
def update_score():
    global current_score
    data = request.get_json()
    runs = int(data['runs'])
    extras = int(data['extras'])
    wicket = int(data['wicket'])

    # Update score and wickets
    current_score['runs'] += runs + extras
    current_score['wickets'] += wicket

    # Count valid balls only if there are no extras
    if extras == 0:
        current_score['balls'] += 1

        # Check if we’ve completed an over
        if current_score['balls'] % 6 == 0:
            current_score['overs'] += 1
            current_score['balls'] = 0  # Reset balls count after each over

    return jsonify(current_score)

# Route to check prediction
@app.route('/check_prediction', methods=['POST'])
def check_prediction():
    data = request.get_json()
    user_prediction = data['prediction']
    actual_result = data['actual_result']
    response_message = "You're a Genius!" if user_prediction == actual_result else "Oops! You're Wrong!"
    
    return jsonify({'message': response_message})



# Define your route to serve the form
@app.route('/isoprobability')
def winprobability():
    return render_template('isoprobability.html')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Calculatescore')
def Calculatescore():
    return render_template('Calculatescore.html')

@app.route('/isoprobability')
def isoprobability():
    return render_template('isoprobability.html')



@app.route('/team')
def team():
    Guide = {"name": "RAJESH SUNDARESAN", "image": "rajesh-en.jpg", "website": "https://ece.iisc.ac.in/~rajeshs/", "linkedin": "https://www.linkedin.com/in/rajesh-sundaresan-7bb443114/?originalSubdomain=in"}
    team_members = [
        {"name": "ATHARV SURAWANSHI", "image": "atharv.jfif", "linkedin": "https://www.linkedin.com/in/atharv-suryawanshi?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app", "github": "https://github.com/AtharvSuryawanshi"},
        {"name": "ADHITYA PONNURAJ", "image": "adhitya.jpeg",  "github": "https://github.com/Arashi2304"},
        {"name": "ANKUSH", "image": "ankush.jpeg",  "linkedin": "https://www.linkedin.com/in/ankush-ahirwar-4561301a8?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app", "github": "https://github.com/ank1001"},
        {"name": "JAGATH CHANDRA", "image": "JC.jpeg", "linkedin": "#", "github": "#"},
        {"name": "ARJUN SAGAR N V", "image": "ARJUN.jpg",  "linkedin": "https://www.linkedin.com/in/arjun-sagar-06865827a/", "github": "https://github.com/Arjun-08"},
        
        # Add more members as needed
    ]
    return render_template('team.html', team_members=team_members, Guide= Guide)

@app.route('/iso_probability', methods=['GET', 'POST'])
def iso_probability():
    if request.method == 'POST':
        runs_remaining = int(request.form['runs_remaining'])
        balls_left_init = int(request.form['balls_left_init'])
        wickets_left = int(request.form['wickets_left'])
        balls_left_fin = int(request.form['balls_left_fin'])
        modified_target = find_modified_target(F, runs_remaining, balls_left_init, wickets_left, balls_left_fin)
        return jsonify({'modified_target': modified_target})
    return render_template('iso_probability.html')


@app.route('/clear_score', methods=['POST'])
def clear_score():
    global current_score
    current_score = {'runs': 0, 'wickets': 0, 'balls': 0, 'overs': 0}  # Reset the score to zero
    return jsonify(current_score)


@app.route('/next_ball_probabilities', methods=['POST'])
def next_ball_probabilities():
    data = request.get_json()
    remaining_balls = int(data.get('remaining_balls', 1))  # Default remaining balls
    remaining_wickets = int(data.get('remaining_wickets', 10))  # Default remaining wickets

    # Dummy probabilities for each outcome; replace these with actual iso-probability calculations
    outcomes = ["wide", "no ball", "wicket", "1", "2", "3", "4", "5", "6"]
    probabilities = {outcome: round(np.random.uniform(0.05, 0.25), 2) for outcome in outcomes}  # Example probabilities

    # Normalize probabilities to sum up to 1
    total_prob = sum(probabilities.values())
    probabilities = {outcome: prob / total_prob for outcome, prob in probabilities.items()}

    return jsonify(probabilities)

if __name__ == '__main__':
    app.run(debug=True)
