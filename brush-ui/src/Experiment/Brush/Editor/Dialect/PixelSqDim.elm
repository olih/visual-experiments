module Experiment.Brush.Editor.Dialect.PixelSqDim exposing (fromFraction)

import Experiment.Brush.Editor.Dialect.Fraction exposing (Fraction)

fromFraction: Float -> Fraction -> Float
fromFraction dim fraction =
    (dim * toFloat fraction.numerator) / toFloat fraction.denominator

