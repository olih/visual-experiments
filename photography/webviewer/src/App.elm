module App exposing (Model, reset, Msg(..), setGroupInfo, setItems, setTag, filterByTag, view)
import Http
import GroupInfo as GroupInfo
import MediaFileInfo as MediaFileInfo
import Set exposing(Set)
import Html exposing (Html, div, select, option, text, span, i)
import Html.Attributes as Attr exposing (attribute, name)
import Html.Events as Events
import Browser exposing(UrlRequest)
import Url exposing (Url)
import Browser.Navigation as Nav
import Tags as Tags
type alias Model =
    { 
        navKey: Nav.Key
        , groupInfo: GroupInfo.Model
        , tag : String
        , items: List MediaFileInfo.Model
    }

reset: Nav.Key -> Model
reset key = {
    navKey = key
    , groupInfo = GroupInfo.reset
    , tag = "2020"
    , items = []
 }

type Msg
  = GotGroupInfo (Result Http.Error GroupInfo.Model)
  | SelectTag String
  | LinkClicked UrlRequest
  | UrlChanged Url

setTag: String -> Model -> Model
setTag tag model =
    { model | tag = tag}

setGroupInfo: GroupInfo.Model -> Model -> Model
setGroupInfo groupInfo model =
    { model | groupInfo = groupInfo, tag = GroupInfo.getDefaultTag groupInfo }
    |> filterByTag

setItems: List MediaFileInfo.Model -> Model -> Model
setItems items model =
    { model | items = items}

filterByTag: Model -> Model
filterByTag model =
    { model | items = List.filter (\item -> Set.member model.tag item.tags) model.groupInfo.items }

viewItems : List MediaFileInfo.Model -> Html a
viewItems mediaFiles =
    mediaFiles
    |> List.map MediaFileInfo.view
    |> div []

asOption: String -> Html a
asOption desc =
    option [] [ text desc ]
viewTag : String -> Set String -> Html Msg
viewTag tag tags =
    div [ Attr.class "control has-icons-left" ]
    [ div [ Attr.class "select is-small" ]
        [ 
            option [ attribute "selected" "" ]
                [ text tag ]
            :: (Tags.toListWithoutOne tag tags |> List.map asOption) |> select [ name "tags", Events.onInput SelectTag]
        ]
    , span [ Attr.class "icon is-small is-left" ]
        [ i [ Attr.class "fas fa-globe" ]
            []
        ]
    ]

view: Model ->  Html Msg
view model =
    div [] [
        viewTag model.tag model.groupInfo.tags
        , viewItems model.items
    ]