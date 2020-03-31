module Experiment.Brush.Editor.AppEvent exposing (Msg(..), processEvent)

import Experiment.Brush.Editor.Applicative as App
import Experiment.Brush.Editor.Dialect.RangeParamId exposing (RangeParamId)
import Http

type Msg = 
    OnNext
    | OnPrevious
    | OnFirst
    | OnLast
    | OnTrash
    | OnPreserve
    | OnSave
    | OnChangeParam RangeParamId String
    | GotText (Result Http.Error String)


processEvent: Msg -> App.Model -> App.Model
processEvent uiEvent appModel =
    appModel
