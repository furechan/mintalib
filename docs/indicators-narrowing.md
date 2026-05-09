# Narrowing Indicators to Pandas Only

The idea is to make indccators pandas only. So we get indicatoes pandas only, expressions polares onle, core methods (cacl_*) numpy level, and functions polyvalent. Now functions and indicators share some utilties to convert to and from dataframes. We would need to split those so that functions and indicatoes have their own conversions utils. 

If I recall corectly we have things like dataframe_accessor, wrap_result, and maybe some other methods.

Also  belive these resdie in the core (cython) module, and i ma not sure they belong ethre.

Can you analyse?
