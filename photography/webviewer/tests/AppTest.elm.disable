module AppTest exposing (..)

import Expect exposing (Expectation)
import Fuzz exposing (Fuzzer, int, list, string)
import Test exposing (..)
import Fuzzing as Fuzzing
import App as App
import Json.Decode exposing (decodeString)
import GroupInfo as GroupInfo
import MediaFileInfo as MediaFileInfo
import Set as Set

extractTag: List MediaFileInfo.Model -> String
extractTag mediaFiles =
    mediaFiles 
    |> List.take 7
    |> List.map .tags
    |> List.foldl Set.union Set.empty
    |> Set.toList
    |> List.head
    |> Maybe.withDefault "tag"
createAppModel: List MediaFileInfo.Model -> App.Model
createAppModel mediaFiles =
    App.reset
    |> App.setGroupInfo (GroupInfo.reset |> GroupInfo.setItems (mediaFiles ++ [Fuzzing.defaultMediaFile]))
    |> App.setTag (extractTag mediaFiles)

suite : Test
suite =
    describe "App Module"
    [
     describe "filterByTags"
        [
            fuzz (list Fuzzing.mediaFileInfo) "should filter content" <|
                \items ->
                    createAppModel items
                    |> App.filterByTag
                    |> .items
                    |> List.length
                    |> Expect.atLeast 1
       ]

    ]