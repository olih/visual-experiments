module Experiment.Brush.Editor.Dialect.RangeContent exposing (RangeContent, fromSection, view)

import Experiment.Brush.Editor.Dialect.Content as Content exposing (Content)
import Experiment.Brush.Editor.Dialect.Section exposing (Section)
import Experiment.Brush.Editor.Dialect.RangeParam as RangeParam exposing (RangeParam)
import Html exposing (Html, div)
import Html.Attributes as Attr
import Experiment.Brush.Editor.AppEvent exposing (Msg(..))

type alias RangeContent =
    { 
        section: Section
        , ranges: Content RangeParam
    }

fromSection: Section -> RangeContent
fromSection section =
    RangeContent section (RangeParam.fromStringList section.lines |> Content.toContent)

view : RangeContent -> Html Msg
view rgContent =
    rgContent.ranges.values
    |> List.map RangeParam.view 
    |> div [Attr.class ""]