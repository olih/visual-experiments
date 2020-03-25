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
  (App.reset, fetchGroupInfo())



-- UPDATE

update : App.Msg -> App.Model -> (App.Model, Cmd App.Msg)
update msg model =
  case msg of
    ToggleTag tag ->
      (App.toggleTag tag model, Cmd.none)
    
    GotGroupInfo result ->
      case result of
        Ok groupInfo ->
          (App.setGroupInfo groupInfo, Cmd.none)

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
    [ h2 [] [ text "Random image" ]
    , viewGif model
    ]


viewGif : App.Model -> Html App.Msg
viewGif model =
  case model of
    Failure ->
      div []
        [ text "I could not load a random image for some reason. "
        , button [ onClick MorePlease ] [ text "Try Again from application/json!" ]
        ]

    Loading ->
      text "Loading..."

    Success url ->
      div []
        [ button [ onClick MorePlease, style "display" "block" ] [ text "Another from application/json!" ]
        , img [ src url ] []
        ]



-- HTTP

fetchGroupInfo : Cmd App.Msg
fetchGroupInfo =
  Http.get
    { url = "http://localhost:8080/some-json.json"
    , expect = Http.expectJson GotGroupInfo GroupInfo.decoder
    }
