module Experiment.Brush.Editor.MultiContent exposing (MultiContent)

import Experiment.Brush.Editor.Item.MediaItem exposing(MediaItem)
import Experiment.Brush.Editor.Settings.RangeParam exposing(RangeParam)
type alias MultiContent = {
    mediaItems : List MediaItem
    , rangeSettings: List RangeParam
    }
