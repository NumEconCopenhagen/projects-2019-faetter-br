# Dataproject
The data project aims at producing a forecast of danish socio-economic groups. This is done by importing register-based Labourforce Statistics (RAS) and a projection of the danish population from Statistics Denmark. These datasets contain population and frequencies of socio-economic groups on a multitude of subsets. These include the origin of the population, the age destribution and gender. This allows analysis of different aspects of the agegroups - do immigrants work more of less than danes? How about their decendants? Will immigration increase labour supply in Denmark in the future? Are elders' share of the population growing?

The imported datasets are initially non-compatiable with each other, as collumnn names and indexes for origin and age are different across datasets. As an example RAS' age collumn containes age intervals while the other datasets are using individual age categories. Lastly, we ensure a consistent namingscheme across datasets to ensure that origin and gender indexes are the same. We solve these compatibility issues in the first major block of our code called "data".

The second block is the "projection" of socio-economic groups. Prior to 2017, we simply compute the actual historical destribution of socio-economic groups, as we have knowledge of the frequencies in a historical perspective. To compute the destribution towards 2060, we simply hold frequencies of 2017 constant and multiply by the relevant population. This gives an estimate of how socio-groups develop across time  

The last part of the projection block presents some interesting results visually. First, we compute the contributer-fraction to show how the workforce is shrinking releative to the rest of the population. In 2008 roughtly 50 percent of the population partipated in the labourmarket, that is for every 1 person in the labourmarket there would be 1 outside. By 2060 for each 1 person in the labourmarket, 1.25 person will be outside. The last plot is meant to give an idea of how socio-economic groups are changing over time by dragging the slider. Most noticable is the increasing share of pensioners, which is the main driving force behind the increasing contributer-fraction.

To reproduce our results one should simply run the code bit by bit, nothing else is required. To see how socio-economic groups change over time in the last plot, drag the slider at the top of plot named "year".





