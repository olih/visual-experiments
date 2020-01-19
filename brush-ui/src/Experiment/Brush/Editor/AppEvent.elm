module Experiment.Brush.Editor.AppEvent exposing (UIEvent(..))

type UIEvent
    = OnLoad String
    | OnNext
    | OnPrevious
    | OnFirst
    | OnLast
    | OnTrash
    | OnPreserve

