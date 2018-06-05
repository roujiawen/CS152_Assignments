
% Write your Prolog rules here


type("italian") :- type("western").
type("american") :- type("western").
type("mexican") :- type("western").

type("japanese") :- type("asian").
type("korean") :- type("asian").
type("chinese") :- type("asian").

type("chicken") :- type("korean"); type("american").
type("bbq") :- type("korean").

suggestion(rest1) :- type("chinese"), price("_1"), distance(X), X > 1.7, english(no), open_late(no), not(diet("vegan")), not(diet("gluten free")), not(diet("halal")).

suggestion(rest2) :- type("bbq"), price("_2"), distance(X), X > 2.4, english(no), take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest3) :- type("japanese"), price("_2"), distance(X), X > 1.9, take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest4) :- type("korean"), price("_2"), distance(X), X > 0.7, take_out(no), not(diet("halal")).

suggestion(rest5) :- type("american"), price("_1"), distance(X), X > 1, not(diet("vegetarian")), not(diet("vegan")), not(diet("gluten free")), not(diet("halal")).

suggestion(rest6) :- type("korean"), price("_2"), distance(X), X > 2.2, english(no), take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest7) :- type("bbq"), price("_2"), distance(X), X > 1.4, english(no), take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest8) :- type("bbq"), price("_2"), distance(X), X > 0.5, english(no), take_out(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest9) :- type("japanese"), price("_2"), distance(X), X > 1.7, open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest10) :- type("bbq"), price("_2"), distance(X), X > 1.5, open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest11) :- type("korean"), price("_2"), distance(X), X > 1.4, not(diet("halal")).

suggestion(rest12) :- type("bbq"), price("_2"), distance(X), X > 2, english(no), take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest13) :- type("western"), price("_3"), distance(X), X > 1.8, take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest14) :- type("western"), price("_1"), distance(X), X > 1.7, open_late(no), not(diet("vegan")), not(diet("gluten free")), not(diet("halal")).

suggestion(rest15) :- type("korean"), price("_1"), distance(X), X > 1.6, english(no), take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest16) :- type("western"), price("_2"), distance(X), X > 1.3, open_late(no), not(diet("vegan")), not(diet("gluten free")), not(diet("halal")).

suggestion(rest17) :- type("korean"), price("_1"), distance(X), X > 2.3, english(no), take_out(no), open_late(no), not(diet("vegan")), not(diet("halal")).

suggestion(rest18) :- type("japanese"), price("_2"), distance(X), X > 2.5, english(no), take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest19) :- type("japanese"), price("_2"), distance(X), X > 1.9, english(no), take_out(no), not(diet("vegan")), not(diet("halal")).

suggestion(rest20) :- type("bbq"), price("_2"), distance(X), X > 2.3, take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest21) :- type("japanese"), price("_2"), distance(X), X > 0.2, take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest22) :- type("japanese"), price("_2"), distance(X), X > 1.3, english(no), take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest23) :- type("american"), price("_3"), distance(X), X > 1.2, not(diet("vegan")), not(diet("gluten free")), not(diet("halal")).

suggestion(rest24) :- type("korean"), price("_2"), distance(X), X > 1.7, english(no), take_out(no), open_late(no), not(diet("halal")).

suggestion(rest25) :- type("italian"), price("_2"), distance(X), X > 2, open_late(no), not(diet("vegan")), not(diet("gluten free")), not(diet("halal")).

suggestion(rest26) :- type("korean"), price("_2"), distance(X), X > 1.8, english(no), take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("halal")).

suggestion(rest27) :- type("italian"), price("_2"), distance(X), X > 2.4, take_out(no), open_late(no), not(diet("vegan")), not(diet("gluten free")), not(diet("halal")).

suggestion(rest28) :- type("western"), price("_1"), distance(X), X > 2.6, take_out(no), open_late(no), not(diet("vegetarian")), not(diet("vegan")), not(diet("gluten free")), not(diet("halal")).

suggestion(rest29) :- type("italian"), price("_2"), distance(X), X > 2.2, take_out(no), open_late(no), not(diet("vegan")), not(diet("gluten free")), not(diet("halal")).

suggestion(rest30) :- type("asian"), price("_1"), distance(X), X > 2, take_out(no), open_late(no), not(diet("vegan")), not(diet("gluten free")), not(diet("halal")).

:- discontiguous type/1.
:- discontiguous diet/1.

take_out(X) :- known(yes, take_out, X).
distance(X) :- known(yes, distance, X).
type(X) :- known(yes, type, X).
price(X) :- known(yes, price, X).
english(X) :- known(yes, english, X).
open_late(X) :- known(yes, open_late, X).
diet(X) :- known(yes, diet, X).
