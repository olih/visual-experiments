module Experiment.Brush.Editor.Applicative exposing(reset)

import Experiment.Brush.Editor.Dialect.Section exposing (Section)
import Experiment.Brush.Editor.Dialect.BrushContent exposing (BrushContent)
import Experiment.Brush.Editor.Dialect.BrushStrokeContent exposing (BrushStrokeContent)
import Experiment.Brush.Editor.Dialect.RangeContent exposing (RangeContent)
import Experiment.Brush.Editor.Dialect.Failing as Failing exposing (Failure)
import Experiment.Brush.Editor.Dialect.SectionList as SectionList
import Experiment.Brush.Editor.Dialect.Identifier exposing (Identifier)
type alias Model =
    {   idx: Maybe Identifier
        , generation: Maybe Identifier
        , latestGeneration: Maybe Identifier
        , showTrash: Bool
        , sections: List Section
        , maybeBrushContent: Maybe BrushContent
        , maybeRangeContent: Maybe RangeContent
        , maybeBrushStrokeContent: Maybe BrushStrokeContent
        , failures : List Failure
    }

reset: Model
reset = {
        idx = Nothing
        , generation = Nothing
        , latestGeneration = Nothing
        , showTrash = False
        , sections = []
        , maybeBrushContent = Nothing
        , maybeRangeContent = Nothing
        , maybeBrushStrokeContent = Nothing
        , failures = []
    }

fromString: String -> Model -> Model
fromString content =
    let
        sections = SectionList.fromString content
    in
    