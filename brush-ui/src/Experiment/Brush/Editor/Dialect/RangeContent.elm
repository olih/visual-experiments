module Experiment.Brush.Editor.Dialect.RangeContent exposing (RangeContent, fromSection)

import Experiment.Brush.Editor.Dialect.Content as Content exposing (Content)
import Experiment.Brush.Editor.Dialect.Section exposing (Section)
import Experiment.Brush.Editor.Dialect.RangeParam as RangeParam exposing (RangeParam)

type alias RangeContent =
    { 
        section: Section
        , ranges: Content RangeParam
    }

fromSection: Section -> RangeContent
fromSection section =
    RangeContent section (RangeParam.fromStringList section.lines |> Content.toContent)