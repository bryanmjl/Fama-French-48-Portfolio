# Equally Weighted and Market Portfolio
These are the classic portfolio used in any traditional backtesting experiments. The equally weighted portfolio is simply allocating equal weights to each of the 48 industries, while the market portfolio is like an "industry" on its own. To select the optimal portfolio, it must have a sharpe ratio which performs the best against the benchmark portfolios in the Out-of-sample dataset. 


# Optimal Shrinkage Estimators to boost robustness of Tangency Portfolio
Given that CAPM is not practical in the real world due to the complexities of the financial market, I use optimal covariance shrinkage to account for noise and boosting robustness of our tangency portfolio. In this case, I used 3 train datasets ```train_1 train_2 train_3``` to test for each possible combination of Covariance Shrinkage. This gives me 3 Sharpe ratios, and I take the average Sharpe ratio and record it beside each combination of covariance shrinkage. Hence, I select the optimal shrinkage values for shrinking covariance matrix (using Constant Correlation Matrix) based on the highest average Sharpe ratio possible

# Black Litterman
Black Litterman (BL) is a type of portfolio technique which allows investors such as fund managers to input their forward-looking views on the market into the portfolio model. Black Litterman is considered better than the traditional MPT for a few reasons:
1. BL uses the view vector (Q) which allows investors to input their own views. 
2. Investors might not be very confident in their views since those forward views are highly uncertain and they are not clairvoyant as well. The model allows us to introduce the uncertainty of the views (Ω) to account for more realistic modelling, where the lower the uncertainty, the higher the returns will be closer towards that of the investors’ views

Given that Fama French dataset has 48 industries, I segmented them into 6 sectors based on the nature of the industries, which are:
1. Sector 1: Commodities (16 industries)
    - Agric, Food, Smoke, Soda, Beer, Toys, Fun, Books, Hshld, Clths, Paper, Util, Oil, Coal, Mines, Gold
2. Sector 2: Healthcare (3 industries)
    - Hlth, MedEq, Drugs
3. Sector 3: Financial Services (4 industries)
    - Fin, RlEst, Insur, Banks
4. Sector 4: Service Industry (5 industries)
    - Meals, Rtail, Whlsl, BusSv, PerSv
5. Sector 5: Industrial Sector (17 industries)
    - Trans, Boxes, LabEq, Ships, Aero, Autos, ElcEq, Mach, FabPr, Steel, Cnstr, BldMt, Txtls, Rubbr, Chems, Other, Guns 
6. Sector 6: Tech (3 industries)
    - Chips, Comps, Telcm

Absolute views are taken for each sectors where industries under the same sector share the same views uniformity:
1. Sector 1 Commodities: Bearish (2% yearly growth; 30% confidence)

2. Sector 2 Healthcare: Bullish (15% yearly growth; 65% confidence)

3. Sector 3 Financial Services: Bullish (12% yearly growth; 60% confidence)

4. Sector 4 Services: Bearish (2% yearly growth; 30% confidence)

5. Sector 5 Industrial: Bearish (3% yearly growth; 30% confidence)

6. Sector 6 Tech: Bullish (15% yearly growth; 65% confidence)

To build the Black Litterman model, here's what I need:
1. Covariance Matrix (No Shrinkage applied)

2. Implied Equilibrium Returns
    - Market Capitalisation: Proxied by calculating it as each industry column sum total return, divided by grand overall 48 industry total returns

    - Risk Aversion: Proxied by sumproduct of market capitalization and mean industry returns, divided by the portfolio variance

3. Views and confidence of each industry (See above for absolute views for each sector)

Since Black Litterman may introduce some shorting for different industries, I have also created constraints to add no shorting rule for Black Litterman Portfolio as well. 
