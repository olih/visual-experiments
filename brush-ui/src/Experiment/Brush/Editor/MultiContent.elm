module Experiment.Brush.Editor.MultiContent exposing (MultiContent, reset)

import Experiment.Brush.Editor.Item.MediaItem exposing(MediaItem)
import Experiment.Brush.Editor.Settings.RangeParam exposing(RangeParam)
import Experiment.Brush.Editor.Settings.Failing exposing (Failure)

type alias MultiContent = {
    lines: List String
    , mediaItems : List MediaItem
    , mediaItemsIndexes: List (Int, Int)
    , rangeSettings: List RangeParam
    , failures: List Failure
    }

reset: MultiContent
reset = {
    lines =[]
    , mediaItems = []
    , mediaItemsIndexes = []
    , rangeSettings = []
    , failures = []
    }

createMediaItems: List String -> List MediaItem
createMediaItems lines =
    []
--TODO MediaItem or Failure vs List (Maybe MediaItem, Maybe Failure)

updateLines: List String -> MultiContent -> MultiContent
updateLines lines multiContent =
    { multiContent | lines = lines, mediaItems = createMediaItems lines}

