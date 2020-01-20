module Experiment.Brush.Editor.Applicative exposing(reset)

import Experiment.Brush.Editor.Dialect.Section exposing (Section)
import Experiment.Brush.Editor.Dialect.BrushContent exposing (BrushContent)
import Experiment.Brush.Editor.Dialect.BrushStrokeContent exposing (BrushStrokeContent)
import Experiment.Brush.Editor.Dialect.RangeContent exposing (RangeContent)
type alias Model =
    {   idx: Int
        , generation: Int
        , showTrash: Bool
        , sections: List Section
        , maybeBrushContent: Maybe BrushContent
        , maybeRangeContent: Maybe RangeContent
        , maybeBrushStrokeContent: Maybe BrushStrokeContent
    }

reset: Model
reset = {
        idx = 0
        , generation = 0
        , showTrash = False
        , sections = []
        , maybeBrushContent = Nothing
        , maybeRangeContent = Nothing
        , maybeBrushStrokeContent = Nothing
    }
