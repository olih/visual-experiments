module Experiment.Brush.Editor.Dialect.PixelSqDim exposing (fromFraction)

import Experiment.Brush.Editor.Dialect.Fraction exposing (Fraction)

fromFraction: Int -> Fraction -> Int
fromFraction dim fraction =
    (dim * fraction.numerator) // fraction.denominator

