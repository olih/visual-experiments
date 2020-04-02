module Experiment.Brush.Editor.Dialect.RangeContent exposing (RangeContent, fromSection, setRanges, asRangesIn, getRangeParam, setValues, view)

import Experiment.Brush.Editor.Dialect.Content as Content exposing (Content)
import Experiment.Brush.Editor.Dialect.Section exposing (Section)
import Experiment.Brush.Editor.Dialect.RangeParam as RangeParam exposing (RangeParam)
import Experiment.Brush.Editor.Dialect.RangeParamId exposing (RangeParamId)
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

setRanges: Content RangeParam -> RangeContent -> RangeContent
setRanges ranges content =
    { content | ranges = ranges }

asRangesIn: RangeContent -> Content RangeParam -> RangeContent
asRangesIn content ranges =
    { content | ranges = ranges }


setValues : List RangeParam -> RangeContent -> RangeContent
setValues values content =
    Content.setValues values (RangeParam.toStringList values) content.ranges |> asRangesIn content

getRangeParam: RangeParamId -> RangeContent -> Maybe RangeParam
getRangeParam id content =
    content.ranges.values 
    |> List.filter (\range -> range.id == id)
    |> List.head

view : RangeContent -> Html Msg
view rgContent =
    rgContent.ranges.values
    |> List.map RangeParam.view 
    |> div [Attr.class ""]