module Experiment.Brush.Editor.MultiContent exposing (MultiContent, reset)

import Experiment.Brush.Editor.Item.MediaItem exposing(MediaItem)
import Experiment.Brush.Editor.Settings.RangeParam exposing(RangeParam)
import Experiment.Brush.Editor.Settings.Failing exposing (Failure)

type alias MultiContent = {
    lines: List String
    , mediaItems : List MediaItem
    , rangeSettings: List RangeParam
    , failures: List Failure
    }

reset: MultiContent
reset = {
    lines =[]
    , mediaItems = []
    , rangeSettings = []
    , failures = []
    }

createMediaItems: List String -> List MediaItem
createMediaItems lines =
    []

createRangeSettings: List String -> List RangeParam
createRangeSettings lines =
    []

createFailures: List String -> List Failure
createFailures lines =
    []

updateLines: List String -> MultiContent -> MultiContent
updateLines lines multiContent =
    { multiContent 
    | lines = lines
    , mediaItems = createMediaItems lines
    , rangeSettings = createRangeSettings lines
    , failures = createFailures lines
    }

