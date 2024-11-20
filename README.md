# Iso-Probability Criterion for Cricket Interruptions

## Introduction

Cricket matches are often interrupted by external factors like rain or poor lighting, leading to shortened overs and potentially unfair outcomes. Traditional methods such as **Average Run Rate (ARR)** or **Most Productive Overs (MPO)**, and the widely used **Duckworth-Lewis (DL) Method**, address this issue but still leave room for improvement in fairness.

The **Iso-Probability Criterion**, developed by Michael Carter and Graeme Guthrie, ensures that the probability of winning for both teams remains consistent before and after an interruption. This repository implements this criterion using match data from 2001 to 2024 to model and analyze the fairness of this approach.

## Features

1. **Iso-Probability Calculator**
   - Adjusts the target in interrupted cricket matches while conserving win probabilities for both teams.
   - Ensures fairness by maintaining the balance of winning chances before and after interruptions.

2. **Win Probability Calculation**
   - Computes the probability of a team's victory based on:
     - Runs required
     - Overs remaining
     - Wickets in hand.

3. **Score Prediction**
   - Models run-scoring and wicket probabilities to predict match outcomes under different scenarios.
   - Provides dynamic score predictions and recalculates win probabilities based on real-time match conditions.


## Methodology

### 1. Defining the Probability of Winning
The winning probability is derived from a **Cumulative Distribution Function (CDF)**, `F(r; n, w)`, which models the runs a team is expected to score given:
- `r`: Runs
- `n`: Overs remaining
- `w`: Wickets in hand.

The Iso-Probability condition ensures:
\[ 1 - F(t' - s; n', w) = 1 - F(t - s; n, w) \]
where `t` and `t'` are the targets before and after interruption, and `s` is the score.

### 2. Modeling the Run-Scoring Process
The model accounts for three possible outcomes for each ball:
- **Wide/No Ball:** Probability `p_x`.
- **Wicket Falls:** Probability `p(b, w)` using a **Probit Model**.
- **Runs Scored:** Probability `q(i; b, w)` using an **Ordered Probit Model**.

### 3. Boundary Conditions
Boundary conditions ensure valid results for edge cases:
- Team loses if no balls or wickets remain and they haven’t met the target.
- Team wins if they have exceeded the required runs.

### 4. Parameter Estimation
- **Wide/No Ball Probability** (`p_x`) is calculated as:
  \[
  p_x = \frac{\text{Number of Extras}}{\text{Total Deliveries}}
  \]
- **Wicket Probability** uses a Probit Model:
  \[
  p(b, w) = \Phi(-\alpha_0 - \alpha_1b - \alpha_2w)
  \]
- **Run Probabilities** are modeled using:
  \[
  q(i; b, w) = \Phi(\mu_{i+1} - \beta_0 - \beta_1b - \beta_2w) - \Phi(\mu_i - \beta_0 - \beta_1b - \beta_2w)
  \]

---

## Results

- **Parameter Estimates:**
  - Wide/No Ball: `p_x = 0.04589`
  - Wicket Model: `α_0 = 0.84856`, `α_1 = 0.00349`, `α_2 = 0.17753`
  - Run Model: `β_0 = -0.174`, `β_1 = -0.0084`, `β_2 = 0.13`

- **Comparison with DL Method:**
  In retrospective tests on historical matches, the Iso-Probability method showed significant advantages in fairness, with recalculated targets leading to more equitable outcomes.

---

## Example Use Case

In the Cambridge vs. Oxford match on July 20, 2003:
- **DL Method Outcome:** Declared Oxford the winner after an interruption with 12 overs left.
- **Iso-Probability Outcome:** Calculated Oxford’s winning probability as 99.1%, preserving fairness while adjusting the target.

---

## How to Use

1. **Setup and Installation**
   - Clone the repository: `git clone <repository-url>`
   - Install dependencies: `pip install -r requirements.txt`

2. **Running the Application**
   - Launch the web interface: `python app.py`
   - Access the functionalities through:
     - **Score Calculator**
     - **Win Probability Calculator**
     - **Score Prediction Dashboard**

3. **Demo**
   [Insert link to live demo or screenshots]

---

## Conclusion

The Iso-Probability Criterion provides a fairer alternative to existing methods like DL by preserving the balance of winning probabilities during interruptions. Through rigorous modeling and testing, this approach has demonstrated its potential to transform cricket match adjustments.

---

Feel free to adapt the content as needed!
