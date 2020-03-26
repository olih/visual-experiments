module App exposing (Model, reset, Msg(..), setGroupInfo, setItems, setTag, filterByTag)
import Http
import GroupInfo as GroupInfo
import MediaFileInfo as MediaFileInfo
import Set
type alias Model =
    { 
        groupId: String
        , groupInfo: GroupInfo.Model
        , tag : String
        , items: List MediaFileInfo.Model
    }

reset: Model
reset = {
    groupId = "default"
    , groupInfo = GroupInfo.reset
    , tag = "2020"
    , items = []
 }

type Msg
  = GotGroupInfo (Result Http.Error String)
  | ToggleTag String

setTag: String -> Model -> Model
setTag tag model =
    { model | tag = tag}
setGroupInfo: GroupInfo.Model -> Model -> Model
setGroupInfo groupInfo model =
    { model | groupInfo = groupInfo}

setItems: List MediaFileInfo.Model -> Model -> Model
setItems items model =
    { model | items = items}

filterByTag: Model -> Model
filterByTag model =
    { model | items = List.filter (\item -> Set.member model.tag item.tags) model.groupInfo.items }

