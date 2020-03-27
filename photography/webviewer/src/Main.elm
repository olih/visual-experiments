module Main exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Url exposing (Url)
import Browser.Navigation as Nav
import App as App exposing (Msg(..))
import GroupInfo as GroupInfo
-- MAIN


main =
  Browser.application
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    , onUrlRequest = LinkClicked
    , onUrlChange = UrlChanged
    }



getGroupId: Url -> String
getGroupId url =
    url.fragment |> Maybe.withDefault "default"

-- MODEL

init : () -> Url -> Nav.Key -> (App.Model, Cmd App.Msg)
init _ url key=
  (App.reset key, fetchGroupInfo <| getGroupId url)



-- UPDATE

update : App.Msg -> App.Model -> (App.Model, Cmd App.Msg)
update msg model =
  case msg of
    SelectTag tag ->
      (App.setTag tag model |> App.filterByTag, Cmd.none)
    
    GotGroupInfo result ->
      case result of
        Ok groupInfo ->
          (App.setGroupInfo groupInfo model, Cmd.none)

        Err _ ->
          (model, Cmd.none)
        
    LinkClicked urlRequest ->
        case urlRequest of
            Browser.Internal url ->
                ( model
                , Nav.pushUrl model.navKey (Url.toString url)
                )
            Browser.External href ->
                ( model
                , Nav.load href
                )        
    UrlChanged url ->
        stepUrl url model


stepUrl : Url -> App.Model -> (App.Model, Cmd App.Msg)
stepUrl url model =
    (model,  fetchGroupInfo <| getGroupId url)

-- SUBSCRIPTIONS

subscriptions : App.Model -> Sub App.Msg
subscriptions model =
  Sub.none

-- VIEW

view : App.Model -> Browser.Document App.Msg
view model =
  { title = "Photography Olivier Huin"
  , body =
      [ viewHeader
      , App.view model
      , viewFooter
      ]
  }
  

viewHeader : Html msg
viewHeader =
  div []
    [ h2 [] [ text "Photography by Olivier Huin" ]
    ]

viewFooter : Html msg
viewFooter =
  div [class "footer"]
    [ 
    ]
-- HTTP

fetchGroupInfo : String -> Cmd App.Msg
fetchGroupInfo groupId =
  Http.get
    { url = ["/data/group-", groupId, ".json"] |> String.concat
    , expect = Http.expectJson GotGroupInfo GroupInfo.decoder
    }
