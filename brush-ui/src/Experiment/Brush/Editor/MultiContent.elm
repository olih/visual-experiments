module Experiment.Brush.Editor.MultiContent exposing (MultiContent, reset, fromStringList, toStringList)

import Parser exposing(run)
import Experiment.Brush.Editor.Item.MediaItem as MediaItem exposing(MediaItem)
import Experiment.Brush.Editor.Settings.RangeParam as RangeParam exposing(RangeParam)
import Experiment.Brush.Editor.Settings.Failing exposing (Failure)

type alias MultiContent = {
    mediaItems : List MediaItem
    , rangeSettings: List RangeParam
    , failures: List Failure
    }

reset: MultiContent
reset = {
    mediaItems = []
    , rangeSettings = []
    , failures = []
    }

parseMediaItem: String -> Maybe MediaItem
parseMediaItem line =
    run MediaItem.parser line |> Result.toMaybe

parseRangeParam: String -> Maybe RangeParam
parseRangeParam line =
    run RangeParam.parser line |> Result.toMaybe

createMediaItems: List String -> List MediaItem
createMediaItems lines =
    List.filterMap parseMediaItem lines

createRangeSettings: List String -> List RangeParam
createRangeSettings lines =
    List.filterMap parseRangeParam lines


createFailures: List String -> List Failure
createFailures lines =
    []

fromStringList: List String -> MultiContent
fromStringList lines =
    { mediaItems = createMediaItems lines
    , rangeSettings = createRangeSettings lines
    , failures = createFailures lines
    }

toStringList: MultiContent -> List String
toStringList content =
   List.map MediaItem.toString content.mediaItems
   ++ List.map RangeParam.toString content.rangeSettings
