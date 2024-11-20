Iso-probability Criterion for Cricket Interruptions

1 Introduction
In the game of cricket, matches are occasionally interrupted due to rain or bad lighting, leading to
reduced overs of play. This affects the chances of winning for both teams. In order to tackle this
problem, various methods were introduced, such as Average Run Rate (ARR) or Most Productive
Overs (MPO), which often results in leaving one side at a disadvantage. The DL method was
introduced in 1997, which calculated the expected number of runs in the lost overs to estimate a
new target. This method was significantly better than its predecessors, yet it still had limitations.
In this project, we look into a new approach to tackle cricket interruptions in a more ’fair’ manner
called the Iso-probability criterion. It was developed by Michael Carter and Graeme Guthrie. As
the name suggests, it works on the principle of conserving the probability of winning for each team
before and after the interruption. Using data from matches between 2001 and 2024, we test this
method and analyze its effectiveness.


2 Methods
In order to implement this method, we define a cumulative distribution function F(r; n, w) that
models the number of runs r a team is expected to score, given n overs remaining and w wickets
in hand. This function will be the foundation for calculating the probability of winning based on
various game states, both before and after an interruption.


2.1 Defining Probability of Winning
If Team 2 has a target t and has already scored s runs, then the probability that Team 2 will win
the match with the remaining n overs and w wickets is given by:
1 − F(t − s; n, w)
Now, suppose an interruption occurs at this point, reducing the remaining overs to n
′ and
revising the target to t
′
. The iso-probability condition requires that the probability of winning
remains consistent before and after the interruption. Therefore, we set:
1 − F(t
′ − s; n
′
, w) = 1 − F(t − s; n, w)
This equation ensures that the probability of winning for Team 2 remains unchanged, thereby
maintaining fairness.


2.2 Modeling the Run-Scoring Process
To accurately estimate F(r; n, w) we model the run-scoring process with three possible outcomes
for each ball, denoted by b, the number of deliveries remaining, and w, wickets in hand. We assume
that the following events can occur on each ball:
1
• No Ball/Wide: With probability px, the score increases by 1 run, but b and w remain the
same.
• Wicket: With probability p(b, w), a wicket falls, reducing w by 1 and b by 1.
• Run Scored: With probability q(i; b, w), r increases by i, while b decreases by 1 and w remains
the same.
Using this approach, we build a probability model for each possible score trajectory, leading to a
comprehensive cumulative distribution function for run outcomes over the course of the remaining
deliveries.
Figure 1: Progression of 2nd innings [1]


2.3 Boundary Conditions
To finalize the model, we set boundary conditions that represent winning or losing situations:
• F(r, 0, w) = 1 if r ≥ 0 : The team loses if there are no balls remaining.
• F(r, b, 0) = 1 if r ≥ 0 : The team loses if there are no wickets left.
• F(r, n, w) = 0 if r < 0 : The team wins if they have scored the required runs.


2.4 Estimating Probability parameters

2.4.1 Wide or No Ball
The probability of wide or no ball is estimated using the following
Px =
Nos extra deliveries
Nos extra deliveries + Nos legitimate deliveries

2.4.2 Wickets
The probability of loosing a wicket p(b, w) while having b deliveries and w in hand is estimated
using a probit model. Let the unobserved variable be y
∗
b,w defined as
y
∗
b,w = α0 + α1b + α2w + θb,w
where α0, α1, α2 are constants and θb,w ∼ N(0, 1). According to the property of probit model, a
wicket falls if y
∗
b,w < 0 which occurs with a probability of p(b, w) = Φ(−α0 − α1b − α2w) where Φ
is cumulative distribution function of a normal distribution. Using our knowledge of the game we
can say: 1. α1 > 0 as it is more likely for a wicket to fall as the game progresses. 2. α2 > 0 as lower
batting order more easily to fall. In order to estimate these parameters, we use a random variable
2
yb which is 1 if wicket falls and 0 if it does. Assuming outcomes are independent of deliveries, we
get the likelihood function as follows:
Likelihood =
Y
n=1
Φ(−α0 − α1b − α2w)
yb
(1 − Φ(−α0 − α1b − α2w))1−yb
We choose value of α0, α1, α2 which maximizes the value of log-likelihood for an inning.


2.4.3 Runs
The probability of scoring runs i for iϵ{1, 2, 3, 4, 5, 6} is given by q(i; b, w) for b deliveries and w
wickets in hand. Here we will use an ordered probit model with an unobserved variable i
∗
b,w as
i
∗
b,w = β0 + β1b + β2w + ϵb,w
where the β’s are constants and ϵb,w ∼ N(0, 1). The thresholds for runs are denoted by µ0 ≤
µ1 ≤ µ2 ≤ µ3 ≤ µ4 ≤ µ5. The runs scored by batting team are i for i = {1, 2, 3, 4, 5, 6} if
µi−1 < i∗
b,w < µi
, zero runs if i
∗
b,w < µ0 and six runs if i
∗
b,w > µ5.
q(i; b, w) =



Φ(µ0 − β0 − β1b − β2w), if i = 0,
1 − Φ(µ5 − β0 − β1b − β2w), if i = 6,
Φ(µr − β0 − β1b − β2w)
−Φ(µr−1 − β0 − β1b − β2w), otherwise.
Using our knowledge of the game we can say:
1. β1 < 0 as scoring accelerates as game moves ahead
2. β2 > 0 scoring decreases in lower batting order
In order to calculate the probability, we do the same as previous estimation and calculate the
parameters which results in the maximum value of Likelihood.


2.5 Function F
Using these parameters, we construct our cumulative distribution function F(r; b, w)
F(t − s; b, w) = pxF(t − s − 1; b, w)
+ (1 − px)p(α)F(t − s; b − 1, w − 1)
+ (1 − px)(1 − p(α))X
6
i=0
q(i; α)F(t − s − i; b − 1, w) (1)


2.6 Code Breakdown
1. Data Processing:
(a) get_iso_data: Preprocesses the match data, including calculating balls remaining,
wickets remaining, and other match statistics.
(b) get_prob_of_wide_or_no_ball: Computes the probability of a wide or no ball based
on the match data.

3. Parameter Estimation (Probit Models):
(a) compute_llf: Calculates the log-likelihood for different run values using a probit model.

5. RunsOProbit Class: Contains methods to fit the model to the data and predict the
probability of scoring a specific number of runs given the match state.

(a) fit: Fits the model to the data.
(b) predict: Predicts the probability of scoring a specific number of runs based on the
match state.


7. Iso-probability Calculation:
(a) construct_F: Builds the cumulative distribution function F(r; b, w) using the parameters of the run and wicket models. It uses a recursive approach to fill in the values for
each combination of runs, balls, and wickets.
8. Training the Model:
(a) training: Imports data, sets up models, and fits them to the data. It includes the
training time and fitting for the wicket model, followed by the run model.
3 Results
After training the model on data of cricket matches from 2001-2024. We get the following values
for the parameters:
Parameters values Parameters values
px 0.04589
α0 0.84856 β0 -0.174
α1 0.00349 β1 -0.0084
α2 0.17753 β2 0.13
α3 -1.9190 β3 1.06-E5
µ1 0.94 µ3 1.325
µ2 1.263 µ4 2.321
µ5 2.328
Table 1: Parameter values
Runs 50 overs 20 overs 20 overs 1 over
10 wickets 10 wickets 3 wickets 3 wickets
0 0.024749 0.002703 0.060854 0.076849
1 0.626725 0.375976 0.661241 0.380887
2 0.226459 0.337476 0.181470 0.303909
3 0.036048 0.086351 0.025305 0.072922
4 0.005008 0.013871 0.003379 0.011482
5 0.032534 0.118765 0.020504 0.094397
6 0.000055 0.000319 0.000030 0.000238
7 0.002526 0.018644 0.001321 0.013421
Table 2: Selected values of q(i; b, w)


Now lets look at an example for how this method works and compares to DL method of resetting
targets. On 20th July 2003, in a cricket match Cambridge vs Oxford, Cambridge scored 190 from
50 overs and Oxford competed with a score of 162/1 from 31 overs when the match was interrupted.
They needed 29 from 12 overs, a very simple target indeed. But when rain stopped with 12 overs
still remaining, DL method declared Oxford as winner. The probability of Oxford winning was
very high, but not 1. Alternatively our method calculates probability of winning 99.1 %.
Here are re-calculated targets for previous matches using different target resetting methods [1].
In order emphasize this method, lets consider 3 grounds A,B,C with similar weather and lighting
conditions. Team 1A and 1B score 250 off 50 overs and team 1C scores 180 off 50 overs. Now
consider team 2A scores 120/3 in 20 overs and 2B, 2C scores 50/3 in 20 overs. Here, we will
compare and contrast DL vs Iso-probability method on our trained model.

Match Date ARR DL eDL mARR mDL
CG
NZ v. Sri Lanka 8 February 2001 162 154 159 155 157
India v. NZ 9 Jan 1999 202 200 203 206 217
218
NZ v. England 23 Feb 1997 133 164 183 142 177
195
SA v. England 12 Mar 1992 195 208 216 196 213
223
Table 3: Revised targets under various adjustment rules according to [1]
Team 1 Team 2 Target D/L D/L IsoP IsoP
at int at int target to-go target to-go
A 120/3 131 (in 30) 221 101 (20) 232 112 (20)
B 50/3 201 (in 30) 221 171 (20) 219 169 (20)
C 50/3 131 (in 30) 159 109 (20) 162 112 (20)
Table 4: Comparison of D/L and IsoP methods


4 Conclusion
In conclusion, we have implemented an adjustment mechanism for interrupted cricket matches that
preserves the likelihood of winning at the point of interruption, providing a more equitable and
incentive-free alternative to existing methods. Unlike traditional systems like Duckworth-Lewis,
which focus on maintaining resources (runs and wickets), this approach stresses the chance of winning as the most important metric to maintain throughout interruptions. By evaluating historical
data, we validated this rule and established that it effectively maintains match integrity and player
incentives, as evidenced in multiple previous matches when our strategy was used retrospectively.
In certain occasions, this modification resulted in different outcomes, demonstrating the rule’s potential impact on match results.
In contrast to our probability-based approach, proponents of the Duckworth/Lewis (D/L) method
believe that it promotes fairness by keeping the margin of advantage throughout pauses, even if it
occasionally favors the leading side. D/L advocates argue that their methodology is tactically neutral, encouraging players to stick to their customary strategy while avoiding inconsistencies caused
by probability-based changes. While we accept these arguments, we have demonstrated that our
strategy effectively maintains equity by balancing win probabilities. Our Iso-probability strategy
provides an alternative that closely aligns the match outcome with pre-interrupted conditions,
making it an equally viable option for fair target reset.
