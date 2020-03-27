module Main exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import App as App exposing (Msg(..))
import GroupInfo as GroupInfo
-- MAIN


main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }



-- MODEL

init : () -> (App.Model, Cmd App.Msg)
init _ =
  (App.reset, fetchGroupInfo)



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
          (App.reset, Cmd.none)

-- SUBSCRIPTIONS

subscriptions : App.Model -> Sub App.Msg
subscriptions model =
  Sub.none

-- VIEW

view : App.Model -> Html App.Msg
view model =
  div []
    [ h2 [] [ text "Photography by Olivier Huin" ]
    , App.view model
    ]



-- HTTP

fetchGroupInfo : Cmd App.Msg
fetchGroupInfo =
  Http.get
    { url = "/data/group-testing.json"
    , expect = Http.expectJson GotGroupInfo GroupInfo.decoder
    }
