# Lessons from creating tortuga

## Parameters

* Changing the sign for the angle produces zigzags and a less dense drawing
  * Looks like mountains most likely because branches are limited to one or two

* With no change of sign, 2 to 4 branches looks like algae

* Sticking to a single variable seems to produce better specimens.

* Crossover creates curious patterns with segmented styles.

## Metrics

* Average svg file: 45kb
* Manually selected 208 out of 3084 thus 6.7%
* Crossover kept automatically 171 files out of 3000 thus 5.7%.
* All in all, only 0.4% of all files are kept.
* SVG takes half a second to be saved

## Codewise

* Prototyping helps to find a direction but the complexity of the problem requires to create reliable unit tested code to build upon.
* SVG is powerful but by default the transform property add a translation to a rotation or scaling. I don't think this is intuitive and quite difficult to understand how to cancel this side effect. In the end, it was easier to rewrite the rotation or scaling of the pathrather to use svg symbol.
* typing package is great addition to the python language as it makes the code much more readable and predictable.
* Fractions are acually supported out of the box in python. Awesome.
* The uses of fractions has pros and cons. They are good to start with but it quicky becomes apparent that sin, cos, square root and other geometric functions would produce quite complex and only approximate fractions. If choosen from a list, they are more readable but after a few additions and multiplications they become difficult to read. Floats would work every time but are less readable for value under 1 most of the time. Still unsure about best approach.
* random package is very useful and has some very good insights about statistics by [Peter Norvig](https://nbviewer.jupyter.org/url/norvig.com/ipython/Economics.ipynb)
* sets are very useful for tagging.
* Many thanks to Dr Aradhna Kaushal for introducing me to [Pearson product-moment correlation coefficients](https://numpy.org/doc/stable/reference/generated/numpy.corrcoef.html) which are a useful approach for checking how scattered the points are.
* Reading json as dict is error prone, and difficult to get an understanding of the schema. Better to use a class to do so.
* Externalize configuration parameters to a json file was very hepful in delaying decisions about what should be the best parameter for a given situation.


## Links
* [On generative algorithms by Anders Hoff](https://inconvergent.net/)
* [Generative design studio](https://n-e-r-v-o-u-s.com/)
* [Evolutionary art](https://en.wikipedia.org/wiki/Evolutionary_art)
* [rhino3d](https://developer.rhino3d.com/guides/rhinopython/primer-101/8-geometry/#81-the-opennurbs-kernel)
* [Ray tracing](https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-ray-tracing/implementing-the-raytracing-algorithm)
* [advanced/image_processing](https://scipy-lectures.org/advanced/image_processing/)
