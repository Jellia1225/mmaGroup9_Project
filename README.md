# mmaGroup9_Project

## Part I: Dataset Introduction ##
This project uses a dataset representing flights operated by Potter Airlines, an airline that has been considered to operate between major Canadian cities. The dataset contains 200 flights for the upcoming year 2027. The attribute values have been randomized in order to support the development and testing of the dynamic pricing model. 

### Dataset variables: ###
  flight_id : Unique identifier for each flight (e.g. PA101)
  origin : Departure city, selected randomly from a list of eight major Canadian cities
  destination : Arrival city, also selected randomly from the same list
  departure_date : Scheduled departure date, generated randomly for the year 2027
  base_fare : Base ticket fare before dynamic pricing adjustments, generated randomly within a realistic interval of $200-$800
  capacity : Total number of seats on the flight, generated randomly within an interval of 100-300 seats
  seats_remaining : Number of seats available for a given flight, generated randomly between 0-capacity
  route_demand : Randomized demand level for the flight, represented as a value between 0 and 1
  season : Indicates whether the flight takes place during a vacation season or a regular period
  is_weekend : Indicates whether the departure date of the flight falls on a weekend day.

The dataset is stored in "flights.csv" and is also represented in Python as a list of dictionaries. These dictionaries are then used to create "Flight" objects through the project's "Flight" class.

### Dataset assumptions: ###
1- The dataset contains 200 flights, all of which have a unique flight id.
2- The Canadian cities in the data are: Toronto, Vancouver, Montreal, Quebec City, Calgary, Edmonton, Ottawa, and Winnipeg.
  2.1- A flight cannot have the same origin and destination.
3- Each date within the selected period of 01-01-2027 and 31-12-2027 is assumed to be equally likely.
4- June, July, August, December, and January are classified as vacation periods, and all other months as regular periods. This assumption aims to capture periods in which leisure travel may be higher, and therefore, flight prices might increase.
5- Friday, Saturday, and Sunday are classified as weekend days, while Monday through Thursday are classified as weekdays.
6- The selected aircraft capacity range of 100-300 assumes to represent the different aircraft sizes that Potter Airlines may operate.
  6.1- The selected range is assumed to represent realistic aircraft capacities for national-level flights.
7- A flight's number of seats remaining can never exceed the aircraft's capacity.
8- The base fare interval of $200-$800 has been assumed to represent realistic Canadian national-level flight base fares.
9- The route demand attribute is treated as a continuous variable, where a value closer to 0 represents lower demand and a value closer to 1 represents higher demand.
10- The initial dataset generation treats most variables as independently randomized within their defined ranges.
  10.1- Relationships between attributes are later considered by the dynamic pricing model rather than being directly imposed. This allows for edge cases to arise (e.g. combinations of flights with little days until departure, low seats remaining, etc.) and be implemented and analyzed properly by the pricing model.

## Part II: Pricing Model ##
The pricing model calculates a dynamic ticket price for each flight by applying five pricing factors to the base fare. These factors include time to departure, route demand, flight capacity, travel season, and whether the flight is scheduled on a weekend.
The final adjusted fare is calculated as:

*Adjusted Fare = Base Fare × Time Factor × Demand Factor × Capacity Factor × Seasonal Factor × Weekend Factor*

### Pricing Factors ###
**Time Factor**: This factor is based on the number of days remaining before departure. The fare increases as the departure date gets closer and decreases when the flight is booked further in advance.

**Demand Factor**: The fare is adjusted based on the demand level of each route. Routes with higher demand have higher fares, while routes with lower demand have lower fares.

**Capacity Factor**: This factor uses the load factor of each flight. As more seats are occupied, the fare increases. Flights with more available seats have lower fares.

**Seasonal Factor**: The model considers whether the flight is during a vacation or regular travel period. Fares increase during vacation periods and remain at the regular level during non-vacation periods.

**Weekend Factor**: The model also considers whether the departure falls on a weekend. Weekend flights have higher fares to account for higher travel demand, while weekday flights do not receive this adjustment.

### Pricing Date ###
The model allows the user to enter a pricing date, which is used to calculate the number of days between the pricing date and the departure date. If the user does not enter a date, the model uses today's date as the default.

### Final Price###
After all pricing factors are applied, a minimum and maximum fare are used to keep the final prices within a reasonable range. The adjusted fare is limited between $200 and $800. The final output includes the original flight information, each pricing factor, and the adjusted fare. This allows us to compare the final prices across flights and understand how different factors affect the pricing results.

