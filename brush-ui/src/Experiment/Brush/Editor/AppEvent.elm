module Experiment.Brush.Editor.AppEvent exposing (UIEvent(..), processEvent)

import Experiment.Brush.Editor.Applicative as App
type UIEvent = 
    OnNext
    | OnPrevious
    | OnFirst
    | OnLast
    | OnTrash
    | OnPreserve
    | OnSave


processEvent: UIEvent -> App.Model -> App.Model
processEvent uiEvent appModel =
    appModel
