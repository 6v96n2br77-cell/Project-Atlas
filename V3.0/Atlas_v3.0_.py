import random
#Dictionaries and Markov Chain Business Cycle Model
nova={"name":"Nova","objective":"Profit Maximisation","price":1400,"quality":9,"brand":9,"sales":0,"revenue":0,"market_share":0,"costs":0, "profit":0, "previous_profit":0, "previous_revenue":0, "previous_market_share":0}
vertex={"name":"Vertex","objective":"Revenue Maximisation","price":900,"quality":8.5,"brand":7,"sales":0,"revenue":0,"market_share":0,"costs":0, "profit":0, "previous_profit":0, "previous_revenue":0, "previous_market_share":0}
pulse={"name":"Pulse","objective":"Business Growth","price":600,"quality":6,"brand":5,"sales":0,"revenue":0,"market_share":0,"costs":0, "profit":0, "previous_profit":0, "previous_revenue":0, "previous_market_share":0}
firms=[nova, vertex, pulse]
economy={"state": "","cycle_position":0,"inflation": 0.02,"inflation_target":0.02,"interest_rate":0.03,"desired_interest_rate":0.03,"gdp": 1000000000,"rgdp": 0.03,"consumer_confidence":0.75,"target_confidence":0.75,"year":1}
cycle_transitions={-2:{-2:0.45,-1:0.30,0:0.25},-1:{-2:0.25,-1:0.25,0:0.50},0:{-1:0.15,0:0.45,1:0.40},1:{-1:0.20,0:0.20,1:0.40,2:0.20},2:{1:0.60,2:0.30,-1:0.10}}
#Business Cycle Function
def update_business_cycle(economy):
    current_position=economy["cycle_position"]
    possible_states=cycle_transitions[current_position]
    random_number=random.random()
    cumulative_probability=0
    for state, probability in possible_states.items():
        cumulative_probability+=probability
        if random_number<=cumulative_probability:
            economy["cycle_position"]=state
            break
#RGDP (Growth) Function    
def update_rgdp(economy):
    if economy["state"]=="Boom":
        economy["rgdp"]+=random.uniform(0.005,0.015)
    elif economy["state"]=="Expansion":
        economy["rgdp"]+=random.uniform(0.001,0.008)
    elif economy["state"]=="Stable":
        economy["rgdp"]+=random.uniform(-0.003,0.003)
    elif economy["state"]=="Slowdown":
        economy["rgdp"]+=random.uniform(-0.008,-0.002)
    elif economy["state"]=="Recession":
        economy["rgdp"]+=random.uniform(-0.02,-0.005)
    interest_drag=(economy["interest_rate"]-0.03)*0.5
    economy["rgdp"]-=interest_drag
    economy["rgdp"]+=(0.03-economy["rgdp"])*0.1
    economy["rgdp"]=max(-0.08,min(economy["rgdp"],0.08))
#Economic Status Function  
def determine_economic_state(economy):
    states = {-2: "Recession",-1: "Slowdown",0: "Stable",1: "Expansion",2: "Boom"}
    economy["state"] = states[economy["cycle_position"]]
#Inflation Function 
def update_inflation(economy):
    inflation_pressure=economy["rgdp"]-0.03
    inflation_adjustment=inflation_pressure*0.2
    inflation_return=(economy["inflation_target"]-economy["inflation"])*0.15
    shock = random.uniform(-0.002,0.002)
    economy["inflation"]+=(inflation_adjustment+inflation_return+shock)
    economy["inflation"]=max(-0.02,min(economy["inflation"],0.15))
#Interest Rate Determinant Function
def determine_interest_rate_target(economy):
    target=0.03
    if economy["inflation"]>economy["inflation_target"]:
        target+=(economy["inflation"]-economy["inflation_target"])*1.75
    if economy["rgdp"]<0:
        target-=0.01
    economy["desired_interest_rate"]=max(0,min(target,0.12))
#Interest Rate Function   
def update_interest_rate(economy):
    economy["interest_rate"]+=(economy["desired_interest_rate"]-economy["interest_rate"])*0.2
#Consumer Confidence Function
def update_consumer_confidence(economy):
    change = 0
    if economy["cycle_position"]==2:
        change+=0.01
    elif economy["cycle_position"]==1:
        change+=0.005
    elif economy["cycle_position"]==-1:
        change-=0.01
    elif economy["cycle_position"]==-2:
        change-=0.02
    change -= max(0, economy["interest_rate"]-0.05)*0.25
    change+=(economy["target_confidence"]-economy["consumer_confidence"])*0.1
    economy["consumer_confidence"]+=change
    economy["consumer_confidence"]=max(0.2,min(economy["consumer_confidence"],1))
#Macro Variable Function
def update_economic_variables(economy):
    update_rgdp(economy)
    update_inflation(economy)
    determine_interest_rate_target(economy)
    update_interest_rate(economy)
    update_consumer_confidence(economy)
    economy["gdp"] *= (1 + economy["rgdp"])
#Macro Function    
def update_economy(economy):
    update_business_cycle(economy)
    determine_economic_state(economy)
    update_economic_variables(economy)
    economy["year"]+=1
#Utility Function
def calculate_utility(price, quality, brand, price_weight, quality_weight, brand_weight):
            price_score=20-(price/100)
            price_utility=price_score*price_weight
            quality_score=quality
            quality_utility=quality_score*quality_weight
            brand_score=brand
            brand_utility=brand_score*brand_weight
            return price_utility+quality_utility+brand_utility
#Borrowing Propensity Function
def calculate_borrowing_propensity(consumer,economy):
    propensity=0.5
    propensity+=(economy["consumer_confidence"]-0.75)
    propensity-=(economy["interest_rate"]-0.03)*3
    if consumer["income"]>60000:
        propensity+=0.1
    elif consumer["income"]<30000:
        propensity-=0.1
    return max(0,min(propensity,1))
#Affordability Function
def calculate_affordability(price, consumer):
    if price<=consumer["income"]:
        return 1
    else:
        borrowing_needed=price-consumer["income"]
        affordability=1-(borrowing_needed/price)
        affordability*=consumer["borrowing_propensity"]
        return max(0,affordability)
#Simulation Loop
yearly_results=[]
for year in range(1,11):
    update_economy(economy)
    for firm in firms:
        firm["sales"]=0
    #Consumer Count Calculation
    consumers=[]
    base_consumers=1000
    confidence_multiplier=economy["consumer_confidence"]/0.75
    interest_multiplier=1-((economy["interest_rate"]-0.03)*5)
    inflation_multiplier=1-max(0,economy["inflation"]-0.02)*3
    growth_multiplier=1+(economy["rgdp"]-0.03)*4
    consumer_count=int(base_consumers*confidence_multiplier*interest_multiplier*inflation_multiplier*growth_multiplier)
    consumer_count+=random.randint(-100,100)
    consumer_count=max(300,min(1800,consumer_count))
    #Consumer Loop
    for consumer in range(consumer_count):
        #Consumer Income
        consumer={"income":random.randint(15000,100000)}
        consumer["borrowing_propensity"]=calculate_borrowing_propensity(consumer,economy)
        if economy["state"]=="Boom":
            consumer["income"]*=1.15
        elif economy["state"]=="Expansion":
            consumer["income"]*=1.05
        elif economy["state"]=="Slowdown":
            consumer["income"]*=0.95
        elif economy["state"]=="Recession":
            consumer["income"]*=0.85
        #Consumer Preference Weighting
        price_weight=random.random()
        quality_weight=random.random()
        brand_weight=random.random()
        if consumer["income"]<40000:
            price_weight+=0.3
        elif consumer["income"]<50000:
            price_weight+=0.2
        elif consumer ["income"]<60000:
            price_weight+=0.1
        elif consumer["income"]<80000:
            quality_weight+=0.2
            brand_weight+=0.2
        else:
            quality_weight+=0.2
            brand_weight+=0.2
        total=price_weight+quality_weight+brand_weight
        price_weight=price_weight/total
        quality_weight=quality_weight/total
        brand_weight=brand_weight/total
        consumer["price_weight"]=price_weight
        consumer["quality_weight"]=quality_weight
        consumer["brand_weight"]=brand_weight
        maximum_budget=consumer["income"]*0.02
        #Individual Firm Utility Calculation and Selection
        nova_utility=calculate_utility(nova["price"],nova["quality"],nova["brand"],price_weight,quality_weight,brand_weight)
        vertex_utility=calculate_utility(vertex["price"],vertex["quality"],vertex["brand"],price_weight,quality_weight,brand_weight)
        pulse_utility=calculate_utility(pulse["price"],pulse["quality"],pulse["brand"],price_weight,quality_weight,brand_weight)
        affordability=calculate_affordability(firm["price"],consumer)
        nova_utility*=affordability
        vertex_utility*=affordability
        pulse_utility*=affordability
        if nova_utility>vertex_utility and nova_utility>pulse_utility and nova["price"]<=maximum_budget:
            nova["sales"]+=1
            consumer["choice"]="Nova"
            consumer["utility"]=nova_utility
            consumers.append(consumer)
        elif vertex_utility>nova_utility and vertex_utility>pulse_utility and vertex["price"]<=maximum_budget:
            vertex["sales"]+=1
            consumer["choice"]="Vertex"
            consumer["utility"]=vertex_utility
            consumers.append(consumer)
        elif pulse_utility>vertex_utility and pulse_utility>nova_utility and pulse["price"]<=maximum_budget:
            pulse["sales"]+=1
            consumer["choice"]="Pulse"
            consumer["utility"]=pulse_utility
            consumers.append(consumer)
    #Annual Data Analytics     
    print("")
    print("ATLAS MARKET RESULTS",year+2026)
    print("")
    print("Macroeconomic Status:",economy["state"])
    print("Economic Growth:",round(economy["rgdp"]*100,2),"%")
    print("Inflation:",round(economy["inflation"]*100,2),"%")
    print("Interest Rate:",round(economy["interest_rate"]*100,2),"%")
    print("Consumer Count:",len(consumers))
    print("")
    for firm in firms:
        firm["revenue"]=firm["sales"]*firm["price"]
        firm["market_share"]=(firm["sales"]/len(consumers))*100
        print(firm["name"])
        print("Business Objective:",firm["objective"])
        print("Total Sales(annum):", firm["sales"])
        print("Market Share:", round(firm["market_share"], 2), "%")
        print("Total Revenue (annum): £", firm["revenue"])
        #Effect of Rising Marginal Costs and Inflation (Supply Constraints)
        firm["cost_per_unit"]=200+(firm["quality"]*50)
        if firm["sales"]>200:
            firm["cost_per_unit"]*=1.05
        if firm["sales"]>400:
            firm["cost_per_unit"]*=1.10
        if firm["sales"]>600:
            firm["cost_per_unit"]*=1.15
        firm["cost_per_unit"]*=(1+economy["inflation"])
        firm["costs"]=firm["sales"]*firm["cost_per_unit"]
        firm["profit"]=firm["revenue"]-firm["costs"]
        print("Total Costs (annum): £",round(firm["costs"], 2))
        print("Total Profit (annum): £",round(firm["profit"], 2))
        print("")
    #Price and Non-Price Competition
    if nova["profit"]<nova["previous_profit"]:
        nova["quality"]=min(nova["quality"]+0.2,10)
    elif nova["profit"]>nova["previous_profit"]:
        nova["price"]=min(nova["price"]+40,1500)
    if vertex["revenue"]<vertex["previous_revenue"]:
        vertex["brand"]=min(vertex["brand"]+0.2,9)
    elif vertex["revenue"]>vertex["previous_revenue"]:
        vertex["price"]=min(vertex["price"]+20,1000)
    if pulse["market_share"]<pulse["previous_market_share"]:
        pulse["price"]=max(pulse["price"]-25,500)
    elif pulse["market_share"]>pulse["previous_market_share"]:
        pulse["price"]=min(pulse["price"]+20,750)
    for firm in firms:
        firm["previous_profit"]=firm["profit"]
        firm["previous_revenue"]=firm["revenue"]
        firm["previous_market_share"]=firm["market_share"]
    year_result = {"year": year,"nova_sales": nova["sales"],"nova_revenue": nova["revenue"],"nova_profit": nova["profit"],"nova_market_share": nova["market_share"], "nova_costs": nova["costs"], "nova_sales": nova["sales"], "vertex_sales": vertex["sales"], "vertex_revenue": vertex["revenue"],"vertex_profit": vertex["profit"],"vertex_market_share": vertex["market_share"], "vertex_costs": vertex["costs"], "vertex_sales": vertex["sales"], "pulse_sales": pulse["sales"], "pulse_revenue": pulse["revenue"],"pulse_profit": pulse["profit"],"pulse_market_share": pulse["market_share"], "pulse_costs": pulse["costs"], "pulse_sales": pulse["sales"],"consumer_list":len(consumers), "rgdp":economy["rgdp"]*100, "inflation":economy["inflation"]*100, "interest_rate":economy["interest_rate"]*100}
    yearly_results.append(year_result)
#Total Consumers Calculation
total_consumers=sum(year["consumer_list"]for year in yearly_results)
#Total Profit Calculation
total_nova_profit=sum(year["nova_profit"]for year in yearly_results)
total_vertex_profit = sum(year["vertex_profit"] for year in yearly_results)
total_pulse_profit = sum(year["pulse_profit"] for year in yearly_results)
#Total Revenue Calculation
total_nova_revenue=sum(year["nova_revenue"]for year in yearly_results)
total_vertex_revenue=sum(year["vertex_revenue"]for year in yearly_results)
total_pulse_revenue=sum(year["pulse_revenue"]for year in yearly_results)
#Total Costs Calculation
total_nova_costs=sum(year["nova_costs"]for year in yearly_results)
total_vertex_costs=sum(year["vertex_costs"]for year in yearly_results)
total_pulse_costs=sum(year["pulse_costs"]for year in yearly_results)
#Total Sales Calculation
total_nova_sales=sum(year["nova_sales"]for year in yearly_results)
total_vertex_sales=sum(year["vertex_sales"]for year in yearly_results)
total_pulse_sales=sum(year["pulse_sales"]for year in yearly_results)
#Average Consumer Income Calculation
total_income=0
for consumer in consumers:
    total_income+=consumer["income"]
average_income=total_income/len(consumers)
#Nova Consumer Analytics
nova_income=0
nova_buyers=0
for consumer in consumers:
    if consumer["choice"]=="Nova":
        nova_income+=consumer["income"]
        nova_buyers+=1
nova_average_income=nova_income/nova_buyers
nova_difference = ((nova_average_income - average_income) / average_income) * 100
#Vertex Consumer Analytics
vertex_income=0
vertex_buyers=0
for consumer in consumers:
    if consumer["choice"]=="Vertex":
        vertex_income+=consumer["income"]
        vertex_buyers+=1
vertex_average_income=vertex_income/vertex_buyers
vertex_difference = ((vertex_average_income - average_income) / average_income) * 100
#Pulse Consumer Analytics
pulse_income=0
pulse_buyers=0
for consumer in consumers:
    if consumer["choice"]=="Pulse":
        pulse_income+=consumer["income"]
        pulse_buyers+=1
pulse_average_income=pulse_income/pulse_buyers
pulse_difference = ((pulse_average_income - average_income) / average_income) * 100
#Overall Market Summary
print("")
print("===== 10 YEAR MARKET SUMMARY =====")
print("")
print("Nova Total Profit: £", round(total_nova_profit,2))
print("Nova Total Revenue: £", round(total_nova_revenue,2))
print("Nova Total Costs: £", round(total_nova_costs,2))
print("Nova Total Sales:", round(total_nova_sales,2))
print("")
print("Vertex Total Profit: £", round(total_vertex_profit,2))
print("Vertex Total Revenue: £", round(total_vertex_revenue,2))
print("Vertex Total Costs: £", round(total_vertex_costs,2))
print("Vertex Total Sales:", round(total_vertex_sales,2))
print("")
print("Pulse Total Profit: £", round(total_pulse_profit,2))
print("Pulse Total Revenue: £", round(total_pulse_revenue,2))
print("Pulse Total Costs: £", round(total_pulse_costs,2))
print("Pulse Total Sales:", round(total_pulse_sales,2))
#Overall Market Analytics
print("")
print("===== MARKET ANALYSIS =====")
print("")
print("Total Consumer Count:",total_consumers)
print("Average Consumer Income: £", round(average_income, 2))
print("Average Nova Consumer Income: £", round(nova_average_income, 2),
      f"({nova_difference:+.2f}% vs Market Average)")
print("Average Vertex Consumer Income: £", round(vertex_average_income, 2),
      f"({vertex_difference:+.2f}% vs Market Average)")
print("Average Pulse Consumer Income: £", round(pulse_average_income, 2),
      f"({pulse_difference:+.2f}% vs Market Average)")

import matplotlib.pyplot as plt
#Macro Graph
macro_years=[]
rgdps=[]
inflations=[]
interest_rates=[]

for result in yearly_results:
    macro_years.append(result["year"])
    rgdps.append(result["rgdp"])
    inflations.append(result["inflation"])
    interest_rates.append(result["interest_rate"])
      
plt.figure(figsize=(8,5))
plt.plot(macro_years, rgdps, label="RGDP")
plt.plot(macro_years, inflations, label="Inflation")
plt.plot(macro_years, interest_rates, label="Interest Rate")
plt.xlabel("Year")
plt.ylabel("Percentage Points (%)")
plt.title("Macroeconomic Variables in Atlas Over Time")
plt.legend()
#Profit Graph
profit_years = []
nova_profits = []
vertex_profits = []
pulse_profits = []

for result in yearly_results:
    profit_years.append(result["year"])
    nova_profits.append(result["nova_profit"])
    vertex_profits.append(result["vertex_profit"])
    pulse_profits.append(result["pulse_profit"])
    
plt.figure(figsize=(8,5))
plt.plot(profit_years, nova_profits, label="Nova")
plt.plot(profit_years, vertex_profits, label="Vertex")
plt.plot(profit_years, pulse_profits, label="Pulse")
plt.xlabel("Year")
plt.ylabel("Profit (£)")
plt.title("Atlas Firm Profit Over Time")
plt.legend()
#Market Share Graph
market_years=[]
nova_market_shares = []
vertex_market_shares = []
pulse_market_shares = []

for result in yearly_results:
    market_years.append(result["year"])
    nova_market_shares.append(result["nova_market_share"])
    vertex_market_shares.append(result["vertex_market_share"])
    pulse_market_shares.append(result["pulse_market_share"])
    
plt.figure(figsize=(8,5))
plt.plot(market_years, nova_market_shares, label="Nova")
plt.plot(market_years, vertex_market_shares, label="Vertex")
plt.plot(market_years, pulse_market_shares, label="Pulse")
plt.xlabel("Year")
plt.ylabel("Market Share (%)")
plt.title("Atlas Firm Market Share Over Time")
plt.legend()
#Revenue Graph
revenue_years=[]
nova_revenues = []
vertex_revenues = []
pulse_revenues = []

for result in yearly_results:
    revenue_years.append(result["year"])
    nova_revenues.append(result["nova_revenue"])
    vertex_revenues.append(result["vertex_revenue"])
    pulse_revenues.append(result["pulse_revenue"])
    
plt.figure(figsize=(8,5))
plt.plot(revenue_years, nova_revenues, label="Nova")
plt.plot(revenue_years, vertex_revenues, label="Vertex")
plt.plot(revenue_years, pulse_revenues, label="Pulse")
plt.xlabel("Year")
plt.ylabel("Revenue (£)")
plt.title("Atlas Firm Revenue Over Time")
plt.legend()
#Cost Graph
cost_years=[]
nova_cost = []
vertex_cost = []
pulse_cost = []

for result in yearly_results:
    cost_years.append(result["year"])
    nova_cost.append(result["nova_costs"])
    vertex_cost.append(result["vertex_costs"])
    pulse_cost.append(result["pulse_costs"])
    
plt.figure(figsize=(8,5))
plt.plot(cost_years, nova_cost, label="Nova")
plt.plot(cost_years, vertex_cost, label="Vertex")
plt.plot(cost_years, pulse_cost, label="Pulse")
plt.xlabel("Year")
plt.ylabel("Costs (£)")
plt.title("Atlas Firm Costs Over Time")
plt.legend()

plt.show()
