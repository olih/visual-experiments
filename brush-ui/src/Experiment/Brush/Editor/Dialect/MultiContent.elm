module Experiment.Brush.Editor.Dialect.MultiContent exposing (MultiContent, reset, fromStringList, toStringList)

import Parser exposing(run)
import Experiment.Brush.Editor.Dialect.MediaItem as MediaItem exposing(MediaItem)
import Experiment.Brush.Editor.Dialect.RangeParam as RangeParam exposing(RangeParam)
import Experiment.Brush.Editor.Dialect.Failing as Failing exposing (FailureKind(..), Failure)

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

parseInvalidMediaItem: String -> Maybe Failure
parseInvalidMediaItem line =
    case run MediaItem.parser line of
        Ok _ ->
            Nothing

        Err msg ->
            if line |> String.startsWith "ID " then
                Failing.fromDeadEndList msg line |> Just
            else
                Nothing

parseInvalidRangeParam: String -> Maybe Failure
parseInvalidRangeParam line =
    case run RangeParam.parser line of
        Ok _ ->
            Nothing

        Err msg ->
            if line |> String.startsWith "SETTINGS RANGE " then
                Failing.fromDeadEndList msg line |> Just
            else
                Nothing
createMediaItems: List String -> List MediaItem
createMediaItems lines =
    List.filterMap parseMediaItem lines

createRangeSettings: List String -> List RangeParam
createRangeSettings lines =
    List.filterMap parseRangeParam lines


createFailures: List String -> List Failure
createFailures lines =
   List.filterMap parseInvalidMediaItem lines
   ++ List.filterMap parseInvalidRangeParam lines

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
