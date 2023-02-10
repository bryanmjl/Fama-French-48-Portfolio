# Fama French 48 Portfolio Model
Given a hypothetical scenario of an investor who is **in 2016** and would like to allocate his money amongst 48 industries (Fama French) with an investment horizon of **5 years**, how can he best do so? This project aims to build an optimal portfolio out of Fama French 48 industries using data from 1986 to 2015. Here are the following assumptions used to build the portfolio:
1. For simplicity, the weights are static and no rebalancing of portfolio over the next 5 years from 2016 to 2020
5. No information allowed at the beginning of the Year 2016

To evaluate the portfolios, concept of backtesting (In and Out of sample train test) is applied and also additional portfolio stress testing to see the VaR and Expected Shortfall (ES) of each portfolio. From there, the optimal portfolio is chosen alongside performance metrics below mentioned.

# Portfolios chosen for testing
1. Optimal Shrinkage to boost robustness of Tangency Portfolio
    - Uses Shrinkage estimator developed by Prof Ledoit and Prof Wolf, based on a paper titled “Honey, I Shrunk the Covariance Matrix"
    - Apply Shrinkage estimator on Tangency Portfolio
Shrunk the Covariance Matrix”
2. Hierarchical Risk Parity Portfolio
    - Enhancement of Vanilla Risk Parity Portfolio
3. Black Litterman
    - Uses forward views to build onto basic portfolio model
    - Uses Idzorek's version of Black Litterman Model as per https://www.cis.upenn.edu/~mkearns/finread/idzorek.pdf

# Performance Metrics Guidelines
1. Sharpe Ratio
    - Provides an accurate representation of risk-reward payoff
2. Benchmark against Baseline Market Portfolio and Equally Weighted Portfolio (EWP)
    - These portfolio are considered the baseline standard for any portfolio building
3. Backtesting using the concept of In-sample and Out of Sample Analysis
    - In-sample dataset range one: 2000 Jan to 2010 Dec
    - Out-sample dataset range one: 2011 Jan to 2015 Dec
    - In-sample dataset range two: 2000 Jan to 2010 Jul
    - Out-sample dataset range two: 2010 August to 2015 Dec
    - In-sample dataset range three: 2000 Jan to 2011 May
    - Out-sample dataset range three: 2011 June to 2015 Dec

The idea of using In-sample Out-of-sample analysis works well for backtesting to see how well our portfolios would have performed given some training data on an "unseen" dataset. In-sample has a range of 10 years while Out-sample has a range of 5 years 

# Details
For more details on the individual portfolio models, please refer to the "Report.md"

# Credits
This was adapated from my NUS module DBA3713 Analytics in Risk Management but concepts are extended beyond class's teachings