module App exposing (Model, reset, Msg(..), toggleTag, setGroupInfo)
import Http
import GroupInfo as GroupInfo
type alias Model =
    { 
        groupInfo: GroupInfo.Model
        , tags : List String
    }

reset: Model
reset = {
    groupInfo = GroupInfo.reset
    , tags = []
 }

type Msg
  = GotGroupInfo (Result Http.Error String)
  | ToggleTag String

toggleTag: String -> Model -> Model
toggleTag tag model =
    model

setGroupInfo: GroupInfo.Model -> Model -> Model
setGroupInfo groupInfo model =
    { model | groupInfo = groupInfo}